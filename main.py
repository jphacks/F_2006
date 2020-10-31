from flask import Flask, request, render_template, jsonify
import json
app = Flask(__name__)
 
@app.route('/')
def hello_world():
    return render_template("main.html")

@app.route('/result', methods=[POST"])
def result():
    #if request.headers['Content-Type'] != 'application/json':
     #   print(request.headers['Content-Type'])
      #  return jsonify(res='error'), 400
    data = request.json
    print(data)
    
    data = data.text

    # ここで処理
    data = [data]

    data = {
        text: data
    }

    return jsonify(data)

#おまじない
if __name__ == '__main__':
    app.run()