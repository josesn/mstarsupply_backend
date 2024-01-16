from marshmallow import Schema, fields
from product import schemas as product_schemas

class EntrySchemaCreate(Schema):
    id = fields.Int()
    quantity = fields.Int()
    datetime = fields.DateTime(dump_only=True)
    local = fields.Str()
    product = fields.Nested(product_schemas.ProductSchema, only=('id', 'name'))
    _type = fields.Str(data_key="type")

class EntrySchema(Schema):
    id = fields.Int()
    quantity = fields.Int()
    datetime = fields.DateTime(dump_only=True)
    local = fields.Str()
    product = fields.Nested(product_schemas.ProductSchema, only=('id', 'name'))
    _type = fields.Str(data_key="type")