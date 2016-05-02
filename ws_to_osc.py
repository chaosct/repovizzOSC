#!/bin/env python
# -*- coding: utf-8 -*-

"""
repoVizz OSC middleware

Carles F. Julià <carles.fernandez@upf.edu> 2016
"""

from multiprocessing import Process, freeze_support, Queue
connectaddr = ('localhost', 6448)

# ===== GUI part =====

from Tkinter import *
import ttk

queue = Queue()


def gui():
    root = Tk()
    root.title("repoVizz OSC")

    def change_addr(*args):
        try:
            queue.put((host.get(), int(port.get())))
        except ValueError:
            pass

    mainframe = ttk.Frame(root, padding="3 1 12 12")
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    mainframe.columnconfigure(0, weight=1)
    mainframe.rowconfigure(0, weight=1)

    ttk.Label(mainframe, text="Sending OSC messages").grid(
        column=1, row=1, sticky=W)
    ttk.Button(mainframe, text="Change", command=change_addr).grid(
        column=1, row=3, sticky=E)

    configframe = ttk.Frame(mainframe, padding="2 2 0 0")
    configframe.grid(column=1, row=2, sticky=(N, W, E, S))
    configframe.columnconfigure(0, weight=1)
    configframe.rowconfigure(0, weight=1)

    ttk.Label(configframe, text="host ").grid(column=1, row=1, sticky=(W, E))
    ttk.Label(configframe, text="port ").grid(column=1, row=2, sticky=(W, E))

    host = StringVar()
    port = StringVar()

    host.set(connectaddr[0])
    port.set(str(connectaddr[1]))

    ttk.Entry(configframe, width=20, textvariable=host).grid(
        column=2, row=1, sticky=(W, E))
    ttk.Entry(configframe, width=7, textvariable=port).grid(
        column=2, row=2, sticky=(W, E))

    for child in mainframe.winfo_children():
        child.grid_configure(padx=5, pady=5)

    root.bind('<Return>', change_addr)

    root.mainloop()


def server(q=None):
    from server import server
    server(q)


def main():
    global connectaddr
    args = sys.argv[1:]
    args = [a for a in args if a != '--cli']
    if len(args) == 2:
        h = args[0]
        p = int(args[1])
        connectaddr = (h,p)
    elif args:
        print "Usage: {} [--cli] [hostname port]".format(sys.argv[0])
        return
    print "Sending OSC to {}:{}".format(*connectaddr)
    if '--cli' not in sys.argv:
        t = Process(target=server, args=(queue,))
        t.daemon = True
        t.start()
        gui()
    else:
        server()


if __name__ == '__main__':
    freeze_support()
    main()
