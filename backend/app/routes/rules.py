import time
from marshmallow import Schema, fields, ValidationError, validate
from routes.utils import make_response
from flask import abort


def is_integer(x):
    if x != int(x):
        raise ValidationError("Not a valid integer")


class DeleteDDLRules:
    """
        "ddl_id" -> int(>=0)
    """
    title = fields.Float(required=True, validate=[validate.Range(min=0), is_integer])


class ListDDLsRules(Schema):
    """
        "start" -> int(>=0)
        "end" -> int(>=0)
        "filter" -> dict
            "is_completed" -> int(0, 1)
            "is_overtime" -> int(0, 1)
            "by_course" -> int(0, 1)
            "by_tag" -> int(0, 1)
    """
    start = fields.Float(required=True, validate=[validate.Range(min=0), is_integer])
    end = fields.Float(required=True, validate=[validate.Range(min=0), is_integer])
    filter = fields.Dict(required=True,
                         keys=fields.Str(required=True,
                                         validate=validate.OneOf(["is_completed", "is_overtime", "by_course", "by_tag"])),
                         values=fields.Float(required=True, validate=[validate.Range(min=0, max=1), is_integer]))


class AddDDLRules(Schema):
    """
        "title" -> str (len 1 - 128)
        "content" -> str (len 1 - 256)(not necessary)
        "ddl_time" -> int(不得在30天前)
        "tag" -> str(not necessary)
        "course_uuid" -> uuid(not necessary)
    """
    title = fields.Str(required=True, validate=validate.Length(min=1, max=128))
    content = fields.Str(validate=validate.Length(min=1, max=256))
    ddl_time = fields.Float(required=True,
                            validate=[validate.Range(min=round(time.time() * 1000) - 2_592_000_000), is_integer])
    tag = fields.Str(validate=validate.Length(min=1, max=256))
    course_uuid = fields.UUID()


def check_data(schema, data):
    """
    json输入格式校验
    :param schema: 校验规则
    :param data: 校验数据
    :return:若校验失败，abort并返回错误
    """
    try:
        return schema().load(data)
    except ValidationError as e:
        abort(make_response(status=-1, msg=str(e.messages), return_data={}), 400)
