import threading

from pynput.mouse import Button, Controller
from ewmh import EWMH
ewmh = EWMH()

#lock = threading.Lock()

def is_in_focus():
    window = ewmh.getActiveWindow()
    #return window.get_wm_class() == ('gst-launch-1.0', 'GStreamer')
    return window.get_wm_class() == ('jetbrains-pycharm-ce', 'jetbrains-pycharm-ce')


def frame(window):
    framed_window = window
    while framed_window.query_tree().parent != ewmh.root:
        framed_window = framed_window.query_tree().parent
    return framed_window


def is_stream_open():
    open_wins = ewmh.getClientList()
    for win in open_wins:
        #if win.get_wm_class() == ('gst-launch-1.0', 'GStreamer'):
        if win.get_wm_class() == ('jetbrains-pycharm-ce', 'jetbrains-pycharm-ce'):
            return True
    return False


def get_pos_in_stream(x, y):
    #with lock:
    win_geo = None
    open_wins = ewmh.getClientList()
    for win in open_wins:
        # if win.get_wm_class() == ('gst-launch-1.0', 'GStreamer'):
        if win.get_wm_class() == ('jetbrains-pycharm-ce', 'jetbrains-pycharm-ce'):
            win_geo = frame(win).get_geometry()
            break
    rel_x = x - win_geo.x
    rel_y = y - win_geo.y - win_geo.depth
    if 0 <= rel_x <= win_geo.width and 0 <= rel_y <= win_geo.height:
        return rel_x, rel_y
    print("cursor out of stream")
    return None, None

###########################################################################


def is_relevant_input():
    window = ewmh.getActiveWindow()
    # if window.get_wm_class() == ('gst-launch-1.0', 'GStreamer'):
    if window.get_wm_class() == ('jetbrains-pycharm-ce', 'jetbrains-pycharm-ce'):
        mouse_pos = Controller().position
        win_geo = frame(window).get_geometry()
        if (win_geo.x <= mouse_pos[0] <= (win_geo.width + win_geo.x)) and (win_geo.y <= mouse_pos[1] <= (win_geo.height + win_geo.y)):
            return True
    return False