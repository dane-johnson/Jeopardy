#Lot of imports, buckle up
import os
import rooms
from rooms import Room
from player import Player
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, escape
from flask_socketio import SocketIO, send, emit, join_room

#Init application
app = Flask(__name__)
app.config.from_object(__name__)
socketio = SocketIO(app)
active_rooms = {}

#Load default config and override config from an environment variable
app.config.update(dict(
	SECRET_KEY="trebek_rex"
	))

app.config.from_envvar("JEOPARDY_SETTINGS", silent = True)

#Frontend
@app.route('/')
@app.route('/index')
def welcome():
	#If this is the first time, find out if we'll be displaying in mobile view
	if not session.get('mobile'):
		platform = request.user_agent.platform
		session['mobile'] = (platform == 'iphone' or platform == 'android')
	if session['mobile']:
		return render_template("welcome.html")
	else:
		return render_template("welcome.html")
@app.route('/host_game')
def start_game():
	return render_template("host.html")
@app.route('/join_game')
def join_game():
	return render_template("join.html")
@app.route('/lobby')
def connect_player():
  room_code = str(escape(request.args.get('room_code')).striptags())
  name = str(escape(request.args.get('name')).striptags())
  if request.args.get('host', False):
    pass
    #TODO add alex feature
  session['room'] = room_code
  session['username'] = name
  active_rooms[room_code] + Player(name)
  socketio.emit('player joined', name, room=room_code)
  return render_template("lobby.html")


#Backend
@socketio.on('host game')
def setup_room():
	name = rooms.generate_room_name(active_rooms)
	active_rooms[name] = Room(name)
	join_room(name)
	emit('room created', name, room=name)
@socketio.on('user entered lobby')
def send_members(join_data):
  room = active_rooms[join_data['room']]
  join_room(room.name)
  data = []
  for player in room.players:
    data.append(player.name)
  emit('users in lobby', data, room=room.name);
@socketio.on('disconnect')
def handle_disconnect():
	print 'User disconnected'


if __name__ == '__main__':
	socketio.run(app)