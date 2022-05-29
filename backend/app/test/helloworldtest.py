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
			self.assertIsNotNone(User.query.get(json.loads(ret.data.decode('utf-8'))['data']['userid']))
