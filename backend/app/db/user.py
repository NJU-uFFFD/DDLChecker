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
    ddls = db.relationship('Ddl', backref='User', lazy='dynamic')
    accounts = db.relationship('Account', backref='User', lazy='dynamic')
    subscriptions = db.relationship('UserSubscriptions', backref='User', lazy='dynamic')

    def __init__(self, openid, username):
        self.username = username
        self.openid = openid
