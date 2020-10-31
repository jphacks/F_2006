from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
import json
app = Flask(__name__)
CORS(app)
 
@app.route('/result', methods=["POST"])
def result():
    #if request.headers['Content-Type'] != 'application/json':
     #   print(request.headers['Content-Type'])
      #  return jsonify(res='error'), 400
    data = request.json
    print(data)
    
    data = data['text']

    # ここで処理

    data = [data]

    data = {
        'text': data
    }

    return jsonify(data)

#おまじない
if __name__ == '__main__':
    app.run()
