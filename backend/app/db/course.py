from dataclasses import dataclass
from db import db


@dataclass
class Course(db.Model):
    course_uuid: str
    platform_uuid: str
    course_uuid = db.Column(db.String(64), primary_key=True)
    platform_uuid = db.Column(db.String(64))
    ddls = db.relationship('Ddl', backref='Course', lazy='dynamic')
    source_ddls = db.relationship('SourceDdl', backref='Course', lazy='dynamic')
    subscriptions = db.relationship('UserSubscriptions', backref='Course', lazy='dynamic')

def __init__(self, course_uuid, platform_uuid):
    self.course_uuid = course_uuid
    self.platform_uuid = platform_uuid
