# -*- coding: utf-8 -*-
from flask import Flask, request, render_template, jsonify, redirect, url_for
from flask_cors import CORS
import os
import json
from datetime import datetime
import uuid
import morph
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_marshmallow.fields import fields
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
import urllib.parse
from Cryptodome.Cipher import AES

app = Flask(__name__)
CORS(app)

db_uri = os.environ.get('DATABASE_URL') or "postgresql://admin:admin@localhost:5433/flash-reading-db"
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db = SQLAlchemy(app)

class tDocuments(db.Model):
    __tablename__ = 't_documents'
    uuid = db.Column(db.String(36), primary_key=True)
    user_uuid = db.Column(db.String(36), primary_key=False)
    name = db.Column(db.Text, primary_key=False)
    content = db.Column(db.Text, primary_key=False)
    current_pos = db.Column(db.Integer, primary_key=False)
    created_at = db.Column(db.DateTime(), primary_key=True)
    updated_at = db.Column(db.DateTime(), primary_key=True)

    def __init__(self, user_uuid, uuid, name, content, current_pos):
        self.uuid = uuid
        self.user_uuid = user_uuid
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
    
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

app.config['SECRET_KEY'] = "secret"

class tUsers(UserMixin, db.Model):
    __tablename__ = 't_users'
    id = db.Column(db.String(36), primary_key=True)
    user_name = db.Column(db.String(36), primary_key=False)
    password = db.Column(db.String(36), primary_key=False)

# キー設定関数
def create_key(KeyWord):
    key_size = 32
    KeySizeFill = KeyWord.zfill(key_size)
    Key = KeySizeFill[:key_size].encode('utf-8')

    return Key

# パスワードの暗号化関数
def encryptPassword(PassWord, KeyWord):
    iv = b"1234567890123456"
    Key = create_key(KeyWord)

    obj = AES.new(Key, AES.MODE_CFB, iv)
    ret_bytes = obj.encrypt(PassWord.encode(encoding='utf-8'))

    return ret_bytes

# パスワードの複合化関数
def decodePassword(Password, KeyWord):
    iv = b"1234567890123456"   # 初期化ベクトル設定
    key = create_key(KeyWord) # キー設定

    obj = AES.new(key, AES.MODE_CFB, iv)
    OPassword = obj.decrypt(PassWord.encode(encoding='utf-8')).decode('utf-8') #パスワードの複合化

    return OPassword

@login_manager.user_loader
def load_user(uuid):
    userDoc = db.session.\
                    query(tUsers).\
                    filter(tUsers.id==uuid).\
                    first()

    return userDoc

@app.route('/')
def home():
    return render_template('home.html', baseUrl=request.base_url, docObj="{}") 

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_name = request.form['user-name']
        plain_password = request.form['password']

        password = str(encryptPassword(plain_password, user_name))

        userDoc = db.session.\
            query(tUsers).\
            filter(tUsers.user_name==user_name).\
            filter(tUsers.password==password).\
            first()

        print(userDoc)

        if userDoc:
            login_user(userDoc)

            return redirect(url_for('home'))
        else:
            return jsonify(res='login error'), 400 
    else:
        return render_template('login.html', buttonName="Login", formName='ログイン', action="login", docObj="{}")           

@app.route('/logout')
@login_required
def logout():
    logout_user()

    return redirect(url_for('home'))    

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_name = request.form['user-name']
        password = request.form['password']

        password = str(encryptPassword(password, user_name))

        userDoc = db.session.\
            query(tUsers).\
            filter(tUsers.user_name==user_name).\
            first()

        if userDoc:
            return jsonify(res='register error (すでにユーザーが存在します)'), 400 

        userDoc = tUsers(id=uuid.uuid4(), user_name=user_name, password=password)

        db.session.add(userDoc)
        db.session.commit()

        return redirect(url_for('home'))
    else:
        return render_template('login.html', buttonName="Register", formName='ユーザー登録', action="register", docObj="{}")

@app.route('/list')
@login_required
def list():
    docs = db.session.\
                query(tDocuments).\
                filter(tDocuments.user_uuid == current_user.id).\
                all()

    print(docs)

    docsJson = tDocumentsSchema(many=True).dump(docs) 

    docList = docs

    docsObj = {}
    docsObj['docs'] = docsJson

    return render_template('list.html', baseUrl=request.base_url, docList=docList, docObj="{}", docsObj=docsObj) 

# uuid 既存の文書のみ
@app.route('/doc/<string:uuid>')
@login_required
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

    return render_template('index.html', baseUrl=request.base_url, canInsert=False, docObj=docObj, sentence="")

@app.route('/read')
def read():
    sentence = request.args.get('q')

    if not sentence:
        sentence = ""

    return render_template('index.html', baseUrl=request.base_url, canInsert=True, docObj="{}", sentence=sentence)

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

# required param: content, name, current_pos, split_units, user_uuid
@app.route('/insert', methods=["POST"])
@login_required
def insert():
    if request.headers['Content-Type'] != 'application/json':
        print(request.headers['Content-Type'])
        return jsonify(res='error'), 400

    data = request.json
    print(data)

    docUuid = uuid.uuid4()

    doc = tDocuments(uuid=docUuid, user_uuid=current_user.id, content=data['content'], name=data['name'], current_pos=data['current_pos'])
    db.session.add(doc)

    idx = 0

    for unit in data['split_units']:
        unitUuid = uuid.uuid4()
        unitDoc = tSplitUnits(uuid=unitUuid, doc_uuid=docUuid, index=idx, content=unit)
        db.session.add(unitDoc)
        idx += 1

    db.session.commit()

    return jsonify(success=True)

# required param: uuid, current_pos
@app.route('/update', methods=["POST"])
@login_required
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
    doc.updated_at = datetime.now()

    db.session.commit()
    
    return jsonify(success=True)

# required param: uuid のみ
@app.route('/delete', methods=["POST"])
@login_required
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
