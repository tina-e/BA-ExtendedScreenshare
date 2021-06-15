# https://www.youtube.com/watch?v=FppvGEEv4l4
from gevent import monkey; monkey.patch_all()

from flask import Flask, Response, render_template, stream_with_context
from gevent.pywsgi import WSGIServer

import json
import time

from evdev import InputDevice, ecodes as e, events

app = Flask(__name__)

@app.route("/")
def render_index():
    return render_template("index.html")

@app.route("/listen")
def listen():
    def respond_to_client():
        # listen to mouse
        device = InputDevice('/dev/input/event11')
        print(device)
        for event in device.read_loop():
            _data = json.dumps({"event": str(event)}) #TODO: event in json umwandeln
            yield f"id: 1\ndata: {_data}\nevent: online\n\n"
            #if event.type == e.EV_KEY:
                #print("clicked")
    return Response(respond_to_client(), mimetype='text/event-stream')


if __name__ == "__main__":
    #app.run(port=8000, debug=True)
    http_server = WSGIServer(("localhost", 8000), app)
    http_server.serve_forever()
