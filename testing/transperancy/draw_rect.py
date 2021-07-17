#!/usr/bin/python

'''
ZetCode PyCairo tutorial

This code example shows how to
create a transparent window.

author: Jan Bodnar
website: zetcode.com
'''

# https://zetcode.com/gfx/pycairo/root/

from gi.repository import Gtk
import cairo


class Example(Gtk.Window):

    def __init__(self):
        super(Example, self).__init__()

        self.tran_setup()
        self.init_ui()

    def init_ui(self):
        self.connect("draw", self.on_draw)

        self.set_title("Transparent window")
        self.resize(300, 250)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.connect("delete-event", Gtk.main_quit)
        self.show_all()

    def tran_setup(self):
        self.set_app_paintable(True)
        screen = self.get_screen()

        visual = screen.get_rgba_visual()
        if visual != None and screen.is_composited():
            self.set_visual(visual)

    def on_draw(self, wid, cr):
        cr.set_source_rgba(0.2, 0.2, 0.2, 0.4)
        cr.set_operator(cairo.OPERATOR_SOURCE)
        cr.paint()


def main():
    app = Example()
    Gtk.main()


if __name__ == "__main__":
    main()

