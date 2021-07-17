# https://stackoverflow.com/questions/63606306/pycairo-how-to-correctly-instance-cairo-xlibsurface

import gi
gi.require_versions({
    'Gdk':  '3.0',
    'Gtk':  '3.0',
    'Wnck': '3.0',
    'Gst':  '1.0',
    'AppIndicator3': '0.1',
})

from gi.repository import Gtk, Gdk
import cairo


class Example(Gtk.Window):

    def __init__(self):
        super(Example, self).__init__()

        self.tran_setup()
        self.init_ui()

    def init_ui(self):
        self.connect("draw", self.on_draw)
        # self.set_title("Transparent window")
        self.resize(300, 250)
        self.set_position(Gtk.WindowPosition.NONE)
        self.move(0, 40)
        self.connect("delete-event", Gtk.main_quit)

        # The magic is here
        self.set_type_hint(Gdk.WindowTypeHint.COMBO)
        self.set_keep_above(True)
        self.show_all()


    def tran_setup(self):
        self.set_app_paintable(True)
        screen = self.get_screen()

        #print(self.get_type_hint())

        visual = screen.get_rgba_visual()
        if visual != None and screen.is_composited():
            self.set_visual(visual)

    def on_draw(self, wid, cr):
        cr.set_source_rgba(0.2, 0.2, 0.2, 0.4)
        cr.set_operator(cairo.OPERATOR_SOURCE)
        cr.paint()

        cr.set_source_rgb(0.6, 0.6, 0.6)

        cr.rectangle(20, 20, 120, 80)
        cr.fill()

        self.draw(cr)

    def draw(self, cr):
        cr.set_source_rgb(0, 256, 256)
        cr.rectangle(180, 20, 80, 80)
        cr.fill()


def main():
    app = Example()
    Gtk.main()


if __name__ == "__main__":
    main()