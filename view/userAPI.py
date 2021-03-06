from flask import Blueprint,request, jsonify, render_template, session, redirect, url_for, flash
from .db import connect_mongo, usersDAO

db_connection = connect_mongo.ConnectDB().db
users = usersDAO.Users(db_connection)

userAPI = Blueprint('userAPI',__name__, template_folder='templates')

@userAPI.route('/signup',methods=['GET','POST'])
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
                return redirect(url_for('userAPI.signup'))

@userAPI.route('/')
@userAPI.route('/login',methods=['GET','POST'])
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
                return redirect(url_for('userAPI.login'))

@userAPI.route('/logout')
def logout():
    if 'userEmail' in session:
        session.pop('userEmail')
        return redirect(url_for('userAPI.login'))
    else:
        flash('You have to logged in')
        return redirect(url_for('userAPI.login'))