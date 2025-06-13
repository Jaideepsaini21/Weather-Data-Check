#from flask import Flask, render_template, request, redirect, url_for

#import pymysql as sql

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login/")
def login():
    return render_template("login.html")

@app.route("/signup/")
def signup():
    return render_template("signup.html")

@app.route("/aftersignup/", methods = ['GET', 'POST']):
def aftersignup():
    if request.method == 'GET':
        return render_template("signup.html")
    
    else:
        fullname = request.form.get("name")
        phone = request.form.get("phone")
        email = request.form.get("email")
        passwrod = request.form.get("email")

#if __name__ == "__main__":
 #   app.run(debug=True)