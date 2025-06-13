from flask import Flask, render_template, request, redirect, url_for
import pymysql as sql
from flask import session, make_response

app = Flask(__name__)

app.secret_key = "grrassolutionpvtlimited"

def db_connect():

    db = sql.connect(host="localhost", port=3306, user="root", database="grras")
    cursor = db.cursor()
    return db, cursor

def pass_validate(password: str):
    """
    this method will validate the password based on the conditions
        1. password should be atleast 8 char long.
        2. password should be contain atleast 1 lower char and 1 upper case char and 1 nummeric char , 1 special char.
    """

    if len(password) >= 8:
        lower = 0
        upper = 0
        number = 0
        special = 0

        for i in password:
            if i.islower():
                lower += 1

            elif i.isupper():
                upper += 1

            elif i.isnumeric():
                number += 1

            elif i in "~!@#$%^&*()_+":
                special += 1

        if lower >= 1 and upper >= 1 and number >= 1 and special >= 1:
            return True
        return False
    return False


@app.route("/")
def index():
    if session.get("islogin"):
        return render_template("afterlogin.html")
    return render_template("index.html")

@app.route("/login/")
def login():
    if session.get("islogin"):
        return render_template("afterlogin.html")
    return render_template("login.html")

@app.route("/signup/")
def signup():
    if session.get("islogin"):
        return render_template("afterlogin.html")
    return render_template("signup.html")

@app.route("/aftersignup/", methods=['GET', 'POST'])
def aftersignup():
    if request.method == 'GET':
        #return render_template("signup.html")
        return redirect(url_for("signup"))
    else:
        name = request.form.get("name")
        phone = request.form.get("phone")
        email = request.form.get("email")
        password = request.form.get("password")
        db, cursor = db_connect()

        cmd = f"select * from info where email = '{email}'"
        cursor.execute(cmd)

        data = cursor.fetchall()

        if data:
            msg = "email already exits..."
            return render_template("login.html", msg=msg)
        
        else:
            
            cmd = f"insert into info values('{name}', '{phone}', '{email}', '{password}');"
            cursor.execute(cmd)
            db.commit()
            db.close()
            msg = "Register successfully..."
            return render_template("login.html", msg=msg)
        

@app.route("/afterlogin/", methods=['GET', 'POST'])

def afterlogin():
    if request.method == 'GET':
        return redirect(url_for('login'))
    
    else:
        email = request.form.get("email")
        password = request.form.get("password")

        db, cursor = db_connect()
        cmd = f"select * from info where email = '{email}' " #and '{password}'"
        cursor.execute(cmd)
        data = cursor.fetchall()
        #db.close()

        if data:
            session['email'] = email
            session['password'] = password
            session['islogin'] = True
            return render_template("afterlogin.html")
        
        else:
            msg = "invalid email or password"

            return render_template("login.html", msg=msg)
        
@app.route("/logout/")
def logout():
    del session["email"]
    del session["islogin"]
    return render_template("login.html")

@app.route("/checkweather/")
def checkweather():
    return render_template("weather.html",msg=["","","","","","","","","","",""],t=["","","","","","","","","","",""])

@app.route("/check/", methods=['GET', 'POST'])
def check(): 
 city_name = request.args.get("city")
 
 import requests

 
 key = "e35e9e9cf136ac8f16d02c1247ba7933"
 
 
 url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={key}&units=metric"
 
 response = requests.get(url)
 
 data = response.json()
 
 city = data['name']
 temp = data['main']['temp']
 humidity = data['main']['humidity']
 pressure = data['main']['pressure']
 description = data['weather'][0]['description']
 return render_template('weather.html',msg=[city,temp,humidity,pressure,description],t=["Current temperature:","Humidity:","Pressure:","Weather:"])

@app.route('/information/')
def information():
    return render_template('infor.html',)

    
if __name__ == "__main__":
    app.run(debug=True, port=5001)  