import socket
import threading
import Config


class Receiver:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((Config.STREAMER_ADDRESS, Config.EVENT_PORT))
        connection_thread = threading.Thread(target=self._receive)
        connection_thread.start()

    def _receive(self):
        _receiving = True
        while _receiving:
            data, addr = self.sock.recvfrom(1024)
            try:
                data_decoded = data.decode()
                print(data_decoded)
                #TODO: verarbeite event
            except UnicodeDecodeError:
                continue
