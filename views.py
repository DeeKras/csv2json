"""
    This app converts data from csv <--> json.
    User pastes in the data and chooses the data_type to change it to.
    app does the conversion and presents the converted data as a file for download.
    --
    uses WTForms, SQLAlchemy
"""

from flask import Flask, render_template, redirect, url_for, request, flash, make_response
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

@app.route('/download', methods= ['GET','POST'])
def download():
    form = PasteDataForm()
    if request.method == 'POST':
        data_type = form.data_type.data
        header_row = form.header_row.data
        delimiters = str(form.delimiters.data)
        uuid = urandom(16).encode('hex')  #will use this for unique users using the program
        pasted_data = form.data_blob.data  

        with open(pasted_data_file, "w") as p: # save to a (temporary file because so large)
            p.write(pasted_data)

        #if user didn't choose a data type to convert to
        if data_type not in ['csv', 'json']:
            flash("You must select a format to convert to")
            return redirect(url_for('home'))

        elif data_type == 'csv':  # meaning convert to csv
            output_file = json_to_csv(pasted_data_file)

        elif data_type == 'json':  # meaning convert to json
            output_file = csv_to_json(pasted_data_file, header_row, delimiters)

    response = make_response(str(output_file)) # this creates a file with the converted data on the user's computer
    response.headers["Content-Disposition"] = "attachment; filename=converted.csv"
    return response

def json_to_csv(pasted_data_file):

    with open(pasted_data_file, 'rb') as jsonfile:
        to_convert = json.load(jsonfile)

    with open(csv_workspace, 'w') as csvfile:
        fieldnames = to_convert[0].keys()
        output_file = csv.DictWriter(csvfile, quoting=csv.QUOTE_NONNUMERIC, 
                                                fieldnames=fieldnames, 
                                                delimiter=',', 
                                                lineterminator='\n')
        output_file.writeheader()  #header row
        for row in to_convert:
            output_file.writerow(row)
  
    with open(csv_workspace, 'r') as csvfile:
        rows = ""
        output_file = csv.reader(csvfile, delimiter=',', lineterminator='\n')
        for row in output_file:
            new_row = ', '.join(row)
            rows += new_row
        return rows

def csv_to_json(pasted_data_file, header_row, delimiter):
    output = []

    with open(pasted_data_file, 'rb') as csvfile:
        dialect = csv.Sniffer().sniff(csvfile.read(1024))  
        csvfile.seek(0)
        csv_reader = csv.reader(csvfile, dialect, delimiter=delimiter)
        first_row = csv_reader.next()
        fieldnames = []
        if header_row:
            fieldnames = first_row  # detects names of columns
        else:
            for i, j in enumerate(first_row, 1):
                fieldname = 'field{}'.format(str(i))
                fieldnames.append(fieldname)
        for each in csv_reader:
            row = {}
            for j, fieldname in enumerate(fieldnames):
                row[fieldname] = each[j]
                print row

            output.append(row)

             
    json.dump(output, open(json_workspace, 'w'), indent=4, sort_keys=False)
    output_file = json.load(open(json_workspace, "r"))

    return  output_file



