from marshmallow import Schema, fields, validate


class AddAccountRules(Schema):
    """
        platform_uuid: str(len=64)
        fields: dict
    """
    platform_uuid = fields.UUID(required=False)
    fields = fields.Dict(required=False, keys=fields.Str(required=True), values=fields.Str(required=True))


class UpdateAccountRules(Schema):
    """
        id: int
        delete_account: bool
        fields: dict
    """
    id = fields.Int(required=True, validate=validate.Range(min=1))
    delete_account = fields.Boolean(required=False)
    fields = fields.Dict(required=False, keys=fields.Str(required=True), values=fields.Str(required=True))
