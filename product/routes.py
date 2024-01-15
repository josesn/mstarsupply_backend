from flask import Flask
from flask import Blueprint
from flask import request

from mstarsupply_backend.database import db
from product.models import ProductType, Manufacturer, Product
from product.schemas import ProductTypeSchema, ProductSchema, ManufacturerSchema

from sqlalchemy import select

bp_product = Blueprint('product', __name__ , url_prefix="/product")

@bp_product.route('/type')
def type_list():
    all_types = ProductType.query.all()
    schema = ProductTypeSchema(many=True)
    result = schema.dump(all_types)
    return result, 200

@bp_product.route('/type/<int:id>')
def type_get(id):
    _type = ProductType.query.filter(ProductType.id == id).one()
    schema = ProductTypeSchema()
    result = schema.dump(_type)
    return result, 200

@bp_product.route('/type/create', methods=['POST'])
def type_post():
    try:
        _type = ProductType(
            **request.json
        )
        db.session.add(_type)
    except:
        db.session.rollback()
        raise
    else:
        db.session.commit()
    
    schema = ProductTypeSchema()
    result = schema.dump(_type)

    return result, 201

@bp_product.route('/type/delete/<int:id>')
def type_delete(id):
    try:
        _type = ProductType.query.filter(ProductType.id == id).one()
        _type.delete()
    except:
        db.session.rollback()
    else:
        db.session.commit()

    return {}, 200

@bp_product.route('/type/update/<int:id>/', methods=['PUT'])
def type_update(id):
    try:
        _type = ProductType.query.filter(ProductType.id == id).one()
        _type.name = request.json['name']
    except:
        db.session.rollback()
    else:
        db.session.commit()
    
    schema = ProductTypeSchema()
    result = schema.dump(_type)

    return result, 201

@bp_product.route('/manufacturer')
def manufacturer_list():
    manufacturers = Manufacturer.query.all()
    schema = ManufacturerSchema(many=True)
    result = schema.dump(manufacturers)
    return result, 200

@bp_product.route('/manufacturer/<int:id>')
def manufacturer_get(id):
    manufacturer = Manufacturer.query.filter(Manufacturer.id == id).one()
    schema = ManufacturerSchema()
    result = schema.dump(manufacturer)
    return result, 200

@bp_product.route('/manufacturer/create', methods=['POST'])
def manufacturer_post():
    try:
        manufacturer = Manufacturer(
            **request.json
        )
        db.session.add(manufacturer)
    except:
        db.session.rollback()
        raise
    else:
        db.session.commit()
    
    schema = ManufacturerSchema()
    result = schema.dump(manufacturer)

    return result, 201

@bp_product.route('/manufacturer/delete/<int:id>')
def manufacturer_delete(id):
    try:
        manufacturer = Manufacturer.query.filter(Manufacturer.id == id).one()
        manufacturer.delete()
    except:
        db.session.rollback()
    else:
        db.session.commit()

    return {}, 200

@bp_product.route('/manufacturer/update/<int:id>/', methods=['PUT'])
def manufacturer_update(id):
    try:
        manufacturer = Manufacturer.query.filter(Manufacturer.id == id).one()
        manufacturer.name = request.json['name']
    except:
        db.session.rollback()
    else:
        db.session.commit()
    
    schema = ManufacturerSchema()
    result = schema.dump(manufacturer)

    return result, 201
    
@bp_product.route('/')
def product_list():
    products = Product.query.all()
    schema = ProductSchema(many=True)
    result = schema.dump(products)
    return result, 200

@bp_product.route('/<int:id>')
def product_get(id):
    product = Product.query.filter(Product.id == id).one()
    schema = ProductSchema()
    result = schema.dump(product)
    return result, 200

@bp_product.route('/create', methods=['POST'])
def product_post():
    try:
        product = Product(
            **request.json
        )

        db.session.add(product)
    except:
        db.session.rollback()
        raise
    else:
        db.session.commit()
    
    schema = ProductSchema()
    result = schema.dump(product)

    return result, 201

@bp_product.route('/delete/<int:id>')
def product_delete(id):
    try:
        product = Product.query.filter(Product.id == id).one()
        product.delete()
    except:
        db.session.rollback()
    else:
        db.session.commit()

    return {}, 200

@bp_product.route('/update/<int:id>/', methods=['PATCH'])
def product_update(id):
    try:
        product = Product.query.filter(Product.id == id).one()
        if 'name' in request.json:
            product.name = request.json['name']
        if 'number_register' in request.json:
            product.number_register = request.json['number_register']
        if 'manufacturer' in request.json:
            manufacturer = Manufacturer.query.filter(Manufacturer.id == request.json['manufacturer']).one()
            product.manufacturer = manufacturer
        if 'type' in request.json:
            _type = ProductType.query.filter(ProductType.id == request.json['type']).one()
            product._type = _type
        if 'description' in request.json:
            product.description = request.json['description']
    except:
        db.session.rollback()
    else:
        db.session.commit()
    
    schema = ProductSchema()
    result = schema.dump(product)

    return result, 201
