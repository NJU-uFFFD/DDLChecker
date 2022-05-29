import time
from marshmallow import Schema, fields, validate


class ListDDLsRules(Schema):
    """
        "page" -> int
        "size" -> int
        "filter" -> dict(not necessary)
            "is_completed" -> bool
            "is_overtime" -> bool
        "ddl_time_range" -> dict(not necessary)
            "start" -> int
            "end" -> int
        "create_time_range" -> dict(not necessary)
            "start" -> int
            "end" -> int
        "complete_time_range" -> dict(not necessary)
            "start" -> int
            "end" -> int
        "tag" -> str(not necessary)
        "sorter" -> dict(not necessary)
            "reversed" -> bool
    """
    page = fields.Integer(strict=True, required=True, validate=[validate.Range(min=1)])
    size = fields.Integer(strict=True, required=True, validate=[validate.Range(min=1, max=50)])
    filter = fields.Dict(required=False,
                         keys=fields.Str(required=True, validate=validate.OneOf(["is_completed", "is_overtime"])),
                         values=fields.Boolean(required=True))
    ddl_time_range = fields.Dict(required=False,
                             keys=fields.Str(required=True, validate=validate.OneOf(["start", "end"])),
                             values=fields.Integer(strict=True, required=True, validate=validate.Range(min=0)))
    create_time_range = fields.Dict(required=False,
                                 keys=fields.Str(required=True, validate=validate.OneOf(["start", "end"])),
                                 values=fields.Integer(strict=True, required=True, validate=validate.Range(min=0)))
    complete_time_range = fields.Dict(required=False,
                                    keys=fields.Str(required=True, validate=validate.OneOf(["start", "end"])),
                                    values=fields.Integer(strict=True, required=True, validate=validate.Range(min=0)))
    tag = fields.Str(required=False, validate=validate.Length(min=1, max=4096))
    sorter = fields.Dict(required=False,
                         keys=fields.Str(required=True, validate=validate.OneOf(["reversed"])),
                         values=fields.Boolean(required=True))


class AddDDLRules(Schema):
    """
        "title" -> str (len 1 - 256)
        "content" -> str (len 1 - 4096)(not necessary)
        "ddl_time" -> int(不得在30天前)
        "tag" -> str(len 1 - 4096)(not necessary)
        "course_uuid" -> str(not necessary)
        "platform_uuid" -> str(not necessary)
        "source_ddl_id" -> int(not necessary)
    """
    title = fields.Str(required=True, validate=validate.Length(min=1, max=256))
    content = fields.Str(required=True, validate=validate.Length(min=1, max=4096))
    ddl_time = fields.Integer(strict=True, required=True,
                              validate=validate.Range(min=round(time.time() * 1000) - 2_592_000_000))
    tag = fields.Str(required=False, validate=validate.Length(min=1, max=4096))
    course_uuid = fields.UUID(required=False)
    platform_uuid = fields.UUID(required=False)
    source_ddl_id = fields.Integer(required=False, validate=validate.Range(min=1))


class UpdateDDLRules(Schema):
    """
        "id" -> int(>=0)
        "title" -> str (len 1 - 256)(not necessary)
        "content" -> str (len 1 - 4096)(not necessary)
        "ddl_time" -> int(不得在30天前)(not necessary)
        "tag" -> str(len 1 - 4096)(not necessary)
        "course_uuid" -> str(not necessary)
        "platform_uuid" -> str(not necessary)
        "is_completed" -> bool(not necessary)
        "is_deleted" ->bool(not necessary)
    """
    id = fields.Integer(strict=True, required=True, validate=[validate.Range(min=0)])
    title = fields.Str(required=False, validate=validate.Length(min=1, max=256))
    content = fields.Str(required=False, validate=validate.Length(min=1, max=4096))
    ddl_time = fields.Integer(strict=True, required=False,
                              validate=validate.Range(min=round(time.time() * 1000) - 2_592_000_000))
    tag = fields.Str(required=False, validate=validate.Length(min=1, max=4096))
    course_uuid = fields.UUID(required=False)
    platform_uuid = fields.UUID(required=False)
    is_completed = fields.Boolean(required=False)
    is_deleted = fields.Boolean(required=False)
