from flask import Blueprint, flash, session, render_template, jsonify, request, redirect, url_for
from .db import connect_mongo, postsDAO
import time

db_connection = connect_mongo.ConnectDB().db
posts = postsDAO.Posts(db_connection)

postAPI = Blueprint('postAPI', __name__, template_folder='templates')

def dict_merge(x,y):
	return {**x,**y}

@postAPI.route("/post", methods=["GET", "POST"])
def post():
	if request.method == "GET":
		if "userEmail" in session:
			all_posts = posts.getAllposts()
			return render_template("post.html", posts=all_posts)
		else:
			flash('You have to logged in')
			redirect(url_for('userAPI.login'))

	if request.method == "POST":
		if "userEmail" in session:
			now = time.strftime("%Y-%m-%d %H:%M")
			posts.postCreate(dict_merge({"postAuthor":session["userEmail"],"postDate":now},request.form.to_dict(flat=True)))
			all_posts = posts.getAllposts()
			return render_template("post.html", posts=all_posts)
		else:
			flash('You have to logged in')
			redirect(url_for('userAPI.login'))

