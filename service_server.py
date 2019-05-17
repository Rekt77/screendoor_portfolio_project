# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 20:18:20 2019

@author: Rekt77
"""

from flask import Flask, request, jsonify, render_template, session, redirect, url_for, escape, flash
from datetime import timedelta
from db import connect_mongo, usersDAO, booksDAO
import json

app = Flask(__name__)

with open("jwt.json") as Json:
    app.secret_key = json.loads(Json.read())["secret"]

db_connection = connect_mongo.ConnectDB().db
users = usersDAO.Users(db_connection)
books = booksDAO.Books(db_connection)

@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=20)
    print("before!")

@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method == 'GET':
        if 'userEmail' in session:
            return render_template('welcome.html', info=session['userEmail'])
        else:
            return render_template('signup.html')
        
    if request.method == 'POST':
        if 'userEmail' in session:
            return render_template('welcome.html', info=session['userEmail'])

        else :
            if users.userCreate(request.form.to_dict(flat='true')):
                session['userEmail'] = request.form['userEmail']
                return render_template('welcome.html', info=session['userEmail'])
            else:
                flash('Email is already Exists, try again with other Email.')
                return redirect(url_for('signup'))

@app.route('/')
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        if 'userEmail' in session:
            return render_template('welcome.html', info=session['userEmail'])
        else:
            return render_template('login.html')
        
    if request.method == 'POST':
        if 'userEmail' in session:
            return render_template('welcome.html', info=session['userEmail'])
        else:
            if users.userAuthentication(request.form.to_dict(flat='true')):
                session['userEmail'] = request.form['userEmail']
                return render_template('welcome.html', info=session['userEmail'])
            else:
                flash('Wrong ID or PW, You have to check your ID or PW.')
                return redirect(url_for('login'))

@app.route('/logout')
def logout():
    if 'userEmail' in session:
        session.pop('userEmail')
        return redirect(url_for('login'))
    else:
        flash('You have to logged in')
        return redirect(url_for('login'))

@app.route('/register')
def register():
    if 'userEmail' in session:
        return render_template('register.html')
    else:
        flash('You have to logged in to use this service.')
        return redirect(url_for('login'))
    
@app.route('/books',methods=['GET', 'POST'])
def Books():
    if request.method == 'GET':
        if 'userEmail' in session:
            all_book = books.getAllbooks()
            return render_template('books.html', books=all_book)
        else:
            flash('You have to logged in')
            return redirect(url_for('login'))
    
    elif request.method == 'POST':
        if 'userEmail' in session:
            books.bookCreate(request.form.to_dict(flat=True))
            all_book = books.getAllbooks()
            return render_template('books.html', books=all_book)
        else:
            flash('You have to logged in')
            return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)