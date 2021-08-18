import os
import sys
from server import Server
from configparser import ConfigParser
from argparse import ArgumentParser
from persistence.persistence import Persistence

"""
This class is responsible for starting the whole application.
It initializes the database first and then builds the configuration
for the Flask server
"""

if __name__ == "__main__":
    config = ConfigParser()
    argparser = ArgumentParser()
    os.chdir(os.path.abspath(os.path.dirname(__file__)))
    config.read('./../config/config.ini')
    argparser.add_argument("-p", '--port',
                    help="The port used for providing the server.",
                    default=config['networking']['port'])
    args, unknown = argparser.parse_known_args()

    db = Persistence()
    flask_server = Server(__name__, db, args.port)
    flask_server.start()