from flask import Flask, render_template, redirect, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from os import urandom

from forms import PasteDataForm

app = Flask(__name__)
app.secret_key = urandom(32)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://test.db'
db = SQLAlchemy(app)



@app.route('/')
def home():
    return render_template('home.html', form=PasteDataForm())

@app.route('/convert-format', methods=['POST'] )
def convert_format():
    uuid = urandom(16).encode('hex')
    return redirect(url_for('results'))

@app.route('/results', methods=['GET'])
def results():
    return render_template('results.html')
