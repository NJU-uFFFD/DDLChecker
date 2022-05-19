from dataclasses import dataclass
from db import db


@dataclass
class Ddl(db.Model):
    id: int
    userid: int
    title: str
    content: str
    tag: str
    course_uuid: str
    ddl_time: int
    is_completed: bool
    source_uuid: str
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(256))
    content = db.Column(db.String(4096))
    tag = db.Column(db.String(4096))
    course_uuid = db.Column(db.String(64))
    ddl_time = db.Column(db.BigInteger)
    source_uuid = db.Column(db.String(64))
    is_completed = db.Column(db.Boolean)

    def __init__(self, userid, title, ddl_time, content, tag, course_uuid, source_uuid, is_completed=False):
        self.userid = userid
        self.title = title
        self.content = content
        self.tag = tag
        self.course_uuid = course_uuid
        self.ddl_time = ddl_time
        self.source_uuid = source_uuid
        self.is_completed = is_completed
