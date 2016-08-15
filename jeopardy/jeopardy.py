from gevent import monkey
monkey.patch_all()

#Lot of imports, buckle up
import os
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, escape
from flask_socketio import SocketIO, send, emit, join_room

from utils import Room, Contestant, generate_room_name

BAD_ROOM_CODE = 1

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
	# Find out if the room code is valid
	room_code = data['room_code']
	if room_code in active_rooms.keys():
		join_room(room_code)
		# Find out if this player is the host or a contestant
		if(data['host']):
			emit("accept host")
			active_rooms[room_code].add_host()
		else:
			name = data['username']
			emit("accept player", name, broadcast=True, room=room_code)
			active_rooms[room_code].add_contestant(Contestant(name))
	else:
		emit("error", BAD_ROOM_CODE)

@socketio.on('create room')
def create_room():
	room_code = generate_room_name(active_rooms)
	active_rooms[room_code] = Room(room_code)
	join_room(room_code)
	emit('room created', room_code)
@socketio.on('request players')
def send_players(room_code):
	if room_code != None:
		room = active_rooms[room_code]
		players = room.contestants
		# This is a generator function that gets everyone's name
		names = [player.name for player in players]
		emit('player list', names)