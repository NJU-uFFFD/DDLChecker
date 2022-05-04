from db import db

class Ddl(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	userid = db.Column(db.Integer, db.ForeignKey('user.id'))
	title = db.Column(db.String(256))
	content = db.Column(db.String(4096))
	tag = db.Column(db.String(4096))
	source = db.Column(db.Integer)
	ddl_time = db.Column(db.BigInteger)
	is_completed = db.Column(db.Boolean)

	def __init__(self, userid, title, ddl_time, content='', tag='[]', source=1, is_completed=False):
		self.userid = userid
		self.title = title
		self.content = content
		self.tag = tag
		self.source = source
		self.ddl_time = ddl_time
		self.is_completed = is_completed

