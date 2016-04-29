#!/bin/env python

"""
repoVizz OSC middleware

Carles F. Julià <carles.fernandez@upf.edu> 2016
"""

from gevent import monkey
monkey.patch_all()

from time import sleep
from threading import Thread
from multiprocessing import Process, freeze_support
import sys

# ===== Server part =====

import OSC
from flask import Flask
from flask.ext.socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)
connectaddr = ('localhost',6448)


def send(msg):
    osc.sendto(msg,connectaddr)


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


def server():
    global osc, q
    osc = OSC.OSCClient()
    try:
        socketio.run(app, port=5000)
    except KeyboardInterrupt:
        pass


# ===== GUI part =====

from Tkinter import *
import ttk


def gui():
    root = Tk()
    root.title("repoVizz OSC")

    mainframe = ttk.Frame(root, padding="1 1 12 12")
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    mainframe.columnconfigure(0, weight=1)
    mainframe.rowconfigure(0, weight=1)

    ttk.Label(mainframe, text="Sending OSC messages to {}:{}".format(*connectaddr)).grid(column=1,row=1, sticky=E)

    for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

    root.mainloop()


def main():
    if '--cli' not in sys.argv:
        t = Process(target=server)
        t.daemon = True
        t.start()
        gui()
    else:
        server()


if __name__ == '__main__':
    freeze_support()
    main()