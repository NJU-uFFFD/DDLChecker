from dataclasses import dataclass
from db import db


@dataclass
class Course(db.Model):
    course_name: str
    course_uuid: str
    platform_uuid: str
    course_uuid = db.Column(db.String(64), primary_key=True)
    course_name = db.Column(db.String(512))
    platform_uuid = db.Column(db.String(64))
    ddls = db.relationship('Ddl', backref='course', lazy='dynamic')
    source_ddls = db.relationship('SourceDdl', backref='course', lazy='dynamic')
    subscriptions = db.relationship('UserSubscriptions', backref='course', lazy='dynamic')


def __init__(self, course_name, course_uuid, platform_uuid):
    self.course_name = course_name
    self.course_uuid = course_uuid
    self.platform_uuid = platform_uuid

