from ewmh import EWMH
ewmh = EWMH()


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


if __name__ == '__main__':
    found_win = get_win_at(500, 500)
    print(found_win.get_wm_class())





