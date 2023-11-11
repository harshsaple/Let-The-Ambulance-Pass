from flask import Flask, render_template, request
import requests
app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def home():
    start = request.form.get('start_point')
    end = request.form.get('end_point')
    print(start,end)
    return render_template("home.html")

@app.route('/json_string', methods=["GET","POST"])
def json_demo():
    d = {
        "data":"this is some data",
        "start Point" : "-122345678",
        "end Point" :"+0987654"
    }
    return d

if __name__ == '__main__':
    app.run(debug=True)