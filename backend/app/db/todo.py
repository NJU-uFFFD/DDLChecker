from __init__ import db

class Todo(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	userid = db.Column(db.Integer, db.ForeignKey('user.id'))
	title = db.Column(db.String(256))
	content = db.Column(db.String(4096))
	tag = db.Column(db.String(4096))
	source = db.Column(db.Integer)
	ddl_time = db.Column(db.BigInteger)
	is_completed = db.Column(db.Boolean)
