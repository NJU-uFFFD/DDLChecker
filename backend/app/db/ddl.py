from dataclasses import dataclass

from torch import unique

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
    create_time: int
    is_completed: bool
    complete_time: int
    is_deleted: bool
    delete_time: int
    platform_uuid: str
    source_ddl_id: str
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(256))
    content = db.Column(db.String(4096))
    tag = db.Column(db.String(4096))
    course_uuid = db.Column(db.String(64))
    ddl_time = db.Column(db.BigInteger)
    create_time = db.Column(db.BigInteger)
    platform_uuid = db.Column(db.String(64))
    is_completed = db.Column(db.Boolean)
    is_deleted = db.Column(db.Boolean)
    delete_time = db.Column(db.BigInteger)
    complete_time = db.Column(db.BigInteger)
    source_ddl_id = db.Column(db.String(64))

    def __init__(self, userid, title, ddl_time, create_time, content, tag, course_uuid, platform_uuid,
                 source_ddl_id=None, complete_time=None, delete_time=None, is_completed=False, is_deleted=False):
        self.userid = userid
        self.title = title
        self.content = content
        self.tag = tag
        self.course_uuid = course_uuid
        self.ddl_time = ddl_time
        self.create_time = create_time
        self.platform_uuid = platform_uuid
        self.is_completed = is_completed
        self.is_deleted = is_deleted
        self.complete_time = complete_time
        self.delete_time = delete_time
        self.source_ddl_id = source_ddl_id
