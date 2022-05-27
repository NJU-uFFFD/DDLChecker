import time

from marshmallow import Schema, fields, validate


class AddCourseRulesForCommunity(Schema):
    """
        course_name: str
        platform_uuid: str
    """
    course_name = fields.String(required=True, validate=validate.Length(min=1, max=512))
    platform_uuid = fields.UUID(required=True)


class AddDDLRulesForCommunity(Schema):
    """
        "course_uuid" -> str
        "platform_uuid" -> str
        "title" -> str
        "content" -> str
        "tag" -> str
        "ddl_time" -> int
    """
    course_uuid = fields.UUID(required=True)
    platform_uuid = fields.UUID(required=True)
    title = fields.String(required=True, validate=validate.Length(min=1, max=256))
    content = fields.String(required=True, validate=validate.Length(min=1, max=4096))
    tag = fields.String(required=True, validate=validate.Length(min=1, max=4096))
    ddl_time = fields.Integer(strict=True, required=True,
                             validate=validate.Range(min=round(time.time() * 1000) - 2_592_000_000))


class SubscribeCourseRules(Schema):
    """
        course_uuid -> str
    """
    course_uuid = fields.UUID(required=True)


class FetchDDLRule(Schema):
    """
        "id" -> int
    """
    id = fields.Integer(required=True, strict=True, validate=validate.Range(min=1))

