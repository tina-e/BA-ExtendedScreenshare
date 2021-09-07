from argparse import ArgumentParser
from configparser import ConfigParser
import os
import sys
from app import ClipboardServerApp

"""
This starts the clipboard-server. It acts as a bridge to the OS-clipboard
and synchronizes it with the data from the server. This program can run in
two modes, depending on if it was started with the sync-clipboard option
enabled or not. If it IS enabled, all changes made to the local clipboard
will be forwarded to the server.
If disabled, it will act as a full client and only receive data from the
server while not sending local changes.

The Flask server needs to run in its own thread which adds most of the complex setup otherwise
it will block the whole program.
Built after https://codereview.stackexchange.com/questions/114221/python-gui-by-qtwebkit-and-flask
https://stackoverflow.com/questions/41401386/proper-use-of-qthread-subclassing-works-better-method
"""  # noqa

def parse_args():
    parser = ArgumentParser()
    config = ConfigParser()
    config.read('./../config/config.ini')
    parser.add_argument('-p', '--port', type=int, dest='port',
                        help='Port THIS server shall listen on, \
                              defaults to 5555', default=config['networking']['port'])
    parser.add_argument('-d', '--domain', type=str, dest='domain',
                        help='URL THIS server can be reached under, \
                              must contain specified port, \
                              defaults to localhost, set to "public" for exposing clipboard ' \
                             'to a remote clipserver',
                        default=config['networking']['domain'])
    parser.add_argument('-s', '--sync-clipboard', type=bool,
                        dest='sync_clipboard', default=config['networking']['is_syncing'],
                        help='If True, content of clipboard will be \
                        monitored and changes will be sent to server. \
                        Defaults to False')
    parser.add_argument('-c', '--clipserver', type=str, dest='clipserver',
                        help='URL this server can register itself \
                              to the clipboard-server', default=config['networking']['main_server_address'])
    return parser.parse_args()


if __name__ == "__main__":
    # This guarantees correct relational import of dependencies
    os.chdir(os.path.abspath(os.path.dirname(__file__)))
    args = parse_args()
    q_app = ClipboardServerApp(args.port, args.clipserver, args.domain, args.sync_clipboard, sys.argv)
    q_app.main()
    sys.exit(q_app.exec_())