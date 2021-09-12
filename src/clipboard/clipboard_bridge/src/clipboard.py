import copy
from json import dumps
import re

from PyQt5.QtCore import pyqtSignal, QMimeData, QObject


class Clipboard(QObject):
    """
    This class acts as an intermediary between the core
    and the clipboard of the system.
    Internally it currently uses the QClipboard provided by
    the running QApplication.
    This clipoard needs to be provided in __init__.
    This class was introduced to provide the ability for further enhancement
    of the clipboard that might be needed further down the line.
    It will probably also be used to monitor the current state
    of the system-clipboard and notify the core of any occurring changes
    so those changes can be synced up with the remote-clipboard
    """
    clipboard_changed_signal = pyqtSignal(list)

    def _prepare_data(self, data):
        """
        If the data is a str, it encodes it to bytes.
        """
        if type(data) is str:
            data = data.encode(encoding='utf8')
        elif type(data) is dict:  # JSON received
            data = dumps(data)
            data = data.encode(encoding='utf8')
        else:
            data = bytes(data)
        return data

    def _is_mime_type(self, mime_string):
        """
        Checks if mime_string is a valid Mimetype
        """
        return self.mime_pattern.match(mime_string)

    def _get_data_in_clipboard(self):
        """
        Creates a deep copy of the current clipboard contents and then
        clears it. This enables this program to take ownership of the cb
        without data being lost. After that, it can insert data on its whim.
        Otherwise, no additional data can be inserted into the clipboard!
        """
        mime_data = QMimeData()
        src = self.clipboard.mimeData()
        for mt in src.formats():
            mime_data.setData(mt, copy.deepcopy(src.data(mt)))
        self.clipboard.clear()
        return mime_data

    def save(self, data):
        """
        Parses the data to a String (only for the current implementation)
            and saves it in the system's clipboard
        :param data: The data that will be saved in the clipboard
        """
        mime_type = data['mimetype']

        # Create new mime data, when parent is incoming, else add mime type to existing data
        if data['parent'] is None:
            self.mime_data = QMimeData()
        else:
            self.mime_data = self.clipboard.mimeData()

        prepared_data = self._prepare_data(data['data'])

        self.mime_data.setData(mime_type, prepared_data)

        self.clipboard.clear()
        self.clipboard.setMimeData(self.mime_data)

        if data['parent'] is not None:  # If child gotten first, should not happen
            self.current_id = data['parent']
        else:
            self.current_id = data['_id']

        if not self.clipboard.text():
            return -1
        else:
            return 1

    def update(self, data):
        """
        Updates the content of the clipboard. If an update happend to data
        from this clipboard, the app will take ownership of the clipboard
        first. This can happen when the data from THIS clipboard was changed
        by a local application and the data was then sent to the remote server
        via onDataChanged. If a webhook from the remote server then modified
        the data, it will be sent back to THIS clipboard and one needs to
        insert it (which needs ownership of the cb)
        """
        if not self.clipboard.ownsClipboard():
            mime_data = self._get_data_in_clipboard()
        else:
            mime_data = self.clipboard.mimeData()
        mime_type = data['mimetype']
        prepared_data = self._prepare_data(data['data'])
        mime_data.setData(mime_type, prepared_data)
        self.clipboard.setMimeData(mime_data)

    def onDataChanged(self):
        """
        Called when the data of the clipboard has changed.
        All data with valid mimetypes will be saved and then given to the
        local server so it can forward them to the remote clip-server
        """
        # if change was triggerd by inserting data received from server
        if self.clipboard.ownsClipboard():
            return
        mime_data = self.clipboard.mimeData()
        data = []
        for dt in mime_data.formats():
            if self._is_mime_type(dt) and ';charset=' not in dt:
                clip_data = mime_data.data(dt).data()
                if clip_data:
                    # Various images formats are often empty, maybe some
                    # implicit conversion on OS-level is supposed to provide
                    data.append({
                        'mimetype': dt,
                        'data': clip_data
                    })
        self.clipboard_changed_signal.emit(data)

    def __init__(self, clip, sync_clipboard):
        """
        :param clip: The QClipboard of the current QApplication
        """
        super(QObject, self).__init__()
        self.clipboard = clip
        self.current_id = ''
        self.mime_data = QMimeData()
        # https://tools.ietf.org/html/rfc6838#section-4.2
        self.mime_pattern = re.compile(
                '^([a-zA-Z1-9][a-zA-Z1-9!#$&-^.+]{0,126})'
                + '/'
                + '([a-zA-Z1-9][a-zA-Z1-9!#$&-^.+]{0,126})$')
        if sync_clipboard:
            self.clipboard.dataChanged.connect(self.onDataChanged)
