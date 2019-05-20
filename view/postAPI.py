from flask import Blueprint, flash, session, render_template, jsonify, request, redirect, url_for
from .db import connect_mongo, postsDAO

db_connection = connect_mongo.ConnectDB().db
posts = postsDAO.Posts(db_connection)

postAPI = Blueprint('postAPI', __name__, template_folder='templates')

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
			posts.postCreate(request.form.to_dict(flat=true))
			all_posts = posts.getAllposts()
			return render_template("post.html", posts=all_posts)
		else:
			flash('You have to logged in')
			redirect(url_for('userAPI.login'))

