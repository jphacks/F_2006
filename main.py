from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
import os
import json
from datetime import datetime
import uuid
import morph
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_marshmallow.fields import fields
import urllib.parse

app = Flask(__name__)
CORS(app)

db_uri = os.environ.get('DATABASE_URL') or "postgresql://admin:admin@localhost:5433/flash-reading-db"
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db = SQLAlchemy(app)

class tDocuments(db.Model):
    __tablename__ = 't_documents'
    uuid = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.Text, primary_key=False)
    content = db.Column(db.Text, primary_key=False)
    current_pos = db.Column(db.Integer, primary_key=False)
    created_at = db.Column(db.DateTime(), primary_key=True)
    updated_at = db.Column(db.DateTime(), primary_key=True)

    def __init__(self, uuid, name, content, current_pos):
        self.uuid = uuid
        self.name = name
        self.content = content
        now = datetime.now()
        self.created_at = now
        self.updated_at = now
        self.current_pos = current_pos

ma = Marshmallow(app)

class tDocumentsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = tDocuments
        load_instance = True
    
    created_at = fields.DateTime('%Y-%m-%dT%H:%M:%S+09:00')
    updated_at = fields.DateTime('%Y-%m-%dT%H:%M:%S+09:00')

class tSplitUnits(db.Model):
    __tablename__ = 't_split_units'
    uuid = db.Column(db.String(36), primary_key=True)
    doc_uuid = db.Column(db.String(36), primary_key=False)
    index = db.Column(db.Integer, primary_key=False)
    content = db.Column(db.Text, primary_key=False)

class tSplitUnitsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = tSplitUnits
        load_instance = True
    
@app.route('/')
def home():
    return render_template('home.html', baseUrl=request.base_url, docObj="{}") 

@app.route('/list')
def list():
    docs = db.session.query(tDocuments).all()

    print(docs)

    docObj = {}

    docObj['docs'] = docs

    return render_template('list.html', baseUrl=request.base_url, docList=docObj, docObj="{}") 

# uuid 既存の文書のみ
@app.route('/doc/<string:uuid>')
def doc(uuid):
    doc = db.session.\
                query(tDocuments).\
                filter(tDocuments.uuid==uuid).\
                first()

    print(doc)

    docJson = tDocumentsSchema().dump(doc)
    print(docJson)

    docObj = {}
    docObj['doc'] = docJson

    units = db.session.\
               query(tSplitUnits).\
               filter(tSplitUnits.doc_uuid == doc.uuid).\
               order_by(tSplitUnits.index).\
               all()
    
    unitsJson = tSplitUnitsSchema(many=True).dump(units)

    print(unitsJson)

    docObj['units'] = unitsJson

    return render_template('index.html', baseUrl=request.base_url, canInsert=False, docObj=docObj)

@app.route('/read')
def read():
    return render_template('index.html', baseUrl=request.base_url, canInsert=True, docObj="{}")

@app.route('/result', methods=["POST"])
def result():
    if request.headers['Content-Type'] != 'application/json':
        print(request.headers['Content-Type'])
        return jsonify(res='error'), 400

    data = request.json
    print(data)
    
    data = data['text']

    # ここで処理
    texts = morph.morph(data)

    data = {
        'text': texts
    }

    return jsonify(data)

# content, name, current_pos, split_units
@app.route('/insert', methods=["POST"])
def insert():
    if request.headers['Content-Type'] != 'application/json':
        print(request.headers['Content-Type'])
        return jsonify(res='error'), 400

    data = request.json
    print(data)

    docUuid = uuid.uuid4()

    doc = tDocuments(uuid=docUuid,content=data['content'], name=data['name'],current_pos=data['current_pos'])
    db.session.add(doc)

    idx = 0

    for unit in data['split_units']:
        unitUuid = uuid.uuid4()
        unitDoc = tSplitUnits(uuid=unitUuid, doc_uuid=docUuid, index=idx, content=unit)
        db.session.add(unitDoc)
        idx += 1

    db.session.commit()

    return jsonify(success=True)

# uuid, current_pos
@app.route('/update', methods=["POST"])
def update():
    if request.headers['Content-Type'] != 'application/json':
        print(request.headers['Content-Type'])
        return jsonify(res='error'), 400

    data = request.json
    print(data)

    doc = db.session.\
             query(tDocuments).\
             filter(tDocuments.uuid==data['uuid']).\
             first()
    doc.current_pos = data['current_pos']

    db.session.commit()
    
    return jsonify(success=True)

# uuid のみ
@app.route('/delete', methods=["POST"])
def delete():
    if request.headers['Content-Type'] != 'application/json':
        print(request.headers['Content-Type'])
        return jsonify(res='error'), 400

    data = request.json
    print(data)

    doc = db.session.\
             query(tDocuments).\
             filter(tDocuments.uuid==data['uuid']).\
             first()
    db.session.delete(doc)

    units = db.session.\
       query(tSplitUnits).\
       filter(tSplitUnits.doc_uuid==data['uuid']).\
       all()

    for unit in units:
        db.session.delete(unit)

    db.session.commit()
    
    return jsonify(success=True)

#おまじない
if __name__ == '__main__':
    app.run(debug=True)
