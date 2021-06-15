from xdo import Xdo
import subprocess
import Xlib.display
from Xlib import X
from ewmh import EWMH

def get_win_at(x, y):
    window_ids = read_window_ids(False)
    geo_dict = get_geometry_window_pairs(window_ids)
    return find_window_at_position(geo_dict, x, y)


def read_window_ids(incluede_minimized):
    command = 'xdotool search --all --onlyvisible --desktop $(xprop -notype -root _NET_CURRENT_DESKTOP | cut -c 24-) "" 2>/dev/null'
    window_ids_byte = subprocess.check_output(command, shell=True).split(b'\n')
    window_ids_byte.pop(-1)

    window_ids = []
    for id in window_ids_byte:
        id = id.decode("utf-8")

        if incluede_minimized:
            window_ids.append(id)
        else:
            checker = subprocess.check_output('xprop -id ' + id + ' | grep "_NET_WM_STATE(ATOM)"', shell=True)
            if "HIDDEN" not in str(checker):
                window_ids.append(id)
        #Todo: z coordinates

    return window_ids


def get_geometry_window_pairs(window_ids):
    dict = {}
    for window in window_ids:
        command = 'xdotool getwindowgeometry ' + str(window)
        geometry_data = subprocess.check_output(command, shell=True).decode("utf-8").split("\n")
        geometry_data = geometry_data[1:-1]
        geometry_data = [elem.split(" ")[3].strip() for elem in geometry_data]

        x = int(geometry_data[0].split(",")[0])
        y = int(geometry_data[0].split(",")[1])
        width = int(geometry_data[1].split("x")[0])
        height = int(geometry_data[1].split("x")[1])

        dict[window] = [x, y, width, height]
        #print(dict)
    return dict


def find_window_at_position(geo_dict, x, y):
    found_windows = []
    for window in geo_dict:
        if (geo_dict.get(window)[0] <= x <= geo_dict.get(window)[2]) and (geo_dict.get(window)[1] <= y <= geo_dict.get(window)[3]):
            found_windows.append(window)
    return found_windows


#display = Xlib.display.Display()
#root = display.screen().root
#open_windows = root.query_tree()
#print(open_windows)


def try_commands(window_ids):
    import time
    for window in window_ids:
        command = 'xdotool windowmove ' + str(window) + ' 0 0'
        command = 'xdotool windowminimize ' + str(window)
        #command = 'xdotool windowraise ' + str(window)
        subprocess.Popen(command, shell=True)
        time.sleep(1)