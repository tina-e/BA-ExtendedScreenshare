import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gst', '1.0')

from gi.repository import Gtk, Gst
Gst.init(None)
Gst.init_check(None)

class GstWidget(Gtk.Box):
    def __init__(self, pipeline):
        super().__init__()
        self.connect('realize', self._on_realize)
        self._bin = Gst.parse_bin_from_description(pipeline, True)

    def _on_realize(self, widget):
        pipeline = Gst.Pipeline()
        factory = pipeline.get_factory()
        gtksink = factory.make('gtksink')
        pipeline.add(self._bin)
        pipeline.add(gtksink)

        self._bin.link(gtksink)
        self.pack_start(gtksink.props.widget, True, True, 0)
        gtksink.props.widget.show()
        pipeline.set_state(Gst.State.PLAYING)


STREAM_PORT = 5000
RECEIVER_ADDRESS = '192.168.178.136'
win = Gtk.ApplicationWindow()
#widget = GstWidget('videotestsrc')
widget = GstWidget(f"udpsrc address={RECEIVER_ADDRESS} port={STREAM_PORT} "
               "caps = \"application/x-rtp, media=(string)video, "
               "clock-rate=(int)90000, encoding-name=(string)H264, "
               "payload=(int)96\" ! rtph264depay ! decodebin  ! videoconvert")

win.add(widget)
win.show_all()


def on_destroy(win):
    Gtk.main_quit()

win.connect('destroy', on_destroy)

Gtk.main()

# nichts passiert

#https://riptutorial.com/gtk3/example/24777/embed-a-video-in-a-gtk-window-in-python3
