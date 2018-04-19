
__author__ = 'Erwin'
#!flask/bin/python
from flask import Flask,request,render_template

app = Flask(__name__)

@app.route('/login',method=['POST'])
def login():
    req_data = request.get_json()

    user = req_data['username']
    password = req_data['password']
    python_version = req_data['access']



