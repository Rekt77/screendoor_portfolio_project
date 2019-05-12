# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 20:18:20 2019

@author: Rekt77
"""

from flask import Flask, request, jsonify, render_template, session, redirect, url_for, escape, flash
from functools import wraps
import jwt
import requests
import pymongo
import json

app = Flask(__name__)
with open("jwt.json") as Json:
    app.secret_key = json.loads(Json.read())["secret"]

with open("mongoDB.json") as Json:
    user_doc = json.loads(Json.read())


mongoURL = str("mongodb://%s:%s%s"%(user_doc['MongoID'],user_doc['MongoPassword'],user_doc["MongoURL"]))

client = pymongo.MongoClient(mongoURL)
db = pymongo.database.Database(client, 'zoin')
users = pymongo.collection.Collection(db,'Users')
Books = pymongo.collection.Collection(db, 'Books')


def jwt_token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not 'Authorization' in request.headers:
            return jsonify({
                    "message":"token is not given"
                    }),400
        token = request.headers['Authorization']
        try:
            decoded_token = jwt.decode(token,secret_key,algorithms=['HS256'])
        except:
            return jsonify({
                    "message":"invalid token given"
                    }), 400
        kwargs['decoded_token'] = decoded_token
        return f(*args, **kwargs)
    return decorated_function

@app.route('/userSignup', methods = ['POST'])
def userSignup():
    try:
        reqJson = request.get_json()#json 데이터를 받아옴
        doc = {"userEmail":reqJson["userEmail"]}
        if users.find_one(doc) is None:
            users.insert_one({"userEmail":reqJson["userEmail"],"userPassword":reqJson["userPassword"]})
            return jsonify({"status":200,"message":"Signup success"})
        else:
            return jsonify({"status":401,"message":"Email already Exists."})
    
    except:
        return jsonify({"status":403,"message":"Unknown JSON"})


@app.route('/userDelete', methods = ['POST'])
@jwt_token_required
def userDelete():
    try:
        reqJson = request.get_json()#json 데이터를 받아옴
        doc = {"userEmail":reqJson["userEmail"],"userPassword":reqJson["userPassword"]}
        if not users.find_one(doc) is None:
            users.delete_one(doc)
            return jsonify({"status":200,"message":"Delete success"})
        else:
            return jsonify({"status":401,"message":"No Authentication"})
    except:
        return jsonify({"status":403,"message":"Unknown JSON"})

@app.route('/userSignin', methods = ['POST'])
def userSignin():
    reqJson = request.get_json()#json 데이터를 받아옴
    doc = {"userEmail":reqJson["userEmail"],"userPassword":reqJson["userPassword"]}
    try:
        if not users.find_one(doc) is None:
            try:
                res = requests.get("http://localhost:5001/get_token")
                res_json = res.get_json()
                return jsonify({"status":200,"message":"login Success","token":res_json["token"]})
            except:
                return jsonify({"status":500,"message":"internal server error"})

        else:
            return jsonify({"status":401,"message":"login Failure"})
    except:
        return jsonify({"status":403,"message":"login Failed"})

@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method == 'GET':
        if 'userEmail' in session:
            return render_template('welcome.html', info=session['userEmail'])
        return render_template('signup.html')
        
    if request.method == 'POST':
        if 'userEmail' in session:
            return render_template('welcome.html', info=session['userEmail'])

        users.insert_one(request.form.to_dict(flat='true'))
        session['userEmail'] = request.form['userEmail']
        return render_template('welcome.html', info=session['userEmail'])

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        if 'userEmail' in session:
            return render_template('welcome.html', info=session['userEmail'])
        return render_template('login.html')
        
    if request.method == 'POST':
        if 'userEmail' in session:
            return render_template('welcome.html', info=session['userEmail'])

        if users.find_one(request.form.to_dict(flat='true')) is not None:
            session['userEmail'] = request.form['userEmail']
            return render_template('welcome.html', info=session['userEmail'])
        flash('You have to logged in')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    if 'userEmail' in session:
        session.pop('userEmail')
        return redirect(url_for('login'))
    flash('You have to logged in')
    return redirect(url_for('login'))

@app.route('/register')
def register():
    if 'userEmail' in session:
            return render_template('register.html')
    flash('You have to logged in')
    return redirect(url_for('login'))
    
    
@app.route('/books',methods=['GET', 'POST'])
def books():
    if request.method == 'GET':
        if 'userEmail' in session:
            cursor = Books.find({})
            return render_template('books.html', books=cursor)
        flash('You have to logged in')
        return redirect(url_for('login'))
    
    elif request.method == 'POST':
        if 'userEmail' in session:
            Books.insert_one(request.form.to_dict(flat=True))
            cursor = Books.find({})
            return render_template('books.html', books=cursor)
        flash('You have to logged in')
        return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)