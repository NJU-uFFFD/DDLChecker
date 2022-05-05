from marshmallow import Schema, fields, validate


class RegisterRules(Schema):
    """
    "username" -> str(len 1 - 100)
    """
    username = fields.Str(required=True, validate=validate.Length(min=1, max=100))
