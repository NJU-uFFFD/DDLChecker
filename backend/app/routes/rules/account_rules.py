from marshmallow import Schema, fields


class AddAccountRules(Schema):
    """
        platform_uuid: str(len=64)
        fields: dict
    """
    platform_uuid = fields.Str(required=True)
    fields = fields.Dict(required=True, keys=fields.Str(required=True), values=fields.Str(required=True))
