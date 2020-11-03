from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
import json
import morph
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)

db_uri = os.environ.get('DATABASE_URL') or "postgresql://localhost/flash-reading-db"
app.config = ['SQLALCHEMY_DATABASE_URI'] = db_uri
db = SQLAlchemy(app)

class tDocuments(db.Model):
    __tablename__ = 't_documents'
    uuid = db.Column(db.String(36), primary_key=True)
    content = db.Column(db.Text, primary_key=False)
    split_uuid = db.Column(db.String(36), primary_key=False)
    created_at = db.Column(db.DateTime(), primary_key=True)
    updated_at = db.Column(db.DateTime(), primary_key=True)

class tSplitUnits(db.Model):
    __tablename__ = 't_split_units'
    uuid = db.Column(db.String(36), primary_key=True)
    index = db.Column(db,Integer, primary_key=False)
    content = db.Column(db.Text, primary_key=False)

@app.route('/')
def home():
    return render_template('home.html', baseUrl=request.base_url) 

@app.route('/list')
def list():
    docs = tDocuments.query.all()

    for doc in docs:
        print(doc)

        units = tSplitUnits
            .query
            .get(doc.split_uuid)
            .order_by(tSplitUnits.index)

        print(units)
        
        doc.units = units

    return render_template('list.html', baseUrl=request.base_url, docList=doc) 

@app.route('/read')
def read():
    return render_template('index.html', baseUrl=request.base_url)

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

#おまじない
if __name__ == '__main__':
    app.run(debug=True)
