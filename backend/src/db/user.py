from db import db
from dataclasses import dataclass
import random


@dataclass
class User(db.Model):
    id: int
    openid: str
    username: str
    account_add_times: int
    avatar: int
    last_login: int
    id = db.Column(db.Integer, primary_key=True)
    openid = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(100))
    account_add_times = db.Column(db.Integer)
    avatar = db.Column(db.Integer)
    last_login = db.Column(db.BigInteger)
    source_course_created = db.relationship("Course", backref="creator", lazy="dynamic")
    source_ddls_created = db.relationship("SourceDdl", backref="creator", lazy='dynamic')
    ddls = db.relationship('Ddl', backref='user', lazy='dynamic')
    accounts = db.relationship('Account', backref='user', lazy='dynamic')
    subscriptions = db.relationship('UserSubscriptions', backref='user', lazy='dynamic')

    def __init__(self, openid, username, account_add_times=0):
        self.username = username
        self.openid = openid
        self.account_add_times = account_add_times
        self.avatar = random.randint(1, 30)
