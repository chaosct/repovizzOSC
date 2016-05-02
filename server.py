from gevent import monkey
monkey.patch_all(thread=False)

from time import sleep
from threading import Thread
import sys

# ===== Server part =====

import OSC
from flask import Flask
from flask.ext.socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

from ws_to_osc import connectaddr


def send(msg):
    osc.sendto(msg, connectaddr)


@socketio.on('data', namespace='/osc')
def ws_play(message):
    if message['data']:
        msg = OSC.OSCMessage("/repovizz")
        msg += message['data']
        try:
            send(msg)
        except OSC.OSCClientError:
            pass


@socketio.on('bulk', namespace='/osc')
def ws_bulk(message):
    if message['data']:
        for row in message['data']:
            msg = OSC.OSCMessage("/repovizz")
            msg += row
            try:
                send(msg)
                sleep(0.001)
            except OSC.OSCClientError:
                pass


def addr_getter():
    global connectaddr
    while True:
        connectaddr = q.get()


def server(queue):
    global osc, q
    if queue:
        q = queue
        t = Thread(target=addr_getter)
        t.daemon = True
        t.start()
    osc = OSC.OSCClient()
    try:
        socketio.run(app, port=5000)
    except KeyboardInterrupt:
        pass
