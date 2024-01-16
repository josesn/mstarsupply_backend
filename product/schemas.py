from marshmallow import Schema, fields, validate

class ProductTypeSchema(Schema):
    id = fields.Int()
    name = fields.Str()

class ProductTypeSchemaCreate(Schema):
    name = fields.Str(required=True, validate=[validate.Length(max=30)])

class ManufacturerSchema(Schema):
    id = fields.Int()
    name = fields.Str()

class ManufacturerSchemaCreate(Schema):
    name = fields.Str(required=True, validate=[validate.Length(max=30)])

class ProductSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    number_register = fields.Int()
    manufacturer = fields.Nested(ManufacturerSchema)
    _type = fields.Nested(ProductTypeSchema, data_key="type")
    description = fields.Str()

class ProductSchemaCreate(Schema):
    name = fields.Str(required=True, validate=[validate.Length(max=50)])
    number_register = fields.Int(required=True)
    manufacturer = fields.Nested(ManufacturerSchema)
    _type = fields.Nested(ProductTypeSchema, data_key="type")
    description = fields.Str(required=True)