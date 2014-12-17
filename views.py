"""
    This app converts data from csv <--> json.
    User pastes in the data and chooses the data_type to change it to.
    app does the conversion and presents the converted data as a file for download.
    --
    uses WTForms, SQLAlchemy
"""

from flask import Flask, render_template, redirect, url_for, request, flash, make_response, session
from flask.ext.sqlalchemy import SQLAlchemy
from os import urandom
import csv
import json
import cStringIO
import pyperclip



from forms import PasteDataForm

app = Flask(__name__)
app.secret_key = urandom(32)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://test.db'
db = SQLAlchemy(app)

output_file = 'output_file.txt'
pasted_data_file = 'pasted_data_file.txt'




@app.route('/')
def home():
    return render_template('home.html', form=PasteDataForm())

@app.route('/results', methods= ['GET','POST'])
def results():
    form = PasteDataForm()
    print request.method
    if request.method == 'POST':
        data_type = form.data_type.data
        header_row = form.header_row.data
        delimiters = str(form.delimiters.data)
        uuid = urandom(16).encode('hex')  #will use this for unique users using the program
        pasted_data = form.data_blob.data
        session['data_type'] = data_type

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

        session['output'] = output_file

    return render_template("results.html", data_type=data_type,
                                           output_file=output_file)


@app.route('/download', methods=['GET','POST'])
def download():
    output_file = session['output']
    data_type = session['data_type']

    if request.form['submit'] == 'copy':
        pyperclip.copy(output_file)
        flash ("The file should be in your clipboard. You can now paste it.")
        # clipboard = pyperclip.paste()
        return render_template("results.html", data_type=data_type,
                                           output_file=output_file)

    elif request.form['submit'] == 'download':
        response = make_response(str(output_file)) # this creates a file with the converted data on the user's computer
        response.headers["Content-Disposition"] = "attachment; filename=converted.{}".format(data_type)
        return response

def json_to_csv(pasted_data_file):

    with open(pasted_data_file, 'rb') as jsonfile:
        to_convert = json.load(jsonfile)

    # with open(csv_workspace, 'w') as csvfile:
    #     fieldnames = to_convert[0].keys()
    #     output_file = csv.DictWriter(csvfile, quoting=csv.QUOTE_NONNUMERIC, 
    #                                             fieldnames=fieldnames, 
    #                                             delimiter=',', 
    #                                             lineterminator='\n')
    #     output_file.writeheader()  #header row
    #     for row in to_convert:
    #         output_file.writerow(row)

    output = cStringIO.StringIO()
    output.write("{}\n".format(", ".join(to_convert[0].keys())))
    for row in to_convert:
        output.write("{}\n".format(", ".join(row.values())))
    contents = output.getvalue()
    return contents

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

            output.append(row)

             
    json.dump(output, open(output_file, 'w'), indent=4, sort_keys=False)
    output = json.load(open(output_file, "r"))

    return  output



