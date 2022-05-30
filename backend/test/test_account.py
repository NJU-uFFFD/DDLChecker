import unittest

from app import app
from db import db
from db.account import Account
from db.user import User
import json
import uuid

from db.userSubs import UserSubscriptions
from util.encrypt import aes_encrypt


class TestAccount(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
            user = User('114514', '田所浩二')
            user2 = User('1919810', '田所浩三')
            db.session.add(user)
            db.session.add(user2)
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def test_available_account(self):
        ret = self.client.post("/account/available", headers={
            'x-wx-source': 'test',
            'x-wx-openid': '114514'
        })
        self.assertEqual(ret.status_code, 200)
        ret = json.loads(ret.data.decode("utf-8"))
        self.assertEqual(ret['code'], 0)
        self.assertIsNotNone(ret['data'].get("available_account_type"))

    def test_add_account(self):
        with self.app.app_context():
            ret = self.client.post("/account/add", headers={
                'x-wx-source': 'test',
                'x-wx-openid': '114514'
            }, json={
                'platform_uuid': '68dc1014-7bfe-4ea3-a000-5734303d9f59',
                'fields': {"account": "田所浩二", "password": "nmsl"}
            })
            self.assertEqual(ret.status_code, 200)
            ret = json.loads(ret.data.decode("utf-8"))
            self.assertEqual(ret['code'], 0)
            f = Account.query.filter(Account.id == ret['data']['id']).first().fields
            self.assertEqual(f, aes_encrypt(json.dumps({"account": "田所浩二", "password": "nmsl"})))

    def test_add_account_nonexist_platform(self):
        with self.app.app_context():
            ret = self.client.post("/account/add", headers={
                'x-wx-source': 'test',
                'x-wx-openid': '114514'
            }, json={
                'platform_uuid': str(uuid.uuid4()),
                'fields': {"account": "田所浩三", "password": "nmysl"}
            })
            self.assertEqual(ret.status_code, 200)
            ret = json.loads(ret.data.decode("utf-8"))
            self.assertEqual(-1, ret['code'])
            self.assertIn("Invalid platform_uuid", ret['msg'])
            self.assertEqual(Account.query.count(), 0)

    def test_add_account_same_platform(self):
        with self.app.app_context():
            account = Account("1", '68dc1014-7bfe-4ea3-a000-5734303d9f59', aes_encrypt(json.dumps({"account": "田所浩二", "password": "nmsl"})))
            db.session.add(account)
            db.session.commit()
            ret = self.client.post("/account/add", headers={
                'x-wx-source': 'test',
                'x-wx-openid': '114514'
            }, json={
                'platform_uuid': '68dc1014-7bfe-4ea3-a000-5734303d9f59',
                'fields': {"account": "田所浩三", "password": "nmysl"}
            })
            self.assertEqual(ret.status_code, 200)
            ret = json.loads(ret.data.decode("utf-8"))
            self.assertEqual(-1, ret['code'])
            self.assertIn("more than one", ret['msg'])
            self.assertEqual(Account.query.count(), 1)

    def test_too_many_account(self):
        with self.app.app_context():
            for _ in range(0, 29):
                ret1 = self.client.post("/account/add", headers={
                    'x-wx-source': 'test',
                    'x-wx-openid': '114514'
                }, json={
                    'platform_uuid': '68dc1014-7bfe-4ea3-a000-5734303d9f59',
                    'fields': {"account": "田所浩二", "password": "nmsl"}
                })
                ret2 = self.client.post("/account/delete", headers={
                    'x-wx-source': 'test',
                    'x-wx-openid': '114514'
                }, json={
                    'id': json.loads(ret1.data.decode("utf-8"))['data']['id']
                })
            ret1 = self.client.post("/account/add", headers={
                'x-wx-source': 'test',
                'x-wx-openid': '114514'
            }, json={
                'platform_uuid': '68dc1014-7bfe-4ea3-a000-5734303d9f59',
                'fields': {"account": "田所浩二", "password": "nmsl"}
            })
            self.assertEqual(ret1.status_code, 200)
            ret1 = json.loads(ret1.data.decode("utf-8"))
            self.assertEqual(-1, ret1['code'])
            self.assertIn("times limitation", ret1['msg'])
            self.assertEqual(Account.query.count(), 0)

    def test_list_account(self):
        with self.app.app_context():
            account = Account("1", '68dc1014-7bfe-4ea3-a000-5734303d9f59', aes_encrypt(json.dumps({"account": "田所浩二", "password": "nmsl"})))
            db.session.add(account)
            account = Account("2", '68dc1014-7bfe-4ea3-a000-5734303d9f59', aes_encrypt(json.dumps({"account": "田所浩三", "password": "nmysl"})))
            db.session.add(account)
            db.session.commit()
            ret = self.client.post("/account/list", headers={
                'x-wx-source': 'test',
                'x-wx-openid': '114514'
            })
            self.assertEqual(ret.status_code, 200)
            ret = json.loads(ret.data.decode("utf-8"))
            self.assertEqual(ret['code'], 0)
            self.assertEqual(ret['data']['account_count'], 1)

    def test_delete_account(self):
        with self.app.app_context():
            account = Account("1", '68dc1014-7bfe-4ea3-a000-5734303d9f59', aes_encrypt(json.dumps({"account": "田所浩二", "password": "nmsl"})))
            db.session.add(account)
            account = Account("2", '68dc1014-7bfe-4ea3-a000-5734303d9f59', aes_encrypt(json.dumps({"account": "田所浩三", "password": "nmysl"})))
            db.session.add(account)
            db.session.commit()
            ret = self.client.post("/account/delete", headers={
                'x-wx-source': 'test',
                'x-wx-openid': '114514'
            }, json={
                "id": 1
            })
            self.assertEqual(ret.status_code, 200)
            ret = json.loads(ret.data.decode("utf-8"))
            self.assertEqual(ret['code'], 0)
            self.assertIsNone(Account.query.filter(Account.id == 1).first())
            self.assertIsNotNone(Account.query.filter(Account.id == 2).first())

    def test_delete_account_with_sub(self):
        with self.app.app_context():
            account = Account("1", '68dc1014-7bfe-4ea3-a000-5734303d9f59', aes_encrypt(json.dumps({"account": "田所浩二", "password": "nmsl"})))
            sub = UserSubscriptions("1", str(uuid.uuid4()), '68dc1014-7bfe-4ea3-a000-5734303d9f59', True)
            db.session.add(account)
            db.session.add(sub)
            db.session.commit()
            ret = self.client.post("/account/delete", headers={
                'x-wx-source': 'test',
                'x-wx-openid': '114514'
            }, json={
                "id": 1
            })
            self.assertEqual(ret.status_code, 200)
            ret = json.loads(ret.data.decode("utf-8"))
            self.assertEqual(ret['code'], 0)
            self.assertIsNone(Account.query.filter(Account.id == 1).first())
            self.assertEqual(UserSubscriptions.query.count(), 0)

    def test_delete_others_account(self):
        with self.app.app_context():
            account = Account("1", '68dc1014-7bfe-4ea3-a000-5734303d9f59', aes_encrypt(json.dumps({"account": "田所浩二", "password": "nmsl"})))
            db.session.add(account)
            account = Account("2", '68dc1014-7bfe-4ea3-a000-5734303d9f59', aes_encrypt(json.dumps({"account": "田所浩三", "password": "nmysl"})))
            db.session.add(account)
            db.session.commit()
            ret = self.client.post("/account/delete", headers={
                'x-wx-source': 'test',
                'x-wx-openid': '114514'
            }, json={
                "id": 2
            })
            self.assertEqual(ret.status_code, 200)
            ret = json.loads(ret.data.decode("utf-8"))
            self.assertEqual(ret['code'], -1)
            self.assertIn("delete others' account", ret['msg'])
            self.assertIsNotNone(Account.query.filter(Account.id == 1).first())
            self.assertIsNotNone(Account.query.filter(Account.id == 2).first())
