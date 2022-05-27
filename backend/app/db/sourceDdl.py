from dataclasses import dataclass
from db import db


@dataclass
class SourceDdl(db.Model):
    id: int
    course_uuid: int
    platform_uuid: int
    title: str
    content: str
    tag: str
    ddl_time: int
    create_time: int
    id = db.Column(db.Integer, primary_key=True)
    course_uuid = db.Column(db.String(64), db.ForeignKey('course.course_uuid'))
    platform_uuid = db.Column(db.String(64))
    title = db.Column(db.String(256))
    content = db.Column(db.String(4096))
    tag = db.Column(db.String(4096))
    ddl_time = db.Column(db.BigInteger)
    create_time = db.Column(db.BigInteger)
    ddls = db.relationship('Ddl', backref='source_ddl', lazy='dynamic')

    def __init__(self, course_uuid, platform_uuid, title, content, tag, ddl_time, create_time):
        self.course_uuid = course_uuid
        self.platform_uuid = platform_uuid
        self.title = title
        self.content = content
        self.tag = tag
        self.ddl_time = ddl_time
        self.create_time = create_time

    def to_dict(self):
        return {
            "id": self.id,
            "course_uuid": self.course_uuid,
            "platform_uuid": self.platform_uuid,
            "title": self.title,
            "content": self.content,
            "tag": self.tag,
            "ddl_time": self.ddl_time,
            "create_time": self.create_time
        }
