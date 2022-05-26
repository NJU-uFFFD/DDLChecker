from marshmallow import Schema, fields, validate


class AddAccountRules(Schema):
    """
        platform_uuid: str(len=64)
        fields: dict
    """
    platform_uuid = fields.UUID(required=False)
    fields = fields.Dict(required=False, keys=fields.Str(required=True), values=fields.Str(required=True))


class DeleteAccountRules(Schema):
    """
        id: int
    """
    id = fields.Int(required=True, validate=validate.Range(min=1))
