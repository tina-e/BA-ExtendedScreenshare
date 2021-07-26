import time

from ewmh import EWMH
ewmh = EWMH()
import Xlib


def frame(window):
    framed_window = window
    while framed_window.query_tree().parent != ewmh.root:
        framed_window = framed_window.query_tree().parent
    return framed_window


def get_win_geo(window):
    return frame(window).get_geometry()


def get_open_windows():
    running_wins = ewmh.getClientListStacking()
    open_wins = []
    for window in running_wins:
        window_states = ewmh.getWmState(window, 'NET_WM_STATES')
        if '_NET_WM_STATE_HIDDEN' not in window_states and '_NET_WM_STATE_STICKY' not in window_states:
            open_wins.append(window)
    return open_wins


def get_win_at(x, y):
    for window in reversed(get_open_windows()):
        if (get_win_geo(window).x <= x <= get_win_geo(window).width) and (
                get_win_geo(window).y <= y <= get_win_geo(window).height):
            return window
    return None


for i, win in enumerate(get_open_windows()):
    print(i, win.get_wm_class())
    print(win.get_geometry())
    print(frame(win).get_geometry())
#if __name__ == '__main__':
#    found_win = get_win_at(100, 100)
#
#    print(found_win.id)
#    #print(found_win.display)
#    print(found_win)
#    print(found_win.get_attributes())
#    print(found_win.get_wm_class())
#    print("uii")
#    print(found_win.query_tree().parent.get_wm_class())
#    for child in found_win.query_tree().children:
#        print(child.get_geometry())






