from flask_wtf import FlaskForm
from wtforms import TextAreaField, validators


class JobAdForm(FlaskForm):
    texttotest = TextAreaField(u'', [validators.Length(min=1)])
