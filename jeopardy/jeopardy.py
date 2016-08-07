#Lot of imports, buckle up
import os
import rooms
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, escape
from flask_socketio import SocketIO, send, emit, join_room

#Init application
app = Flask(__name__)
app.config.from_object(__name__)
socketio = SocketIO(app)
active_rooms = []

#Load default config and override config from an environment variable
app.config.update(dict(
	SECRET_KEY="trebek_rex"
	))

app.config.from_envvar("JEOPARDY_SETTINGS", silent = True)
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
  room_code = escape(request.args.get('room_code'))
  name = escape(request.args.get('name'))
  print 'Player %s wants to join room %s' % (name, room_code)
  if request.args.get('host', False):
    pass
    #TODO add alex feature
  socketio.emit('player joined', name, room=room_code)
  return "<h1>LOBBY</h1>"
@socketio.on('host game')
def setup_room():
	room = rooms.generate_room_name(active_rooms)
	active_rooms.append(room)
	join_room(room)
	emit('room created', room, room=room)
@socketio.on('disconnect')
def handle_disconnect():
	print 'User disconnected'


if __name__ == '__main__':
	socketio.run(app)