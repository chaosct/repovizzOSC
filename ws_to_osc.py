from gevent import monkey
monkey.patch_all()

from time import sleep
import OSC
from flask import Flask
from flask.ext.socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)
simuladorAddr = ('localhost',6448)


@socketio.on('data', namespace='/osc')
def ws_city(message):
    if message['data']:
        msg = OSC.OSCMessage("/repovizz")
        msg += message['data']
        try:
            osc.send(msg)
        except OSC.OSCClientError:
            pass

@socketio.on('bulk', namespace='/osc')
def ws_city(message):
    if message['data']:
        for row in message['data']:
            msg = OSC.OSCMessage("/repovizz")
            msg += row
            try:
                osc.send(msg)
                sleep(0.001)
            except OSC.OSCClientError:
                pass

if __name__ == '__main__':
    global osc
    osc = OSC.OSCClient()
    osc.connect(simuladorAddr)
    socketio.run(app, port=5000)