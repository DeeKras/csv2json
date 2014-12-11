"""
    This app converts data from csv <--> json.
    User pastes in teh data and chooses the data_type to change it to.
    app does the conversion and displays results
    --
    uses WTForms, SQLAlchemy
"""

from flask import Flask, render_template, redirect, url_for, request
from flask.ext.sqlalchemy import SQLAlchemy
from os import urandom
import csv
import json

from forms import PasteDataForm

app = Flask(__name__)
app.secret_key = urandom(32)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://test.db'
db = SQLAlchemy(app)

csv_workspace = 'work_space.csv'
json_workspace = 'work_space.json'
pasted_data_file = 'pasted_data_file.txt'




@app.route('/')
def home():
    return render_template('home.html', form=PasteDataForm())

@app.route('/convert-format', methods=['POST'])
def convert_format():
    form = PasteDataForm()
    if request.method == 'POST':
        uuid = urandom(16).encode('hex')  #will use this for unique users using the program
        
        pasted_data = form.data_blob.data  
        p  = open(pasted_data_file, "w")  # save to a (temporary file because so large)
        p.write(pasted_data)
        p.close()

        data_type = form.data_type.data
        if data_type == 'csv':  # meaning convert to csv
            output_file = json_to_csv(pasted_data_file)

        if data_type == 'json':  # meaning convert to json
            output_file = csv_to_json(pasted_data_file)

    return render_template('results.html', data_type=data_type, 
                                            output_file=output_file)

def csv_to_json(pasted_data_file):
    output = []

    with open(pasted_data_file, 'rb') as csvfile:
        dialect = csv.Sniffer().sniff(csvfile.read(1024))  
        csvfile.seek(0)
        csv_reader = csv.reader(csvfile, dialect)
 
        fieldnames = csv_reader.next()  # detects how many columns
        for each in csv_reader:
            row ={}
            for i, fieldname in enumerate(fieldnames):
                row[fieldname] = each[i]
            output.append(row)
    json.dump(output,open(json_workspace,'w'),indent=4,sort_keys=False)
    output_file = json.load(open(json_workspace,"r"))

    return  output_file

def json_to_csv(pasted_data_file):

    jsonfile = open(pasted_data_file, 'rb')
    to_convert = json.load(jsonfile)
    jsonfile.close()

    with open(csv_workspace, 'w') as csvfile:
        output_file = csv.writer(csvfile)
        output_file.writerow(to_convert[0].keys())
        for row in to_convert:
            output_file.writerow(row.values())

    with open(csv_workspace, 'r') as csvfile:
        output_file = csvfile.readlines()

    return output_file

