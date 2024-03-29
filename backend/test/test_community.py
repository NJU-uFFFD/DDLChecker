
import unittest

from app import app
from db import db
from db.ddl import Ddl
from db.user import User
from db.course import Course
from db.userSubs import UserSubscriptions
from db.sourceDdl import SourceDdl
import json
import time
import uuid
import copy


class TestCommiunity(unittest.TestCase):
    def setUp(self):
        self.app = app
        assert 'tencent' not in app.config['SQLALCHEMY_DATABASE_URI'] #再删库我是傻逼
        self.client = self.app.test_client()
        self.average_complete_time_percentage = 0
        self.total_time = 0
        with self.app.app_context():
            db.create_all()
            user = User('114514', '田所浩二')
            db.session.add(user)
            db.session.commit()
            user = User('514', 'こいし')
            db.session.add(user)
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            # m = MetaData()
            # m.reflect()
            # m.drop_all()
            db.drop_all()

    def test_add_course(self):
        with self.app.app_context():
            ret = self.client.post('/community/course/add', headers={
                    'x-wx-source': 'test',
                    'x-wx-openid': '114514'
                }, json={
                    'platform_uuid': (str(uuid.uuid4())),
                    'course_name': 'C-PL'
                })
            self.assertEqual(200, ret.status_code)
            ret = json.loads(ret.data.decode('utf-8'))
            self.assertEqual(0, ret['code'])
            ret = ret['data']
            course = Course.query.get(ret['course_uuid'])
            usersub = UserSubscriptions.query.filter(UserSubscriptions.course_uuid == ret['course_uuid'] and UserSubscriptions.userid == 1).first()
            self.assertIsNotNone(usersub)
            self.assertEqual(course.course_name,'C-PL')
            self.assertEqual(course.creator_id,1)
            self.assertEqual(usersub.userid,1)
            self.assertEqual(usersub.course_uuid,course.course_uuid)

    def test_add_existing_course(self):
        with self.app.app_context():
            platform_uuid = str(uuid.uuid4())
            course = Course('C-PL',str(uuid.uuid5(uuid.UUID(platform_uuid),'C-PL')),platform_uuid)
            db.session.add(course)
            db.session.commit()
            ret = self.client.post('/community/course/add', headers={
                    'x-wx-source': 'test',
                    'x-wx-openid': '114514'
                }, json={
                    'platform_uuid': (course.platform_uuid),
                    'course_name': (course.course_name)
                })
            self.assertEqual(400, ret.status_code)
            ret = json.loads(ret.data.decode('utf-8'))
            self.assertEqual(-1, ret['code'])
            ret = ret['data']
            course = Course.query.count()
            self.assertEqual(course, 1)

    def test_list_course(self):
        with self.app.app_context():
            platform_uuid = str(uuid.uuid4())
            course = Course('C-PL',str(uuid.uuid5(uuid.UUID(platform_uuid),'C-PL')),platform_uuid)
            db.session.add(course)
            db.session.commit()
            usersub = UserSubscriptions(1, course.course_uuid, platform_uuid)
            db.session.add(usersub)
            db.session.commit()
            ret = self.client.post('/community/course/list', headers={
                    'x-wx-source': 'test',
                    'x-wx-openid': '114514'
                }, json={
                    'page': 1,
                    'size': 20
                })
            self.assertEqual(200, ret.status_code)
            ret = json.loads(ret.data.decode('utf-8'))
            self.assertEqual(0, ret['code'])
            ret = ret['data']
            self.assertEqual(ret['course_count'], 1)
            self.assertEqual(ret['courses'][0]['course_name'], course.course_name)
            self.assertEqual(ret['courses'][0]['course_uuid'], course.course_uuid)
            self.assertEqual(ret['courses'][0]['subscribed'], True)

    def test_list_course_with_keyword(self):
        with self.app.app_context():
            platform_uuid = str(uuid.uuid4())
            course = Course('C-PL',str(uuid.uuid5(uuid.UUID(platform_uuid),'C-PL')),platform_uuid)
            db.session.add(course)
            db.session.commit()
            course2 = Course('D-PL',str(uuid.uuid5(uuid.UUID(platform_uuid),'D-PL')),platform_uuid)
            db.session.add(course2)
            db.session.commit()
            ret = self.client.post('/community/course/list', headers={
                    'x-wx-source': 'test',
                    'x-wx-openid': '114514'
                }, json={
                    'page': 1,
                    'size': 20,
                    'key_word': 'D'
                })
            self.assertEqual(200, ret.status_code)
            ret = json.loads(ret.data.decode('utf-8'))
            self.assertEqual(0, ret['code'])
            ret = ret['data']
            self.assertEqual(ret['course_count'], 1)
            self.assertEqual(ret['courses'][0]['course_name'], course2.course_name)
            self.assertEqual(ret['courses'][0]['course_uuid'], course2.course_uuid)

    def test_subscribe_course(self):
        with self.app.app_context():
            platform_uuid = str(uuid.uuid4())
            course = Course('C-PL',str(uuid.uuid5(uuid.UUID(platform_uuid),'C-PL')),platform_uuid)
            db.session.add(course)
            db.session.commit()
            course2 = Course('D-PL',str(uuid.uuid5(uuid.UUID(platform_uuid),'D-PL')),platform_uuid)
            db.session.add(course2)
            db.session.commit()
            usersub = UserSubscriptions(1, course.course_uuid, platform_uuid)
            db.session.add(usersub)
            db.session.commit()
            ret = self.client.post('/community/course/subscribe', headers={
                    'x-wx-source': 'test',
                    'x-wx-openid': '114514'
                }, json={
                    'course_uuid': (course2.course_uuid)
                })
            self.assertEqual(200, ret.status_code)
            ret = json.loads(ret.data.decode('utf-8'))
            self.assertEqual(0, ret['code'])
            ret = ret['data']
            self.assertEqual(UserSubscriptions.query.get(ret['id']).userid, 1)
            self.assertEqual(UserSubscriptions.query.get(ret['id']).course_uuid, course2.course_uuid)
            ret = self.client.post('/community/course/subscribe', headers={
                    'x-wx-source': 'test',
                    'x-wx-openid': '114514'
                }, json={
                    'course_uuid': (course.course_uuid)
                })
            self.assertEqual(400, ret.status_code)
            ret = json.loads(ret.data.decode('utf-8'))
            self.assertEqual(-1, ret['code'])

    def test_unsubscribe_course(self):
        with self.app.app_context():
            platform_uuid = str(uuid.uuid4())
            course = Course('C-PL',str(uuid.uuid5(uuid.UUID(platform_uuid),'C-PL')),platform_uuid)
            db.session.add(course)
            db.session.commit()
            course2 = Course('D-PL',str(uuid.uuid5(uuid.UUID(platform_uuid),'D-PL')),platform_uuid)
            db.session.add(course2)
            db.session.commit()
            usersub = UserSubscriptions(1, course.course_uuid, platform_uuid)
            db.session.add(usersub)
            db.session.commit()
            ret = self.client.post('/community/course/unsubscribe', headers={
                    'x-wx-source': 'test',
                    'x-wx-openid': '114514'
                }, json={
                    'course_uuid': (course.course_uuid)
                })
            self.assertEqual(200, ret.status_code)
            ret = json.loads(ret.data.decode('utf-8'))
            self.assertEqual(0, ret['code'])
            ret = ret['data']
            self.assertIsNone(UserSubscriptions.query.get(ret['id']))
            self.assertEqual(UserSubscriptions.query.count(), 0)
            ret = self.client.post('/community/course/unsubscribe', headers={
                    'x-wx-source': 'test',
                    'x-wx-openid': '114514'
                }, json={
                    'course_uuid': (course2.course_uuid)
                })
            self.assertEqual(400, ret.status_code)
            ret = json.loads(ret.data.decode('utf-8'))
            self.assertEqual(-1, ret['code'])

    def test_delete_course(self):
        with self.app.app_context():
            platform_uuid = str(uuid.uuid4())
            course = Course('C-PL',str(uuid.uuid5(uuid.UUID(platform_uuid),'C-PL')),platform_uuid,creator_id=1)
            db.session.add(course)
            db.session.commit()
            ret = self.client.post('/community/course/delete', headers={
                    'x-wx-source': 'test',
                    'x-wx-openid': '114514'
                }, json={
                    'course_uuid': (course.course_uuid)
                })
            self.assertEqual(200, ret.status_code)
            ret = json.loads(ret.data.decode('utf-8'))
            self.assertEqual(0, ret['code'])
            course = Course.query.count()
            self.assertEqual(course, 0)

    def test_add_ddl(self):
        with self.app.app_context():
            platform_uuid = str(uuid.uuid4())
            course = Course('C-PL',str(uuid.uuid5(uuid.UUID(platform_uuid),'C-PL')),platform_uuid,creator_id=1)
            db.session.add(course)
            db.session.commit()
            ddl_time = int(time.time())*1000
            ret = self.client.post('/community/ddl/add', headers={
                    'x-wx-source': 'test',
                    'x-wx-openid': '114514'
                }, json={
                    'course_uuid': course.course_uuid,
                    'title': 'title',
                    'content': 'content',
                    'ddl_time': ddl_time,
                })
            self.assertEqual(200, ret.status_code)
            ret = json.loads(ret.data.decode('utf-8'))
            self.assertEqual(0, ret['code'])
            ret = ret['data']
            ddl = SourceDdl.query.get(ret['id'])
            self.assertIsNotNone(ddl)
            self.assertEqual(ddl.course_uuid,course.course_uuid)
            self.assertEqual(ddl.platform_uuid,course.platform_uuid)
            self.assertEqual(ddl.title,'title')
            self.assertEqual(ddl.content,'content')
            self.assertEqual(ddl.ddl_time,ddl_time)
            self.assertEqual(ddl.creator_id,1)

    def test_delete_ddl(self):
        with self.app.app_context():
            platform_uuid = str(uuid.uuid4())
            course = Course('C-PL',str(uuid.uuid5(uuid.UUID(platform_uuid),'C-PL')),platform_uuid,creator_id=1)
            db.session.add(course)
            db.session.commit()
            source_ddl = SourceDdl(course.course_uuid,platform_uuid,'title','content',
                None,int(time.time())*1000,int(time.time())*1000,1)
            db.session.add(source_ddl)
            db.session.commit()
            ret = self.client.post('/community/ddl/delete', headers={
                    'x-wx-source': 'test',
                    'x-wx-openid': '114514'
                }, json={
                    'id': source_ddl.id
                })
            self.assertEqual(200, ret.status_code)
            ret = json.loads(ret.data.decode('utf-8'))
            self.assertEqual(0, ret['code'])
            self.assertEqual(SourceDdl.query.count(), 0)