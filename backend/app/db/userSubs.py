from dataclasses import dataclass
from db import db


@dataclass
class UserSubscriptions(db.Model):
    id: int
    userid: int
    course_uuid: str
    platform_uuid: str
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('user.id'))
    course_uuid = db.Column(db.String(64))
    platform_uuid = db.Column(db.String(64))

    def __init__(self, userid, course_uuid, platform_uuid):
        self.userid = userid
        self.course_uuid = course_uuid
        self.platform_uuid = platform_uuid




