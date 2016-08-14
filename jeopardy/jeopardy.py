#Lot of imports, buckle up
import os
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, escape
from flask_socketio import SocketIO, send, emit, join_room

from utils import generate_room_name

#Init application
app = Flask(__name__)
app.config.from_object(__name__)
socketio = SocketIO(app)
active_rooms = []

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
	emit("accept player")
@socketio.on('create room')
def create_room():
	room_name = generate_room_name(active_rooms)
	active_rooms.append(room_name)
	emit('room created', room_name)
  
  
if __name__ == '__main__':
	socketio.run(app)