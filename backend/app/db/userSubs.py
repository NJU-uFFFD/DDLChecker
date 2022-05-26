from dataclasses import dataclass
from db import db


@dataclass
class UserSubscriptions(db.Model):
    id: int
    userid: int
    course_uuid: str
    platform_uuid: str
    last_updated: int
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('user.id'))
    course_uuid = db.Column(db.String(64), db.ForeignKey('course.course_uuid'))
    platform_uuid = db.Column(db.String(64))
    last_updated = db.Column(db.BigInteger)

    def __init__(self, userid, course_uuid, platform_uuid, last_updated=0):
        self.userid = userid
        self.course_uuid = course_uuid
        self.platform_uuid = platform_uuid
        self.last_updated = last_updated




