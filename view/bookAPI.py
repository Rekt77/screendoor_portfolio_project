from flask import Blueprint,request, jsonify, render_template, session, redirect, url_for, flash
from .db import connect_mongo, booksDAO

db_connection = connect_mongo.ConnectDB().db
books = booksDAO.Books(db_connection)

bookAPI = Blueprint('bookAPI',__name__, template_folder='templates')

@bookAPI.route('/register')
def register():
    if 'userEmail' in session:
        return render_template('register.html')
    else:
        flash('You have to logged in to use this service.')
        return redirect(url_for('login'))
    
@bookAPI.route('/books',methods=['GET', 'POST'])
def Books():
    if request.method == 'GET':
        if 'userEmail' in session:
            all_book = books.getAllbooks()
            return render_template('books.html', books=all_book)
        else:
            flash('You have to logged in')
            return redirect(url_for('userAPI.login'))
    
    elif request.method == 'POST':
        if 'userEmail' in session:
            books.bookCreate(request.form.to_dict(flat=True))
            all_book = books.getAllbooks()
            return render_template('books.html', books=all_book)
        else:
            flash('You have to logged in')
            return redirect(url_for('userAPI.login'))