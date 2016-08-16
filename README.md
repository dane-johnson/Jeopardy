# Jeopardy
## Notice
Shortly after the project began I decided to attempt to build the project as a single page application. That work is being done on [another branch](http://github.com/dane-johnson/jeopardy/tree/single-page-app/). Please  look there for latest updates.

This is a Jeopardy board, made by my brother and I, utilizing [Flask](http://flask.pocoo.org), [SocketIO](http://socket.io), [flask-SocketIO](http://flask-socketio.readthedocs.io), and [jQuery](https://jquery.com).
jQuery and SocketIO are [included](./jeopardy/static/), and instructions to install the rest are below.

Questions are from real *Jeopardy* games and are delivered by [jService.io](http://jservice.io).

##Installation instructions
- Flask

  Flask can be installed by executing `pip install flask`
  
- flask-SocketIO

  flask-SocketIO can be installed by executing `pip install flask-socketio`
  Additionally, for optimal speed, execute `pip install eventlet`
