from marshmallow import Schema, fields
from product import schemas as product_schemas

class EntrySchema(Schema):
    id = fields.Int()
    quantity = fields.Int()
    datetime = fields.DateTime()
    local = fields.Str()
    product = fields.Nested(product_schemas.ProductSchema)
    _type = fields.Str(data_key="type")