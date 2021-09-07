import requests
from requests import exceptions as req_exceptions
from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal
from utils import network_util
from flask import request
import time
import sys

class ConnectionHandler(QObject):
    """
    ConnectionHandler is a QT-wrapper over a Flask server and will listen to
    incoming requests and handle their data.
    """

    new_item_signal = pyqtSignal(dict)
    recipient_id_got = pyqtSignal(str)
    MAX_CONNECTION_ERRORS = 5
    CONNECTION_ERROR_TIMEOUT = 10

    def __init__(self, flask_app, port, clip_server_url, domain):
        super(QObject, self).__init__()
        self.flask_app = flask_app
        self.port = port
        self.clip_server_url = clip_server_url + "clipboards/register"
        if domain == 'http://localhost':
            self.domain = domain + ':' + str(self.port) + '/'
        # Request own ip through external service for more convenience
        elif domain == 'public':
            self.domain = network_util.get_public_ipv4(self.port)
        else:
            self.domain = domain + ':' + str(self.port) + '/'

        self.connection_error_count = 0

        # needed to add the route here, because self.flask_app needs to be set
        @self.flask_app.route('/', methods=['POST'])
        def new_item_incoming():
            return self.handle_request(request)

    def _on_error(self, message):
        self.connection_error_count += 1
        if self.connection_error_count > self.MAX_CONNECTION_ERRORS:
            self._die(message)
        else:
            print("Connection to server failed, try reconnect in " + str(self.CONNECTION_ERROR_TIMEOUT) +
                  " seconds. Attempt no. (" + str(self.connection_error_count) + "/" + str(self.MAX_CONNECTION_ERRORS) + ") ")
            time.sleep(self.CONNECTION_ERROR_TIMEOUT)
            self.register_to_server()


    def _die(self, message):
        print("Clipboard Server: Networking has died")
        # This causes the app to crash if connection fails
        # TODO: add slot for error messages
        sys.exit(1)

    def _check_data(self, data):
        """
        Checks if the relevant data could be parsed
        """
        keys = data.keys()
        if 'mimetype' in keys and 'data' in keys and '_id' in keys:
            return True
        else:
            return False

    def start_server(self):
        """
        Run flask on specified port
        """
        self.register_to_server()
        self.flask_app.run(
                host='0.0.0.0',
                port=self.port
        )

    def handle_request(self, request):
        """
        Parses incoming data from the server for the relevant parts
        """
        data = {}
        data['data'] = request.get_data()
        data['mimetype'] = request.headers['Content-Type']
        data['_id'] = request.headers['X-C2-_id']
        data['parent'] = request.headers.get('X-C2-parent', None)
        self.new_item_signal.emit(data)
        return '', 204

    def register_to_server(self):
        """
        Registers itself to the remote server. Kills the whole
        application if this fails
        """
        try:
            response = requests.post(
                    self.clip_server_url,
                    json={'url': self.domain},
                    timeout=5
            )
            response.raise_for_status()
            self.recipient_id_got.emit(response.json()['_id'])
            self.connection_error_count = 0
        except req_exceptions.ConnectionError as e:
            self._on_error('Connection refused by remote server')
        except req_exceptions.Timeout as e:
            self._on_error('Remote server failed to respond in time')
        except req_exceptions.HTTPError as e:
            m = 'Remote server responded with statuscode {}\n'.format(
                response.status_code)
            m += 'Message from server: {}'.format(response.text)
            self._on_error(m)