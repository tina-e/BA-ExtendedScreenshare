# https://github.com/PDA-UR/Screenshotmatcher-2.0/blob/master/python-server/src/server/server.py
import requests
from flask import Flask, request, Response


class FileServer:
    def __init__(self, streamer, event, address, port):
        self.streamer = streamer
        self.event = event
        self.address = address
        self.port = port
        self.logs = []
        self.app = Flask(__name__)
        self.client_pointer = None
        self.app.add_url_rule('/connect', "connect", self.connect_route)
        self.app.add_url_rule('/shutdown', "shutdown", self.shutdown, methods=['GET'])
        self.app.add_url_rule(f'/{event}', event, self.file_route, methods=['POST'])

    def start(self):
        self.app.run(host=self.address, port=self.port, threaded=True)

    def shutdown(self):
        shutdown_func = request.environ.get('werkzeug.server.shutdown')
        if shutdown_func is None:
            raise RuntimeError('Not running werkzeug')
        shutdown_func()
        return "Shutting down..."

    def close(self):
        r = requests.get(f"http://{self.address}:{self.port}/shutdown")

    def connect_route(self):
        print("Client connected to server")
        return Response()

    def file_route(self):
        if request.values.get('owner') == "viewer":
            filename = request.values.get('filename')
            mimetype = request.values.get('mimetype')
            drop_x = request.values.get('x')
            drop_y = request.values.get('y')
            print(filename, mimetype, drop_x, drop_y)
            file = request.files["files"]
            file.save(filename)
            #self.streamer.paste_file(file, mimetype, drop_x, drop_y)
        return Response()
