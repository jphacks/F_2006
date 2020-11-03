from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
import os
import json
from datetime import datetime
import uuid
import morph
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)

db_uri = os.environ.get('DATABASE_URL') or "postgresql://admin:admin@localhost:5433/flash-reading-db"
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db = SQLAlchemy(app)

class tDocuments(db.Model):
    __tablename__ = 't_documents'
    uuid = db.Column(db.String(36), primary_key=True)
    content = db.Column(db.Text, primary_key=False)
    split_uuid = db.Column(db.String(36), primary_key=False)
    current_pos = db.Column(db.Integer, primary_key=False)
    created_at = db.Column(db.DateTime(), primary_key=True)
    updated_at = db.Column(db.DateTime(), primary_key=True)

    def __init__(self, uuid, content, split_uuid, current_pos):
        self.uuid = uuid
        self.content = content
        self.split_uuid = split_uuid
        now = datetime.now()
        self.created_at = now
        self.updated_at = now
        self.current_pos = current_pos

class tSplitUnits(db.Model):
    __tablename__ = 't_split_units'
    uuid = db.Column(db.String(36), primary_key=True)
    index = db.Column(db.Integer, primary_key=False)
    content = db.Column(db.Text, primary_key=False)

@app.route('/')
def home():
    return render_template('home.html', baseUrl=request.base_url) 

@app.route('/list')
def list():
    docs = db.session.query(tDocuments).query.all()

    docObj = {}
    docObj['doc'] = doc

    for doc in docs:
        print(doc)

        units = db.session.query(tSplitUnits).get(doc.split_uuid).order_by(tSplitUnits.index)

        print(units)
        
        docObj['units'] = units

    return render_template('list.html', baseUrl=request.base_url, docList=docObj) 

# uuid 空の場合: 新たな文書を読み込み可能, 空でない場合: 既存の文書のみ
@app.route('/read/<string:uuid>')
def read():
    if len(uuid) > 0:
        canInsert = True
            
        doc = db.session.query(tDocuments).filter(uuid=data.uuid).first()

        print(doc)

        docObj = {}
        docObj['doc'] = doc

        docObj['units'] = db.session.query(tSplitUnits).get(doc.split_uuid).order_by(tSplitUnits.index)
        print(docObj['units'])
    else:
        canInsert = False
        docObj = {}

    return render_template('index.html', baseUrl=request.base_url, canInsert=canInsert, doc=docObj)

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

# content, current_pos, split_units
@app.route('/insert', methods=["POST"])
def insert():
    if request.headers['Content-Type'] != 'application/json':
        print(request.headers['Content-Type'])
        return jsonify(res='error'), 400

    data = request.json
    print(data)

    split_uuid = uuid.uuid4()

    doc = tDocuments(uuid=uuid.uuid4(),content=data.content,split_uuid=split_uuid,current_pos=data.current_pos)
    db.session.add(doc)

    idx = 0

    for unit in data.split_units:
        unitDoc = tSplitUnits(uuid=uuid, index=idx, content=unit)
        db.session.add(unitDoc)
        idx += 1

    db.session.commit()

    return

# uuid, current_pos
@app.route('/update', methods=["POST"])
def update():
    if request.headers['Content-Type'] != 'application/json':
        print(request.headers['Content-Type'])
        return jsonify(res='error'), 400

    data = request.json
    print(data)

    doc = db.session.query(tDocuments).filter(uuid=data.uuid).first()
    doc.current_pos = data.current_pos

    db.session.commit()
    
    return

# uuid のみ
@app.route('/delete', methods=["POST"])
def delete():
    if request.headers['Content-Type'] != 'application/json':
        print(request.headers['Content-Type'])
        return jsonify(res='error'), 400

    data = request.json
    print(data)

    doc = db.session.query(tDocuments).filter(uuid=data.uuid).first()
    db.session.delete(doc)

    db.session.commit()
    
    return

#おまじない
if __name__ == '__main__':
    app.run(debug=True)
