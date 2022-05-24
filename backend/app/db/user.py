from db import db
from dataclasses import dataclass


@dataclass
class User(db.Model):
    id: int
    openid: str
    username: str
    id = db.Column(db.Integer, primary_key=True)
    openid = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(100))
    ddls = db.relationship('Ddl', backref='user', lazy='dynamic')
    accounts = db.relationship('Account', backref='user', lazy='dynamic')
    subs = db.relationship('UserSubscriptions', backref='user', lazy='dynamic')

    def __init__(self, openid, username):
        self.username = username
        self.openid = openid
