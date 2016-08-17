from gevent import monkey
monkey.patch_all()

#Lot of imports, buckle up
import os
import httplib
import json
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, escape
from flask_socketio import SocketIO, send, emit, join_room

from utils import Room, Contestant, generate_room_name

#Constants
BAD_ROOM_CODE = 1

#Init application
#Init connection to jservice service
jservice = httplib.HTTPConnection('jservice.io')
app = Flask(__name__)
app.config.from_object(__name__)
socketio = SocketIO(app)
active_rooms = {}

#Load default config and override config from an environment variable
app.config.update(dict(
	SECRET_KEY="trebek_rex"
	))

####################################  Frontend  ###############################
@app.route('/')
@app.route('/index')
def index():
	return render_template("index.html")
@app.route('/views/<path:filename>')
def view(filename):
	# We route any requests for views through the server, so we can apply Flask and Jinja markup.
	return render_template(filename)
@app.route('/category/')
def get_category():
	#Make a request for a random question
	data = []
	while len(data) < 1:
		jservice.request('GET', '/api/random/')
		data = jservice.getresponse().read()
		data = json.loads(data)
	category_id, category_title = data[0]['category']['id'], data[0]['category']['title']
	questions = []
	answers = []
	while len(answers) < 5:
		for i in range(200, 1200, 200):
			jservice.request('GET', '/api/clues?category=%d&value=%d' % (category_id, i))
			data = jservice.getresponse().read()
			data = json.loads(data)
			if len(data) < 1:
				break
			questions.append(data[0]['question'])
			answers.append(data[0]['answer'])
	return json.dumps({'category': category_title, 'questions':questions, 'answers':answers})


####################################  Backend  ################################
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
			#Check to see if the game is ready
			if active_rooms[room_code].is_ready:
				emit("game ready", room=room_code, broadcast=True)
		else:
			name = data['username']
			emit("accept player", name, broadcast=True, room=room_code)
			active_rooms[room_code].add_contestant(Contestant(name))
			#Check to see if the game is ready
			if active_rooms[room_code].is_ready:
				emit("game ready", room=room_code, broadcast=True)
	else:
		emit("error", BAD_ROOM_CODE)
@socketio.on('create room')
def create_room():
	#Get a room from the generator
	room_code = generate_room_name(active_rooms)
	#Add it to the active rooms list as a new Room object
	active_rooms[room_code] = Room(room_code)
	join_room(room_code)
	#Send it out
	emit('room created', room_code)
@socketio.on('request players')
def send_players(room_code):
	if room_code != None:
		room = active_rooms[room_code]
		players = room.contestants
		# This is a generator function that gets everyone's name
		names = [player.name for player in players]
		emit('player list', names)
@socketio.on('start game')
def start():
	print "start game requested";