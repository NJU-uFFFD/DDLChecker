from dataclasses import dataclass
from db import db


@dataclass
class Course(db.Model):
    course_name: str
    course_uuid: str
    platform_uuid: str
    creator_id: int
    course_uuid = db.Column(db.String(64), primary_key=True)
    course_name = db.Column(db.String(512))
    platform_uuid = db.Column(db.String(64))
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    ddls = db.relationship('Ddl', backref='course', lazy='dynamic')
    source_ddls = db.relationship('SourceDdl', backref='course', lazy='dynamic')
    subscriptions = db.relationship('UserSubscriptions', backref='course', lazy='dynamic')

    def __init__(self, course_name, course_uuid, platform_uuid, creator_id=None):
        self.course_name = course_name
        self.course_uuid = course_uuid
        self.platform_uuid = platform_uuid
        self.creator_id = creator_id

    def to_dict(self):
        return {
            "course_name": self.course_name,
            "course_uuid": self.course_uuid,
            "platform_uuid": self.platform_uuid,
            "creator_id": self.creator_id
        }
