
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


class TestHistory(unittest.TestCase):
    ddls = []
    def setUp(self):
        self.app = app
        self.client = self.app.test_client()
        self.average_complete_time_percentage = 0
        self.total_time = 0
        with self.app.app_context():
            db.create_all()
            user = User('114514', '田所浩二')
            db.session.add(user)
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            # m = MetaData()
            # m.reflect()
            # m.drop_all()
            db.drop_all()

    def test_history(self):
        with self.app.app_context():
            self.ddls = []
            ddl1 = Ddl(1, "title1", int(time.time())*1000, int(time.time())*1000-313423000, "content", "", None, "f15684f5-d870-4a9d-b859-e7eec3c6e3b5", source_ddl_id=None, complete_time=None, is_completed=False)
            for i in range(30):
                ddl = copy.deepcopy(ddl1)
                ddl.create_time += 60000 * i
                ddl.ddl_time -= 60000 * (30-i)

                if i % 2 == 1:
                    ddl.is_completed = True
                    ddl.complete_time = ddl.create_time + 1000 * i
                    self.average_complete_time_percentage += (ddl.complete_time - ddl.create_time)
                if i % 3 == 1:
                    ddl.tag = '紧急'
                if i % 3 == 2:
                    ddl.tag = '宽松'
                if i >= 15:
                    ddl.ddl_time += 3600000
                db.session.add(ddl)
                db.session.commit()
                self.total_time += ddl.ddl_time - ddl.create_time
                self.ddls.append([ddl.id,ddl.ddl_time,ddl.create_time,ddl.complete_time])

            ret = self.client.post('/history/stat', headers={
                'x-wx-source': 'test',
                'x-wx-openid': '114514'
            }, json={})
            self.assertEqual(200, ret.status_code)
            ret = json.loads(ret.data.decode('utf-8'))
            self.assertEqual(0, ret['code'])
            ret = ret['data']
            self.assertEqual(ret['completed_count'],15)
            self.assertEqual(ret['urgent_count'],5)
            self.assertEqual(ret['overtime_count'],8)
            self.assertEqual(ret['completed_rate'],0.5)
            self.assertEqual(ret['average_complete_time_percentage'], self.average_complete_time_percentage / self.total_time)
            self.assertEqual(ret['first_time'], self.ddls[0][2])
            self.assertEqual(ret['last_time'], self.ddls[29][1])

    def test_history_without_ddls(self):
        ret = self.client.post('/history/stat', headers={
                'x-wx-source': 'test',
                'x-wx-openid': '114514'
            }, json={})
        self.assertEqual(200, ret.status_code)
        ret = json.loads(ret.data.decode('utf-8'))
        self.assertEqual(0, ret['code'])
        ret = ret['data']
        self.assertEqual(ret['completed_count'],0)
        self.assertEqual(ret['urgent_count'],0)
        self.assertEqual(ret['overtime_count'],0)
        self.assertEqual(ret['completed_rate'],1)
        self.assertEqual(ret['average_complete_time_percentage'], 0)
        self.assertLess(abs(ret['first_time']-int(time.time())*1000), 1000)
        self.assertLess(abs(ret['last_time']-int(time.time())*1000), 1000)
