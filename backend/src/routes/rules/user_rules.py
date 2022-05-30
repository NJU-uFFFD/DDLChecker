from marshmallow import Schema, fields, validate


class RegisterRules(Schema):
    """
        "username" -> str(len 1 - 100)
    """
    username = fields.Str(required=False, validate=validate.Length(min=1, max=100))


class ChangeProfileRules(Schema):
    """
        "username" -> str(len 1 - 100)
        "avatar" -> int(1 - 10)
    """

    username = fields.Str(required=False, validate=validate.Length(min=1, max=100))
    avatar = fields.Integer(required=False, strict=True, validate=validate.Range(min=1, max=10))


class UsernameRules(Schema):
    """
        "id" -> int
    """

    id = fields.Integer(required=True, validate=validate.Range(min=1))



