from flask import Flask, request, render_template,redirect,url_for


import mysql.connector





from werkzeug.utils import secure_filename
import os
from flask import send_from_directory





cnx = mysql.connector.connect(user='root', password='123',
                              host='127.0.0.1',
                              database='ansibleBase')

app = Flask(__name__)

@app.route('/')
def indexPage():
    return render_template('index.html')


@app.route('/login', methods=['GET','POST'])
def login():


    if request.method == 'GET':
        return render_template('loginform.html')









if __name__ == '__main__':
    app.run(port=8090, debug=True)


cnx.close()
