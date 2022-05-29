
import unittest

from app import app
from db import db
from db.ddl import Ddl
from db.user import User
from db.course import Course
import json
import time
import uuid


class TestDdl(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.client = self.app.test_client()
        with self.app.app_context():
            # db.drop_all()
            db.create_all()
            user = User('114514', '田所浩二')
            db.session.add(user)
            db.session.commit()
            user = User('514', 'こいし')
            db.session.add(user)
            db.session.commit()
            course = Course('C-PL','797fe34b-3741-4d59-a1e6-4dbcd0e54892',
                '5367accb-a315-4823-8498-ca66d6164cef',1)
            db.session.add(course)
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            # m = MetaData()
            # m.reflect()
            # m.drop_all()
            db.drop_all()

    def test_add_ddl(self):
        with self.app.app_context():
            ddl_time = (int(time.time())+3600)*1000
            platform_uuid = str(uuid.uuid4())
            ret = self.client.post('/ddl/add', headers={
                'x-wx-source': 'test',
                'x-wx-openid': '114514'
            }, json={
                'title': 't'*255,
                'ddl_time': ddl_time,
                'content': 'c'*4095,
                'platform_uuid': platform_uuid,
                'tag': 'gta'
            })
            self.assertEqual(200, ret.status_code)
            ret = json.loads(ret.data.decode('utf-8'))
            self.assertEqual(0, ret['code'])
            ddl = Ddl.query.get(ret['data']['id'])
            self.assertIsNotNone(ddl)
            self.assertEqual((ddl.title,ddl.content,ddl.ddl_time,ddl.platform_uuid,ddl.tag),
                ('t'*255,'c'*4095,ddl_time,platform_uuid,'gta'))

    def test_add_ddl_with_nonexist_course(self):
        with self.app.app_context():
            ddl_time = (int(time.time())+3600)*1000
            platform_uuid = str(uuid.uuid4())
            ret = self.client.post('/ddl/add', headers={
                'x-wx-source': 'test',
                'x-wx-openid': '114514'
            }, json={
                'title': 't'*255,
                'ddl_time': ddl_time,
                'content': 'c'*4095,
                'course_uuid': str(uuid.uuid4()),
                'platform_uuid': platform_uuid
            })
            self.assertEqual(400, ret.status_code)
            ret = json.loads(ret.data.decode('utf-8'))
            self.assertEqual(-1, ret['code'])
            self.assertIsNone(Ddl.query.first())
            self.assertIn('not exist', ret['msg'])

    def test_add_ddl_with_too_long_ago(self):
        with self.app.app_context():
            ddl_time = (int(time.time())-31*24*3600)*1000
            platform_uuid = str(uuid.uuid4())
            ret = self.client.post('/ddl/add', headers={
                'x-wx-source': 'test',
                'x-wx-openid': '114514'
            }, json={
                'title': 't'*255,
                'ddl_time': ddl_time,
                'content': 'c'*4095,
                'platform_uuid': platform_uuid
            })
            self.assertEqual(400, ret.status_code)
            ret = json.loads(ret.data.decode('utf-8'))
            self.assertEqual(-1, ret['code'])
            self.assertIsNone(Ddl.query.first())

    def test_add_ddl_with_course(self):
        with self.app.app_context():
            ddl_time = (int(time.time())+3600)*1000
            platform_uuid = str(uuid.uuid4())
            course_uuid = '797fe34b-3741-4d59-a1e6-4dbcd0e54892'
            ret = self.client.post('/ddl/add', headers={
                'x-wx-source': 'test',
                'x-wx-openid': '114514'
            }, json={
                'title': 't'*255,
                'ddl_time': ddl_time,
                'content': 'c'*4095,
                'course_uuid': course_uuid,
                'platform_uuid': platform_uuid
            })
            self.assertEqual(200, ret.status_code)
            ret = json.loads(ret.data.decode('utf-8'))
            self.assertEqual(0, ret['code'])
            ddl = Ddl.query.get(ret['data']['id'])
            self.assertIsNotNone(ddl)
            self.assertEqual((ddl.title,ddl.content,ddl.ddl_time,ddl.platform_uuid,ddl.course_uuid),
                ('t'*255,'c'*4095,ddl_time,platform_uuid,course_uuid))

    def test_update(self):
        with self.app.app_context():
            title = 'title'
            ddl_time = (int(time.time())+3600)*1000
            create_time = (int(time.time()))*1000
            content = 'content'*100
            tag = 'tag'
            course_uuid = '797fe34b-3741-4d59-a1e6-4dbcd0e54892'
            platform_uuid = str(uuid.uuid4())
            ddl = Ddl(1,title,ddl_time,create_time,content,tag,course_uuid,platform_uuid)
            db.session.add(ddl)
            db.session.commit()
            title = 'newtitle'
            ddl_time = (int(time.time())+2*3600)*1000
            content = 'newcontent'*100
            tag = 'newtag'
            course_uuid = '797fe34b-3741-4d59-a1e6-4dbcd0e54892'
            platform_uuid = str(uuid.uuid4())
            ret = self.client.post('/ddl/update', headers={
                'x-wx-source': 'test',
                'x-wx-openid': '114514'
            }, json={
                'id': ddl.id,
                'title': title,
                'ddl_time': ddl_time,
                'content': content,
                'tag': tag,
                'course_uuid': course_uuid,
                'platform_uuid': platform_uuid,
                'is_completed': True
            })
            self.assertEqual(200, ret.status_code)
            ret = json.loads(ret.data.decode('utf-8'))
            self.assertEqual(0, ret['code'])
            ddl = Ddl.query.get(ret['data']['id'])
            self.assertIsNotNone(ddl)
            self.assertEqual((ddl.title,ddl.content,ddl.ddl_time,ddl.tag,ddl.course_uuid,ddl.platform_uuid,ddl.is_completed),
                (title,content,ddl_time,tag,course_uuid,platform_uuid,True))
            self.assertEqual(True,abs(ddl.complete_time-int(time.time())*1000)<30000)

    def test_update_others(self):
        with self.app.app_context():
            title = 'title'
            ddl_time = (int(time.time())+3600)*1000
            create_time = (int(time.time()))*1000
            content = 'content'*100
            tag = 'tag'
            course_uuid = '797fe34b-3741-4d59-a1e6-4dbcd0e54892'
            platform_uuid = str(uuid.uuid4())
            ddl = Ddl(2,title,ddl_time,create_time,content,tag,course_uuid,platform_uuid)
            db.session.add(ddl)
            db.session.commit()
            ret = self.client.post('/ddl/update', headers={
                'x-wx-source': 'test',
                'x-wx-openid': '114514'
            }, json={
                'id': ddl.id,
                'title': 'newtitle',
                'content': 'newcontent',
                'is_completed': True
            })
            self.assertEqual(403, ret.status_code)
            ret = json.loads(ret.data.decode('utf-8'))
            self.assertEqual(-1, ret['code'])
            ddl = Ddl.query.get(ddl.id)
            self.assertIsNotNone(ddl)
            self.assertEqual((ddl.title,ddl.content,ddl.ddl_time,ddl.tag,ddl.course_uuid,ddl.platform_uuid,ddl.is_completed),
                (title,content,ddl_time,tag,course_uuid,platform_uuid,False))

    def test_update_nonexist_ddl(self):
        with self.app.app_context():
            title = 'title'
            ddl_time = (int(time.time())+3600)*1000
            create_time = (int(time.time()))*1000
            content = 'content'*100
            tag = 'tag'
            course_uuid = '797fe34b-3741-4d59-a1e6-4dbcd0e54892'
            platform_uuid = str(uuid.uuid4())
            ddl = Ddl(1,title,ddl_time,create_time,content,tag,course_uuid,platform_uuid)
            db.session.add(ddl)
            db.session.commit()
            ret = self.client.post('/ddl/update', headers={
                'x-wx-source': 'test',
                'x-wx-openid': '114514'
            }, json={
                'id': ddl.id+1,
                'title': 'newtitle',
                'content': 'newcontent',
                'is_completed': True
            })
            self.assertEqual(404, ret.status_code)
            ret = json.loads(ret.data.decode('utf-8'))
            self.assertEqual(-1, ret['code'])
            ddl = Ddl.query.get(ddl.id)
            self.assertIsNotNone(ddl)
            self.assertEqual((ddl.title,ddl.content,ddl.ddl_time,ddl.tag,ddl.course_uuid,ddl.platform_uuid,ddl.is_completed),
                (title,content,ddl_time,tag,course_uuid,platform_uuid,False))

    def test_update_nonexist_ddl(self):
        with self.app.app_context():

