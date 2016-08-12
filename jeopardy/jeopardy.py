#Lot of imports, buckle up
import os
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
  
@app.route('/')
@app.route('/index')
def index():
	return render_template("index.html")
  
  
if __name__ == '__main__':
	socketio.run(app)