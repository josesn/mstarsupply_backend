from flask import Blueprint
from flask import request

from mstarsupply_backend.database import db
from .models import Entry
from entry.schemas import EntrySchema

from sqlalchemy import select

bp_entry = Blueprint('entry', __name__ , url_prefix="/entry")

@bp_entry.route('/', methods=['GET'])
def entry_list():
    entries = Entry.query.all()
    if 'type' in request.args:
        entries = [e for e in entries if e._type == request.args['type']]

    schema = EntrySchema(many=True)
    result = schema.dump(entries)
    return result, 200

@bp_entry.route('/<int:id>', methods=['GET'])
def entry_get(id):
    entry = Entry.query.filter(Entry.id == id).one()
    schema = EntrySchema()
    result = schema.dump(entry)
    return result, 200

@bp_entry.route('/', methods=['POST'])
def entry_post():
    try:
        entry = Entry(
            **request.json
        )
        db.session.add(entry)
    except:
        db.session.rollback()
        raise
    else:
        db.session.commit()
    
    schema = EntrySchema()
    result = schema.dump(entry)

    return result, 201

@bp_entry.route('/<int:id>/', methods=['DELETE'])
def entry_delete(id):
    try:
        entry = Entry.query.filter(Entry.id == id).one()
        entry.delete()
    except:
        db.session.rollback()
    else:
        db.session.commit()

    return {}, 200

@bp_entry.route('/<int:id>/', methods=['PATCH'])
def entry_update(id):
    try:
        entry = Entry.query.filter(Entry.id == id).one()
        entry.name = request.json['name']
    except:
        db.session.rollback()
    else:
        db.session.commit()
    
    schema = EntrySchema()
    result = schema.dump(entry)

    return result, 201