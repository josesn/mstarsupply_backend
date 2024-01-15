from marshmallow import Schema, fields

class ProductTypeSchema(Schema):
    id = fields.Int()
    name = fields.Str()

class ManufacturerSchema(Schema):
    id = fields.Int()
    name = fields.Str()

class ProductSchema(Schema):
    name = fields.Str()
    number_register = fields.Int()
    manufacturer = fields.Nested(ManufacturerSchema)
    _type = fields.Nested(ProductTypeSchema)
    description = fields.Str()