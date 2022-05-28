from marshmallow import Schema, fields, validate


class RegisterRules(Schema):
    """
        "username" -> str(len 1 - 100)
    """
    username = fields.Str(required=False, validate=validate.Length(min=1, max=100))



class RenameRules(Schema):
    """
        "username" -> str(len 1 - 100)
    """

    username = fields.Str(required=False, validate=validate.Length(min=1, max=100))