from flask import Flask, request, render_template
app = Flask(__name__)
 
@app.route('/')
def hello_world():
    return render_template("main.html")

@app.route('/result', methods=["POST"])
def result():
    text=request.form["input-text"]
    return render_template("result.html",text=text)
 
#おまじない
if __name__ == '__main__':
    app.run()
