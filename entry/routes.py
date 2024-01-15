from flask import Blueprint
from flask import request
from flask import make_response
from flask.helpers import send_file, url_for
from mstarsupply_backend.database import db
from .models import Entry
from entry.schemas import EntrySchema
from report.utils import GeneratePDF

from sqlalchemy import select

bp_entry = Blueprint('entry', __name__ , url_prefix="/entry")

@bp_entry.route('/report', methods=['GET'])
def entry_report():
    list_values = []
    entries = Entry.query.all()
    if 'type' in request.args:
        entries = [e for e in entries if e._type == request.args['type']]
        
    list_keys = ('Total', 'Produto', 'Tipo', 'Local', 'Data', "Hora")
    try:
        for q in entries:
            fields = (
                {'value': q.quantity, 'prefix': "", 'suffix': "", 'custom_format': {'pdf': '', 'xlsx': ''}},
                {'value': q.datetime.date(), 'prefix': "", 'suffix': "", 'custom_format': {'pdf': '', 'xlsx': ''}},
                {'value': q.datetime.time(), 'prefix': "", 'suffix': "", 'custom_format': {'pdf': '', 'xlsx': ''}},
                {'value': q.local, 'prefix': "", 'suffix': "", 'custom_format': {'pdf': '', 'xlsx': ''}},
                {'value': q.product.name if q.product else None, 'prefix': "", 'suffix': "", 
                 'custom_format': {'pdf': '', 'xlsx': ''}},
                {'value': q._type, 'prefix': "", 'suffix': "", 'custom_format': {'pdf': '', 'xlsx': ''}},
            )
            list_values.append(fields)
    except Exception as e:
        return "<p>ERROR</p>"
    
    pdf_generator = GeneratePDF('Entradas e saidas', list_keys, list_values)
    pdf_generator.prepare_report_pdf()
    pdf = pdf_generator.generate_template()
    return send_file(pdf, as_attachment=True, mimetype='application/pdf',
        download_name='entry_report.pdf', max_age=0)

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