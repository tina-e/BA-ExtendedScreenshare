import sys

from PyQt5.QtCore import QObject, pyqtSlot

from clipboard import Clipboard
import html2text


class ClipboardHandler(QObject):
    """
    This class is responsible for taking data from other programs,
    plugins etc and save them to the clipboard
    and also forwards the data to the server
    It also retrieves data from the server and can return it
    """
    # A Clipboard from this package, used for changing the local clipboard
    clipboard = None

    def _save_to_local_clipboard(self, data):
        """
        Saves data to the local clipboard. Uses a QClipboard
        :param data: Data to be saved
        """

        ''' the follwing part removes any formatting of the clipboard content
        without this, only non-formatted content can be pasted remote - ME '''
        plain = html2text.html2text(data['data'].decode('iso-8859-1'))
        plain = plain.rstrip('\n')
        if data['mimetype'] == 'application/x-gtk-text-buffer-rich-text' and plain.startswith('GTK'):
            plain = plain.split(' ', 1)[1]
        data['data'] = plain.encode('utf-8')
        data['mimetype'] = 'text/plain'
        '''end ME'''

        self.clipboard.save(data)

    def put_into_storage(self, data):
        """
        Responsible for storing data on a higher level.
        This function should be called when you want to save
        data in your clipboard and on the server simultaneously
        :param data: The data to be saved
        """
        if data.get('parent') and data['parent'] == self.clipboard.current_id:
            # Child of current item, add alternative
            self.clipboard.update(data)
        else:
            self._save_to_local_clipboard(data)

    def __init__(self, q_app, sync_clipboard):
        """
        :param q_app: The current QApplication this package is part
        of running in
        :param sync_clipboard: Instructs the clipboard whether or not
        it should monitor its contents and notify on change
        """
        self.clipboard = Clipboard(q_app.clipboard(), sync_clipboard)
