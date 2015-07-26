from flask_wtf import Form
from wtforms import TextField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea


class DocumentForm(Form):
    title = TextField('title', validators=[DataRequired()])
    data = TextField('data', widget=TextArea())
