# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 20:18:20 2019

@author: Rekt77
"""

from flask import Flask, session
from view.bookAPI import bookAPI
from view.userAPI import userAPI
from datetime import timedelta
import json

app = Flask(__name__)
app.register_blueprint(bookAPI)
app.register_blueprint(userAPI)
with open("jwt.json") as Json:
    app.secret_key = json.loads(Json.read())["secret"]

@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=20)
    print("before!")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)