import sys
import threading
from streamer import Streamer
from accessor import Accessor
from event_receiver import Receiver
from event_sender import Sender
import Config
import subprocess
import signal


def start_stream():
    streamer = Streamer()
    streamer.open_stream()
    streamer.start_stream()

def access_stream():
    accessor = Accessor()
    accessor.access_stream()


#def start_host():
    # server = Server()
    # server.start()

#def start_client():
    # client = Client()
    # client.connect()
    # client.listen_on_device()
    # client.listen_on_device_abs()


def start_event_receiver():
    rec = Receiver()

def start_event_sender():
    sen = Sender()

def reattach_back():
    print("test")
    if Config.IS_STREAMER:
        mouse_id = subprocess.check_output(f"xinput list --id-only '{Config.MOUSE_DEVICE_STREAMER_POINT.name}'", shell=True).strip().decode()
        scroll_id = subprocess.check_output(f"xinput list --id-only 'pointer:{Config.MOUSE_DEVICE_STREAMER_CLICK.name}'", shell=True).strip().decode()
        click_id = subprocess.check_output(f"xinput list --id-only 'keyboard:{Config.MOUSE_DEVICE_STREAMER_CLICK.name}'", shell=True).strip().decode()
        key_id = subprocess.check_output(f"xinput list --id-only '{Config.KEYBOARD_DEVICE_STREAMER.name}'", shell=True).strip().decode()

        standard_master_pointer_id = subprocess.check_output("xinput list --id-only 'Virtual core pointer", shell=True).strip().decode()
        subprocess.check_output(f"xinput reattach {mouse_id} {standard_master_pointer_id}", shell=True)
        subprocess.check_output(f"xinput reattach {scroll_id} {standard_master_pointer_id}", shell=True)

        standard_master_keyboard_id = subprocess.check_output("xinput list --id-only 'Virtual core keyboard",shell=True).strip().decode()
        subprocess.check_output(f"xinput reattach {click_id} {standard_master_keyboard_id}", shell=True)
        subprocess.check_output(f"xinput reattach {key_id} {standard_master_keyboard_id}", shell=True)
    sys.exit(0)



if Config.IS_STREAMER:
    #threading.Thread(target=start_host).start()
    threading.Thread(target=start_event_receiver())
    threading.Thread(target=start_stream).start()
    signal.signal(signal.SIGINT, reattach_back) #TODO: Fehlermeldung, reattach_back() wird nicht ausgeführt
else:
    access_stream()
    print("stream running")
    #start_client()
    threading.Thread(target=start_event_sender).start()
    signal.signal(signal.SIGINT, reattach_back)
    #threading.Thread(target=start_client).start()
    #threading.Thread(target=access_stream).start()



