'''
from gi.repository import Gtk, Gdk
import cairo

import prototype.Config
attr = Gdk.WindowAttr()
attr.x = 10
attr.y = 10
attr.title = "hello world"

win = Gdk.Window(None, 1, 1, Gdk.WINDOW_TOPLEVEL, event_mask=0, wclass=Gdk.INPUT_ONLY)
win.set_background_rgba(Gdk.RGBA(1, 0.5, 0.5, 0.5))
win.set_pass_through(True)
win.set_title("test")
win.show()
'''

from gi.repository import Gtk, Gdk

overlay = Gtk.Frame(label=None)
overlay.set_screen(Gdk.get_default_root_window().get_screen())



