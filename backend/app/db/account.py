from db import db
from dataclasses import dataclass


@dataclass
class Account(db.Model):
    id: int
    userid: int
    platform_uuid: str
    fields: str

    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('user.id'))
    platform_uuid = db.Column(db.String(256))
    fields = db.Column(db.String(4096))

    def __init__(self, userid, platform_uuid, fields):
        self.userid = userid
        self.platform_uuid = platform_uuid
        self.fields = fields
