# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 02:46:37 2019

@author: Rejt77
"""

from flask import Flask, jsonify
import jwt
import datetime
import json

app= Flask(__name__)

with open("jwt.json") as Json:
    secret_key = json.loads(Json.read())["secret"]

@app.route("/get_token")
def get_token():
    date_time_obj = datetime.datetime
    exp_time = date_time_obj.timestamp(date_time_obj.utcnow() + datetime.timedelta(hours=24))
    payload = {
        'exp':int(exp_time)        
    }
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    
    return jsonify({
            "message":"token is generated",
            "token":str(token.decode('utf-8'))
            }),201
    
if __name__ == "__main__":
    app.run(port=5001)