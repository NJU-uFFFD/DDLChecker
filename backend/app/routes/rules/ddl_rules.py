import time
from marshmallow import Schema, fields, validate


class DeleteDDLRules(Schema):
    """
        "ddl_id" -> int(>=0)
    """
    ddl_id = fields.Integer(strict=True, required=True, validate=[validate.Range(min=0)])


class ListDDLsRules(Schema):
    """
        "start" -> int(>=0)
        "end" -> int(>=0)
        "filter" -> dict
            "is_completed" -> bool
            "is_overtime" -> bool
    """
    start = fields.Integer(strict=True, required=True, validate=[validate.Range(min=0)])
    end = fields.Integer(strict=True, required=True, validate=[validate.Range(min=0)])
    filter = fields.Dict(required=False,
                         keys=fields.Str(required=True,
                                         validate=validate.OneOf(["is_completed", "is_overtime"])),
                         values=fields.Boolean(required=True))


class AddDDLRules(Schema):
    """
        "title" -> str (len 1 - 256)
        "content" -> str (len 1 - 4096)(not necessary)
        "ddl_time" -> int(不得在30天前)
        "tag" -> str(len 1 - 4096)(not necessary)
        "course_uuid" -> str(not necessary)
        "source_uuid" -> str(not necessary)
    """
    title = fields.Str(required=True, validate=validate.Length(min=1, max=256))
    content = fields.Str(required=True, validate=validate.Length(min=1, max=4096))
    ddl_time = fields.Integer(strict=True, required=True, validate=[validate.Range(min=round(time.time() * 1000) - 2_592_000_000)])
    tag = fields.Str(required=False, validate=validate.Length(min=1, max=4096))
    course_uuid = fields.UUID(required=False)
    source = fields.UUID(required=False)

