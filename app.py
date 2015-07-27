from flask import Flask, render_template, url_for
from flask.ext.sqlalchemy  import SQLAlchemy
from flask.ext.socketio import SocketIO, emit, send, join_room, leave_room
import gevent

from forms import *
'''
NOTES:
#Using namespace for the first time /doc for the document part
#Maybe use /chat for chat part if it ever gets added
TODO:
#Make is save the doc and update immediately - Done
#Allow for titles and for rooms
#Organise colorwise
#
'''

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')

#db object
db = SQLAlchemy(app)

#importing models after the db object is created
from models import *


#Socketio server instance
socketio = SocketIO(app)

data_now = ""

room='default'

@app.route('/')
def home():
    return render_template('index.html')


@socketio.on('create or join', namespace='/doc')
def create_or_join(room):
    print "Received request from client  to join room : " + str(room)
    join_room(str(room))
    emit('in_room', room)


@socketio.on('fields change', namespace='/doc')
def on_fields_change(numberofFields):
    print "Number of fields has changed to : " + str(numberofFields)
    emit('updateFields', {'data': numberofFields}, broadcast=True)


@socketio.on('edited', namespace='/doc')
def on_edited(message):
    print "Got edited : " + str(message)
    data_now = message['data']
    #Now updating in the database
    doc = DocumentTable.query.filter_by(field=message['field']).first()
    if doc is not None:
        print "Adding : " + data_now + " : to the database"
        doc.data = data_now
        db.session.commit()
    else:
        qry = DocumentTable(room, message['data'], message['field'])
        db.session.add(qry)
        db.session.commit()
    #Sending the changes to everybody
    emit('update', {'data': data_now}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app)
