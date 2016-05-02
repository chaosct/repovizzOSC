Repovizz player to OSC
======================

This software adds to repovizz the feature to send the played streams to 3rd party
software using OSC. The principle is very simple:

repovizz in browser --(websocket)--> ws_to_osc.py --(OSC)--> 3rd Party software

**Author/contact**: carles.fernandez@upf.edu


Setup
-----

You can use a pre-compiled binary instead.

We have to set up the websocket-toOSC server:

```
# virtualenv stuff (optional)
$ virtualenv env
$ . env/bin/activate

# installing libraries
(env)$ pip install -r requirements.txt

# running the server
(env)$ python repoVizzOSC.py #with GUI
(env)$ python repoVizzOSC.py --cli #without GUI
```


Usage
-----

Open your browser to http://repovizz.upf.edu and use repovizz as usual.
When inside a datapack, add some signals to the canvases. When you play them (pressing space),
the data is sent to the server and then as OSC messages to `localhost:6448` with the address `/repovizz`
and the signals' values as arguments.

To send parts of the recording, select a part of the timeline (`b` key: begin, `e` key: end),
and press `o` key to send the bulk of messages.

License
-------

This repository needs a license.
