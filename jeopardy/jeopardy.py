#Lot of imports, buckle up
import os
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, escape
from flask_socketio import SocketIO, send, emit, join_room

from utils import Room, Contestant, generate_room_name

#Init application
app = Flask(__name__)
app.config.from_object(__name__)
socketio = SocketIO(app)
active_rooms = {}

#Load default config and override config from an environment variable
app.config.update(dict(
	SECRET_KEY="trebek_rex"
	))

#Frontend
@app.route('/')
@app.route('/index')
def index():
	return render_template("index.html")
@app.route('/views/<path:filename>')
def view(filename):
  return render_template(filename)

#Backend
@socketio.on('player joined')
def add_player(data):
	#This is firing twice per connection. Why?
	print "adding player"
	name = data['username']
	room_code = data['room_code']
	if room_code in active_rooms.keys():
		active_rooms[room_code].add_contestant(Contestant(name))
		# emit to all clients
		emit('accept player', name, broadcast=True)
@socketio.on('create room')
def create_room():
	room_name = generate_room_name(active_rooms)
	active_rooms[room_name] = Room(room_name)
	emit('room created', room_name)
  
  
if __name__ == '__main__':
	socketio.run(app)