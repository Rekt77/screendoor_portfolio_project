# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 20:18:20 2019

@author: Rekt77
"""

from flask import Flask, request, jsonify, render_template, session, redirect, url_for, escape, flash
from datetime import timedelta
import pymongo
import json

app = Flask(__name__)

# dead code
with open("jwt.json") as Json:
    app.secret_key = json.loads(Json.read())["secret"]


with open("mongoDB.json") as Json:
    user_doc = json.loads(Json.read())


mongoURL = str("mongodb://%s:%s%s"%(user_doc['MongoID'],user_doc['MongoPassword'],user_doc["MongoURL"]))

client = pymongo.MongoClient(mongoURL)
db = pymongo.database.Database(client, 'zoin')
users = pymongo.collection.Collection(db,'Users')
Books = pymongo.collection.Collection(db, 'Books')

@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=1)

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

@app.route('/')
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

        flash('Wrong ID or PW, You have to check your ID or PW.')
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