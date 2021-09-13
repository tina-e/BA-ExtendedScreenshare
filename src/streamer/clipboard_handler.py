import sys
import pyclip
from PyQt5.QtCore import QMimeData, QUrl
from PyQt5.QtWidgets import QApplication

from src.event_types import EventTypes


class ClipboardHandler:
    def __init__(self, mouse_handler):
        self.mouse_handler = mouse_handler
        self.app = QApplication(sys.argv)

    def on_copy(self, sock, rec_addr, port):
        stored_is_file, stored_content = self.read_clipboard()
        self.mouse_handler.simulate_copy()
        _, content_for_remote = self.read_clipboard()
        message = EventTypes.COPY.to_bytes(1, 'big')
        message += content_for_remote
        sock.sendto(message, (rec_addr, port))
        self.write_clipboard(stored_is_file, stored_content)
        
    def read_clipboard(self):
        is_file = False
        content = pyclip.paste()
        if self.app.clipboard().mimeData().hasUrls():
            is_file = True
            content = content.decode('utf-8').split('file://', 1)[1]
        return is_file, content
    
    def write_clipboard(self, is_file, content):
        if is_file:
            data = QMimeData()
            url = QUrl.fromLocalFile(content)
            data.setUrls([url])
            self.app.clipboard().setMimeData(data)
        else:
            pyclip.copy(content)

    def on_paste(self, incoming_content):
        stored_is_file, stored_content = self.read_clipboard()
        pyclip.copy(incoming_content)
        self.mouse_handler.simulate_paste()
        self.write_clipboard(stored_is_file, stored_content)
