import time

from marshmallow import Schema, fields, ValidationError, validate
from routes.utils import make_response
from flask import abort


class AddDDLRules(Schema):
    title = fields.Str(required=True, validate=validate.Length(min=1, max=128))
    content = fields.Str(required=True, validate=validate.Length(min=1, max=256))
    ddl_time = fields.Int(required=True, validate=validate.Range(min=round(time.time() * 1000) - 2_592_000_000))
    tag = fields.Str(required=True, validate=validate.Length(min=1, max=256))
    course = fields.UUID(required=True)


def check_data(schema, data):
    try:
        return schema().load(data)
    except ValidationError as e:
        abort(make_response(status=-1, msg=str(e.messages), data={}), 400)
