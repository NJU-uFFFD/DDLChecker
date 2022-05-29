import unittest
from app import app
from db import db
from db.user import User
import json
class HelloWorldTest(unittest.TestCase):
	def setUp(self):
		self.app=app
		self.client=self.app.test_client()
		with self.app.app_context():
			db.drop_all()
			db.create_all()

	def tearDown(self):
		with self.app.app_context():
			#db.drop_all()
			pass

	def test_index(self):
		ret = self.client.get('/')
		self.assertEqual(b'hello!',ret.data)

	def test_register(self):
		with self.app.app_context():
			ret = self.client.post('/user/register',headers={
				'x-wx-source':'test',
				'x-wx-openid':'114514'
				},json={})
			ret = json.loads(ret.data.decode('utf-8'))
			self.assertEqual(0,ret['code'])
			self.assertIsNotNone(User.query.get(ret['data']['userid']))

	def test_register_with_name(self):
		with self.app.app_context():
			ret = self.client.post('/user/register',headers={
				'x-wx-source':'test',
				'x-wx-openid':'114514'
				},json={
				'username':'田所浩二'*20
				})
			ret = json.loads(ret.data.decode('utf-8'))
			self.assertEqual(0,ret['code'])
			self.assertIsNotNone(User.query.get(ret['data']['userid']))
			self.assertEqual('田所浩二'*20,User.query.get(ret['data']['userid']).username)

	def test_register_with_too_long_name(self):
		with self.app.app_context():
			ret = self.client.post('/user/register',headers={
				'x-wx-source':'test',
				'x-wx-openid':'114514'
				},json={
				'username':'田所浩二'*27
				})
			#print(ret.data)
			self.assertEqual(400,ret.status_code)
			ret = json.loads(ret.data.decode('utf-8'))
			self.assertIsNone(User.query.first())
	

