from app import db
from flask.ext.sqlalchemy import SQLAlchemy

class DocumentTable(db.Model):
    __tablename__ = 'DocumentTable'

    id = db.Column(db.Integer, primary_key=True)
    room = db.Column(db.String, nullable=False)
    data = db.Column(db.Text, nullable=True)
    field = db.Column(db.Text, nullable=False)

    def __init__(self, room, data, field):
        self.room = room
        self.data = data
        self.field = field
