from threading import Thread
import time

# https://www.youtube.com/watch?v=HDY8pf-b1nA
import gi
gi.require_version("Gst", "1.0")
gi.require_version("GstApp", "1.0")
from gi.repository import Gst, GLib, GstApp

Gst.init()

reciever_ip = "192.168.178.169"
port = "5000"
start_x = 50
start_y = 50
end_x = 800
end_y = 750

main_loop = GLib.MainLoop()
main_loop_thread = Thread(target=main_loop.run)
main_loop_thread.start()

# ! video/x-raw,width=750,height=500   legt größe des streams fest
# use-damage=0 angeblich CPU fordernd
# ximageslink creates window for output (glimagesink also possible, higher CPU required)
# ! videoscale method=0, auch wieder CPU sache scheinbar
# pipeline = Gst.parse_launch("ximagesrc startx=100 starty=10 endx=800 endy=800 ! video/x-raw,framerate=30/1 ! ximagesink")

# https://gist.github.com/esrever10/7d39fe2d4163c5b2d7006495c3c911bb
# gst-launch-1.0 -v ximagesrc startx=50 starty=10 endx=800 endy=800 ! video/x-raw,framerate=20/1 ! videoscale ! videoconvert ! x264enc tune=zerolatency bitrate=500 speed-preset=superfast ! rtph264pay ! udpsink host=192.168.178.169 port=5111
pipeline = Gst.parse_launch(f"ximagesrc startx={start_x} starty={start_y} endx={end_x} endy={end_y} "
                            "! video/x-raw,framerate=20/1 "
                            "! videoscale "
                            "! videoconvert "
                            "! x264enc tune=zerolatency bitrate=500 speed-preset=superfast "
                            "! rtph264pay "
                            f"! udpsink host={reciever_ip} port={port}")
print(pipeline)
print(type(pipeline))
pipeline.set_state(Gst.State.PLAYING)
# pipeline = Gst.parse_launch("ximagesrc startx=100 starty=10 endx=800 endy=800 ! video/x-raw,framerate=30/1 ! videoconvert ! x264enc ! rtph264pay config-interval=10 pt=96 ! udpsink host=192.168.178.136 host=8500")

# pipeline = Gst.parse_launch("rtpmp4vpay ! decodebin ! videoconvert ! autovideosink")
# pipeline = Gst.parse_launch("v4l2src ! decodebin ! videoconvert ! appsink name=sink")
# appsink = pipeline.get_by_name("sink")
# pipeline.set_state(Gst.State.PLAYING)

try:
    while True:
        time.sleep(0.1)
        #sample = appsink.try_pull_sample(Gst.SECOND)
        #if sample is None:
        #    continue
        #print("sample")
except KeyboardInterrupt:
    pass

pipeline.set_state(Gst.State.NULL)
main_loop.quit()
main_loop_thread.join()





# https://stackoverflow.com/questions/43777428/capture-gstreamer-network-video-with-python
