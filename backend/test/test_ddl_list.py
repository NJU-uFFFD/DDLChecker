
import unittest

from app import app
from db import db
from db.ddl import Ddl
from db.user import User
from db.course import Course
import json
import time
import uuid
import copy


class TestDdlList(unittest.TestCase):
    ddls = []
    def setUp(self):
        self.app = app
        self.client = self.app.test_client()
        with self.app.app_context():
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
            self.ddls = []
            ddl1 = Ddl(1, "title1", int(time.time())*1000, int(time.time())*1000-313423000, "content", "", "797fe34b-3741-4d59-a1e6-4dbcd0e54892","f15684f5-d870-4a9d-b859-e7eec3c6e3b5", source_ddl_id=None, complete_time=None, is_completed=False)
            for i in range(30):
                ddl = copy.deepcopy(ddl1)
                ddl.create_time += 60000 * i
                ddl.ddl_time -= 60000 * (30-i)
                if i % 2 == 1:
                    ddl.is_completed = True
                    ddl.complete_time = ddl.create_time + 1000 * i
                if i % 3 == 1:
                    ddl.tag = '紧急'
                if i % 3 == 2:
                    ddl.tag = '宽松'
                if i >= 15:
                    ddl.ddl_time += 3600000
                db.session.add(ddl)
                db.session.commit()
                self.ddls.append([ddl.id,ddl.ddl_time,ddl.create_time,ddl.complete_time])
            ddl1.userid = 2
            db.session.add(ddl1)
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            # m = MetaData()
            # m.reflect()
            # m.drop_all()
            db.drop_all()

    def test_list_ddl(self):
        with self.app.app_context():
            ret = self.client.post('/ddl/list', headers={
                'x-wx-source': 'test',
                'x-wx-openid': '114514'
            }, json={
                'page': 1,
                'size': 50
            })
            self.assertEqual(200, ret.status_code)
            ret = json.loads(ret.data.decode('utf-8'))
            self.assertEqual(0, ret['code'])
            self.assertEqual(30,ret['data']['ddl_count'])
            dlist = ret['data']['ddl_list']
            for i in range(30):
                a = dlist[i]
                b = self.ddls[i]
                self.assertEqual((a['id'],a['ddl_time']),(b[0],b[1]))

    def test_list_ddl_with_sorter(self):
        with self.app.app_context():
            ret = self.client.post('/ddl/list', headers={
                'x-wx-source': 'test',
                'x-wx-openid': '114514'
            }, json={
                'page': 1,
                'size': 50,
                'sorter': {
                    'reversed': True
                }
            })
            self.assertEqual(200, ret.status_code)
            ret = json.loads(ret.data.decode('utf-8'))
            self.assertEqual(0, ret['code'])
            self.assertEqual(30,ret['data']['ddl_count'])
            dlist = ret['data']['ddl_list']
            for i in range(30):
                a = dlist[i]
                b = self.ddls[29-i]
                self.assertEqual((a['id'],a['ddl_time']),(b[0],b[1]))

    def test_list_ddl_with_filter(self):
        with self.app.app_context():
            ret = self.client.post('/ddl/list', headers={
                'x-wx-source': 'test',
                'x-wx-openid': '114514'
            }, json={
                'page': 1,
                'size': 50,
                'filter': {
                    'is_completed': True,
                    'is_overtime': False
                }
            })
            self.assertEqual(200, ret.status_code)
            ret = json.loads(ret.data.decode('utf-8'))
            self.assertEqual(0, ret['code'])
            self.assertEqual(8,ret['data']['ddl_count'])
            dlist = ret['data']['ddl_list']
            for i in range(8):
                a = dlist[i]
                b = self.ddls[i*2+15]
                self.assertEqual((a['id'],a['ddl_time']),(b[0],b[1]))

    def test_list_ddl_with_more_filters(self):
        with self.app.app_context():
            ret = self.client.post('/ddl/list', headers={
                'x-wx-source': 'test',
                'x-wx-openid': '114514'
            }, json={
                'page': 1,
                'size': 50,
                'filter': {
                    'is_completed': False,
                    'is_overtime': True
                },
                'tag': '紧急'
            })
            self.assertEqual(200, ret.status_code)
            ret = json.loads(ret.data.decode('utf-8'))
            self.assertEqual(0, ret['code'])
            self.assertEqual(2,ret['data']['ddl_count'])
            dlist = ret['data']['ddl_list']
            for i in range(2):
                a = dlist[i]
                b = self.ddls[4+i*6]
                self.assertEqual((a['id'],a['ddl_time']),(b[0],b[1]))

    def test_list_ddl_with_time_ranges(self):
        with self.app.app_context():
            ret = self.client.post('/ddl/list', headers={
                'x-wx-source': 'test',
                'x-wx-openid': '114514'
            }, json={
                'page': 1,
                'size': 50,
                'ddl_time_range': {
                    'start': (self.ddls[1][1]),
                    'end': (self.ddls[14][1])
                },
                'complete_time_range': {
                    'start': (self.ddls[5][3]),
                    'end': (self.ddls[19][3])
                },
                'create_time_range': {
                    'start': (self.ddls[3][2]),
                    'end': (self.ddls[12][2])
                }
            })
            self.assertEqual(200, ret.status_code)
            ret = json.loads(ret.data.decode('utf-8'))
            self.assertEqual(0, ret['code'])
            self.assertEqual(4,ret['data']['ddl_count'])
            dlist = ret['data']['ddl_list']
            for i in range(4):
                a = dlist[i]
                b = self.ddls[2*i+5]
                self.assertEqual((a['id'],a['ddl_time']),(b[0],b[1]))

    def test_list_ddl_with_pages(self):
        with self.app.app_context():
            for i in range(30):
                ret = self.client.post('/ddl/list', headers={
                    'x-wx-source': 'test',
                    'x-wx-openid': '114514'
                }, json={
                    'page': i+1,
                    'size': 1
                })
                self.assertEqual(200, ret.status_code)
                ret = json.loads(ret.data.decode('utf-8'))
                self.assertEqual(0, ret['code'])
                self.assertEqual(30,ret['data']['ddl_count'])
                self.assertEqual(1,len(ret['data']['ddl_list']))
                dlist = ret['data']['ddl_list']
                b = self.ddls[i]
                a = dlist[0]
                self.assertEqual((a['id'],a['ddl_time']),(b[0],b[1]))

    def test_list_ddl_with_bad_time_ranges(self):
        with self.app.app_context():
            for i in ('ddl_time_range','create_time_range','complete_time_range'):
                for j in ({'start':100000000},{'end':10000000},{},{'start':2,'end':1}):
                    ret = self.client.post('/ddl/list', headers={
                        'x-wx-source': 'test',
                        'x-wx-openid': '114514'
                    }, json={
                        'page': 1,
                        'size': 50,
                        i: j
                    })
                    self.assertEqual(400, ret.status_code)
                    ret = json.loads(ret.data.decode('utf-8'))
                    self.assertEqual(-1, ret['code'])
