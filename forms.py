from flask_wtf import Form
from wtforms import StringField, TextAreaField, RadioField
from wtforms.validators import DataRequired

class PasteDataForm(Form):
    data_type = RadioField(label='What would you like to convert to?',
                            description ='',
                            choices=[('csv', 'CSV'),('json','JSON')],
                            validators=[DataRequired(),])
    data_blob = TextAreaField(label='Dump your data here',
                              validators=[DataRequired(),])
