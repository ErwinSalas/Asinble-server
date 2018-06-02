import base64
__author__ = 'Erwin'
from flask import Flask,request,render_template
import Controller

app = Flask(__name__)
app.secret_key = 'admin'

@app.route('/')
def indexPage():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
