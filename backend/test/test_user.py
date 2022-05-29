
import unittest

from app import app
from db import db
from db.user import User
from sqlalchemy import MetaData
import json


class TestUser(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.client = self.app.test_client()
        with self.app.app_context():
            # db.drop_all()
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            # m = MetaData()
            # m.reflect()
            # m.drop_all()
            db.drop_all()
            pass

    def test_index(self):
        ret = self.client.get('/')
        self.assertEqual(b'hello!', ret.data)
        self.assertEqual(200, ret.status_code)

    def test_register(self):
        with self.app.app_context():
            ret = self.client.post('/user/register', headers={
                'x-wx-source': 'test',
                'x-wx-openid': '114514'
            }, json={})
            self.assertEqual(200, ret.status_code)
            ret = json.loads(ret.data.decode('utf-8'))
            self.assertEqual(0, ret['code'])
            self.assertIsNotNone(User.query.get(ret['data']['userid']))

    def test_register_with_name(self):
        with self.app.app_context():
            ret = self.client.post('/user/register', headers={
                'x-wx-source': 'test',
                'x-wx-openid': '114514'
            }, json={
                'username': '田所浩二' * 20
            })
            self.assertEqual(200, ret.status_code)
            ret = json.loads(ret.data.decode('utf-8'))
            self.assertEqual(0, ret['code'])
            self.assertIsNotNone(User.query.get(ret['data']['userid']))
            self.assertEqual('田所浩二' * 20, User.query.get(ret['data']['userid']).username)

    def test_register_with_too_long_name(self):
        with self.app.app_context():
            ret = self.client.post('/user/register', headers={
                'x-wx-source': 'test',
                'x-wx-openid': '114514'
            }, json={
                'username': '田所浩二' * 27
            })
            # print(ret.data)
            self.assertEqual(400, ret.status_code)
            ret = json.loads(ret.data.decode('utf-8'))
            self.assertEqual(-1, ret['code'])
            self.assertIsNone(User.query.first())

    def test_username(self):
        with self.app.app_context():
            user = User('114514', '田所浩二')
            db.session.add(user)
            db.session.commit()
            ret = self.client.post('/user/username', headers={
                'x-wx-source': 'test',
                'x-wx-openid': '114514'
            }, json={
                'id': 1
            })
            self.assertEqual(200, ret.status_code)
            ret = json.loads(ret.data.decode('utf-8'))
            self.assertEqual(0, ret['code'])
            self.assertEqual('田所浩二', ret['data']['username'])

    def test_nonexistid_username(self):
        with self.app.app_context():
            user = User('114514', '田所浩二')
            db.session.add(user)
            db.session.commit()
            ret = self.client.post('/user/username', headers={
                'x-wx-source': 'test',
                'x-wx-openid': '114514'
            }, json={
                'id': 114514
            })
            self.assertEqual(200, ret.status_code)
            ret = json.loads(ret.data.decode('utf-8'))
            self.assertEqual(-1, ret['code'])
            self.assertIn('not found', ret['msg'])

    def test_rename(self):
        with self.app.app_context():
            user = User('114514', '田所浩二')
            db.session.add(user)
            db.session.commit()
            ret = self.client.post('/user/rename', headers={
                'x-wx-source': 'test',
                'x-wx-openid': '114514'
            }, json={
                'username': '田所浩三'
            })
            self.assertEqual(200, ret.status_code)
            ret = json.loads(ret.data.decode('utf-8'))
            self.assertEqual(0, ret['code'])
            self.assertEqual(user.username, '田所浩三')

    def test_rename_with_too_long_name(self):
        with self.app.app_context():
            user = User('114514', '田所浩二')
            db.session.add(user)
            db.session.commit()
            ret = self.client.post('/user/rename',headers={
                'x-wx-source':'test',
                'x-wx-openid':'114514'
                },json={
                'username':'田所浩三'*27
                })
            self.assertEqual(400,ret.status_code)
            ret = json.loads(ret.data.decode('utf-8'))
            self.assertEqual(-1,ret['code'])
            self.assertEqual(user.username,'田所浩二')

