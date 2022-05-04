from db import db
from dataclasses import dataclass


@dataclass
class Ddl(db.Model):
	id: int
	userid: int
	title: str
	content: str
	tag: str
	course_uuid: str
	ddl_time: int
	is_completed: bool
	id = db.Column(db.Integer, primary_key=True)
	userid = db.Column(db.Integer, db.ForeignKey('user.id'))
	title = db.Column(db.String(256))
	content = db.Column(db.String(4096))
	tag = db.Column(db.String(4096))
	course_uuid = db.Column(db.String(64))
	ddl_time = db.Column(db.BigInteger)
	is_completed = db.Column(db.Boolean)

	def __init__(self, userid, title, ddl_time, content, tag, course_uuid, is_completed=False):
		self.userid = userid
		self.title = title
		self.content = content
		self.tag = tag
		self.course_uuid = course_uuid
		self.ddl_time = ddl_time
		self.is_completed = is_completed
