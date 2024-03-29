import requests
from flask import Flask, request, Response
from pathlib import Path

class FileServer:
    '''
    This class receives files that were dropped into the stream by the receiver.
    '''
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
        '''
        Called when receiver does a POST-Request containing the file(s) that were dropped.
        Receiver sends file, filename and position of the drop. The file is saved.
        The streamer will now handle the drop.
        '''
        if request.values.get('owner') == "receiver":
            filename = request.values.get('filename')
            mimetype = request.values.get('mimetype')
            drop_x = request.values.get('x')
            drop_y = request.values.get('y')
            file = request.files["files"]
            file.save(filename)
            while not Path(filename).exists():
                pass
            self.streamer.handle_drop(filename, drop_x, drop_y)
            #self.streamer.dragon_drop(filename, drop_x, drop_y)
        return Response()
