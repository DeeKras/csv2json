from flask_wtf import Form
from wtforms import StringField, TextAreaField, RadioField, BooleanField
from wtforms.validators import DataRequired

class PasteDataForm(Form):
    data_type = RadioField(label='What would you like to convert to?',
                            description ='',
                            choices=[('csv', 'CSV'),('json','JSON')],
                            validators=[DataRequired(),])
    data_blob = TextAreaField(label='Dump your data here',
                              validators=[DataRequired(),])

#csv related fields
    header_row = BooleanField(label='Is first row the header row?', 
                              default='y')
    delimiters = RadioField(label='Field Separator',
                            choices=[(',', 'Comma [,]'),
                                    (';', 'Semi-Colon [;]'),
                                    (':', 'Colon [:]'),
                                    ('|', 'Bar [|]'),
                                    (r'\t', 'Tab'),
                                    (r'\s', 'Space')],
                            default=',',
                            validators=[DataRequired(),])


