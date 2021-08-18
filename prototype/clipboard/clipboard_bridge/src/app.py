import mimetypes
import os
import signal
import sys
from urllib.parse import unquote
from flask import Flask
from networking.server import ConnectionHandler
from networking.emitter import ClipEmitter
from clipboard_handler import ClipboardHandler
import signal
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore


class ClipboardServerApp(QApplication):

    def load_local_file(self, path):
        new_file = {}
        f = open(path, mode='rb')
        new_file['data'] = f
        new_file['mimetype'] = mimetypes.guess_type(path)[0]
        new_file['filename'] = os.path.split(f.name)[1]
        if new_file['mimetype'] is None:
            new_file['mimetype'] = 'application/ƒoctet-stream'
        return new_file

    def load_files(self, uri_list):
        """
        Gets all files specified in uri_list from the disk and loads them.
        :return: A list of objects with the file itself, it's mimetype
        and name
        """
        to_return = []
        splits = uri_list.splitlines()
        for s in splits:
            path = unquote(s.decode("utf8")).split('://')[1]  # Strings file://
            protocol = unquote(s.decode("utf8")).split('://')[0]

            if protocol is 'file':
                to_return.append(self.load_local_file(path))
            else:
                clip = {}
                clip['data'] = str(s)
                clip['mimetype'] = 'text/plain'
                print('Clipboard bridge cannot (yet) handle the following protocol ' + protocol)
                to_return.append(clip)
        return to_return

    def on_data_get(self, data):
        """
        Not really sure, why this method is needed
        might be related to event-loops
        """
        self.clh.put_into_storage(data)

    def send_clipboard_data(self, clip_list):
        """
        Called after the data of the local clipboard has changed.
        Forwards the new content of the clipboard to the server.
        Files will be loaded as needed.
        """
        for clip in clip_list:
            if 'text/uri-list' in clip['mimetype']:
                clip_list += self.load_files(clip['data'])
                break
        self.clip_sender.add_clips_to_server(clip_list)

    def on_id_get(self, _id):
        """
        Called after the clipboard registered itself to the remote server.
        It will receive an id to identify it which should be used in subsequent
        requests to identify itself in the X-C2-sender_id header
        """
        self.clip_sender._id = _id

    def on_current_clip_id_get(self, _id):
        """
        Called when a new clip has been received. Its id will be saved so
        entries received hereafter can be identified as either a different
        representation of the same data or as a completely new clip
        (i.e. another clipboard has been changed and the contents are
        getting synced)
        """
        self.clh.clipboard.current_id = _id

    def main(self):
        """
        Starts the Flask server and its clipboard.
        Establishes signal-slot connections
        """
        self.flask_qt.moveToThread(self.server_thread)
        self.server_thread.started.connect(self.flask_qt.start_server)

        # Kills server with whole app
        self.aboutToQuit.connect(self.server_thread.terminate)
        # Makes C-c usable in console, because QT would block it normally
        signal.signal(signal.SIGINT, signal.SIG_DFL)

        self.clh.clipboard.clipboard_changed_signal.connect(
                self.send_clipboard_data)
        # Cannot put it into self.flask_qt because run() blocks anything
        self.flask_qt.new_item_signal.connect(self.on_data_get)
        self.flask_qt.recipient_id_got.connect(self.on_id_get)
        self.server_thread.start()

    def __init__(self, port, clipserver_address, domain, is_syncing, argv=sys.argv, app=None):
        super(ClipboardServerApp, self).__init__(argv)
        self.flask_server = Flask(__name__)
        self.flask_qt = ConnectionHandler(
                self.flask_server,
                port,
                clipserver_address,
                domain)
        self.server_thread = QtCore.QThread()

        # Connection to system clipboard
        self.clh = ClipboardHandler(self, is_syncing)
        self.clip_sender = ClipEmitter(
                clipserver_address,
                self.on_current_clip_id_get)