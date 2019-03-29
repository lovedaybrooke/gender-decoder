from flask_wtf import FlaskForm
from wtforms import TextAreaField, SelectField, validators

import app.wordlists as wordlists


class JobAdForm(FlaskForm):
    texttotest = TextAreaField(u"", [validators.Length(min=1)])
    language = SelectField(
        "English",
        choices=[
            (key, value["language_name"]) for key, value in wordlists.all_lists.items()
        ],
        default=("en", "English"),
    )
