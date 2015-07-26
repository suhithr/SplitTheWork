from flask import Flask, render_template, url_for
from flask.ext.sqlalchemy  import SQLAlchemy
from flask.ext.socketio import SocketIO, emit, send, join_room, leave_room
import gevent

from forms import *

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')

#db object
db = SQLAlchemy(app)

#importing models after the db object is created
from models import *


#Socketio server instance
socketio = SocketIO(app)

data_now = ""


@app.route('/')
def home():
    form = DocumentForm()
    return render_template('index.html', form=form)


@socketio.on('create or join', namespace='/doc')
def create_or_join(room):
    print "Received request from client  to join room : " + str(room)
    join_room(str(room))
    emit('in_room', room)
    document = DocumentTable.query.filter_by(room = room).first()
    print "Query result is : " + str(document)
    if document.data is not "":
        data_first = document.data
        print "The first data is " + data_first
        emit('initial data', {'room': room, 'data': data_first})
    else:
        qry = DocumentTable(room, "")
        db.session.add(qry)
        db.session.commit()
        emit('initial data', {'room': room, 'data': ""})
'''
#This one updates the data from the data in the database
@socketio.on('connect', namespace='/doc')
def on_connect():
    emit('initial data', {'data': data_first})
'''

@socketio.on('edited', namespace='/doc')
def on_edited(message):
    print "Got edited : " + str(message)
    data_now = message['data']
    #Now updating in the database
    doc = DocumentTable.query.filter_by(room=message["room"]).first()
    if doc is not None:
        print "Adding : " + data_now + " : to the database"
        doc.data = data_now
    #Sending the changes to everybody
    emit('update', {'data': data_now}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app)
