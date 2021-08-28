from gi.repository import Gtk, Gdk
import cairo

import prototype.Config_alt


class Example(Gtk.Window):

    def __init__(self):
        super(Example, self).__init__()

        self.tran_setup()
        self.init_ui()

    def init_ui(self):
        self.connect("draw", self.on_draw)
        self.resize(prototype.Config_alt.END_X - prototype.Config_alt.START_X, prototype.Config_alt.END_Y - prototype.Config_alt.START_Y)
        self.move(prototype.Config_alt.START_X, prototype.Config_alt.START_Y)

        frame = Gtk.Frame(label=None)
        self.add(frame)
        print(frame.get_parent())
        self.set_decorated(False)

        self.connect("delete-event", Gtk.main_quit)
        self.set_type_hint(Gdk.WindowTypeHint.UTILITY)
        self.set_keep_above(True)
        self.show_all()

        #self.set_resizable(True)

    def tran_setup(self):
        self.set_app_paintable(True)
        screen = self.get_screen()

        visual = screen.get_rgba_visual()
        if visual != None and screen.is_composited():
            self.set_visual(visual)

    def on_draw(self, wid, cr):
        cr.set_source_rgba(0.2, 0.2, 0.2, 0.1)
        cr.set_operator(cairo.OPERATOR_SOURCE)
        cr.paint()


def main():
    app = Example()
    Gtk.main()


if __name__ == "__main__":
    main()

