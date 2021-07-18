import threading
import time

from streamer.streamer import Streamer
from viewer.viewer import Viewer

import Config
import subprocess


streamer = None
viewer = None


def reattach_back():
    if Config.IS_STREAMER:
        #mouse_id = subprocess.check_output(f"xinput list --id-only '{Config.MOUSE_DEVICE_STREAMER_POINT.name}'", shell=True).strip().decode()
        #scroll_id = subprocess.check_output(f"xinput list --id-only 'pointer:{Config.MOUSE_DEVICE_STREAMER_CLICK.name}'", shell=True).strip().decode()
        #click_id = subprocess.check_output(f"xinput list --id-only 'keyboard:{Config.MOUSE_DEVICE_STREAMER_CLICK.name}'", shell=True).strip().decode()
        #key_id = subprocess.check_output(f"xinput list --id-only '{Config.KEYBOARD_DEVICE_STREAMER.name}'", shell=True).strip().decode()

        standard_master_pointer_id = subprocess.check_output("xinput list --id-only 'master pointer'", shell=True).strip().decode()
        #subprocess.check_output(f"xinput reattach {mouse_id} {standard_master_pointer_id}", shell=True)
        #subprocess.check_output(f"xinput reattach {scroll_id} {standard_master_pointer_id}", shell=True)

        #standard_master_keyboard_id = subprocess.check_output("xinput list --id-only 'Virtual core keyboard",shell=True).strip().decode()
        #subprocess.check_output(f"xinput reattach {click_id} {standard_master_keyboard_id}", shell=True)
        #subprocess.check_output(f"xinput reattach {key_id} {standard_master_keyboard_id}", shell=True)
        subprocess.check_output(f"xinput remove-master {standard_master_pointer_id}", shell=True)
    else:
        viewer.end_stream()

if Config.IS_STREAMER:
    #signal.signal(signal.SIGINT, reattach_back)
    streamer = Streamer()

else:
    #signal.signal(signal.SIGINT, reattach_back)
    viewer = Viewer()
    viewer.access_stream()
    # event_thread = threading.Thread(target=start_event_sender)
    # event_thread.daemon = True
    # event_thread.start()




while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        reattach_back()
        break

