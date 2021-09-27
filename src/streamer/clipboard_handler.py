import sys
import threading
import time
import pyclip
import pyautogui
import subprocess
from PyQt5.QtCore import QMimeData, QUrl
from PyQt5.QtWidgets import QApplication
from event_types import EventTypes


class ClipboardHandler:
    '''
    This class handles clipboard actions from the receiver.
    Streamer's clipboard content is caches while performing receiver's copy- oder paste-actions.
    '''
    def __init__(self, mouse_handler, lock):
        self.mouse_handler = mouse_handler
        self.app = QApplication(sys.argv)
        self.lock = lock

    def on_copy(self, sock, rec_addr, port):
        '''
        Current clipboard content is stored until receiver's copy action is done.
        mouse_handler simulates a copy-action of the selected content.
        This content will be send back to him/her.
        Streamer's clipboard content is copied again to the clipboard.
        :param sock: active socket for event communication
        :param rec_addr: receiver's address
        :param port: event port
        '''
        stored_is_file, stored_content = self.read_clipboard()
        self.mouse_handler.simulate_copy()
        _, content_for_remote = self.read_clipboard()
        message = EventTypes.COPY.to_bytes(1, 'big')
        message += content_for_remote
        sock.sendto(message, (rec_addr, port))
        self.write_clipboard(stored_is_file, stored_content)
        
    def read_clipboard(self):
        '''
        :return: contains the clipboard a file currently?, current content of the clipboard
        '''
        with self.lock:
            is_file = False
            content = pyclip.paste()
            if self.app.clipboard().mimeData().hasUrls():
                is_file = True
                content = content.decode('utf-8').split('file://', 1)[1]
            return is_file, content
    
    def write_clipboard(self, is_file, content):
        '''
        Copies the given content in the clipboard.
        If the given content is a path to a file, QClipboard is used; else pyclip copies the text to the clipboard
        :param is_file: is the given content a path to a file which needs to be written in the clipboard?
        :param content: content or path to be written in the clipboard
        '''
        if is_file:
            data = QMimeData()
            url = QUrl.fromLocalFile(content)
            data.setUrls([url])
            self.app.clipboard().setMimeData(data)
        else:
            pyclip.copy(content)

    def on_paste(self, incoming_content):
        '''
        Current clipboard content is stored until receiver's copy action is done.
        Content received is copied to the clipboard and mouse_handler simulates a paste-action.
        Streamer's clipboard content is copied again to the clipboard.
        :param incoming_content: received content that needs to be pasted
        '''
        with self.lock:
            stored_is_file, stored_content = self.read_clipboard()
            pyclip.copy(incoming_content)
            self.mouse_handler.simulate_paste()
            self.write_clipboard(stored_is_file, stored_content)

    def on_drop(self, path_to_file, drop_x, drop_y):
        '''
        Simualtes a drop-event with xcopy:
        xcopy drops a file from given file path to a clicked position.
        xcopy only supports the real cursor, no virtual input devices.
        So we need to move the local cursor to the drop-position and simulate a click.
        Re-moving the local cursor to the previous position
        :param path_to_file: path to file which should be dropped
        :param drop_x: x_pos of drop
        :param drop_y: y_pos of drop
        '''
        current_x, current_y = pyautogui.position()
        subprocess.Popen(f"xcopy -D {path_to_file}", shell=True)  # unterstuetzt nur text we guess
        time.sleep(0.1)  # required, else: no drop happens
        pyautogui.moveTo(drop_x, drop_y)
        pyautogui.mouseDown()
        time.sleep(0.1)  # required, else: no drop happens
        pyautogui.mouseUp()
        pyautogui.moveTo(current_x, current_y)


