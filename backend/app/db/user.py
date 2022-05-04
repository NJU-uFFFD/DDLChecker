from __init__ import db

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	openid = db.Column(db.String(150), unique=True)
	username = db.Column(db.String(100))