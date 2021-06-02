from Xlib import X, display
import Xlib.xobject.colormap as colormap
from Xlib.X import CWColormap, CWBorderPixel, CWBackPixel, CWEventMask
import xutil


class Window:
    def __init__(self, display, msg):
        self.display = display
        self.msg = msg

        self.screen = self.display.screen()
        self.window = self.screen.root.create_window(
            10, 10, 100, 100, 1,
            self.screen.root_depth,
            background_pixel=self.screen.white_pixel,
            event_mask=X.ExposureMask | X.KeyPressMask,
        )



        #rq.Pixmap('background_pixmap'),
        #rq.Card32('background_pixel'),
        #rq.Pixmap('border_pixmap'),
        #rq.Card32('border_pixel'),
        #rq.Gravity('bit_gravity'),
        #rq.Gravity('win_gravity'),
        #rq.Set('backing_store', 1,
        #       (X.NotUseful, X.WhenMapped, X.Always)),
        #rq.Card32('backing_planes'),
        #rq.Card32('backing_pixel'),
        #rq.Bool('override_redirect'),
        #rq.Bool('save_under'),
        #rq.Card32('event_mask'),
        #rq.Card32('do_not_propagate_mask'),
        #rq.Colormap('colormap'),
        #rq.Cursor('cursor'),
        #)


        self.gc = self.window.create_gc(
            foreground=self.screen.black_pixel,
            background=self.screen.white_pixel,
        )

        self.window.map()

    def loop(self):
        while True:
            e = self.display.next_event()

            if e.type == X.Expose:
                self.window.fill_rectangle(self.gc, 20, 20, 10, 10)
                self.window.draw_text(self.gc, 10, 50, self.msg)
            elif e.type == X.KeyPress:
                raise SystemExit


class Frame:
    def __init__(self, display, x, y, width, height, border_width):
        self.display = display
        self.screen = self.display.screen()


        #self.screen.allowed_depths.visuals.visual_id = 0
        #self.screen.allowed_depths.visuals.visual_class = X.TrueColor

        #self.colormap = self.screen.root.create_colormap()
        #attr.colormap = XCreateColormap(display, DefaultRootWindow(display), vinfo.visual, AllocNone)
        colormap = self.screen.default_colormap
        #foreground_pixel = colormap.alloc_color(0, 0, 10000).pixel
        #background_pixel = colormap.alloc_color(0, 0, 10000).pixel

        #self.visual_info = self.screen.root.match_visual_info()
        #X. = self.screen.root.create_colormap(visual=X.StaticGray, alloc=1)

        #X.ParseColor(self.display, self.visual_info, "#FF8000")
        #X.TrueColor(self.display, self.visual_info, "#FF8000")

        self.window = self.screen.root.create_window(
            x, y, width, height, border_width,
            self.screen.root_depth,
            X.InputOutput,
            visual=X.TrueColor,
            event_mask=X.CWColormap | X.CWBorderPixel | X.CWBackPixel | CWEventMask,
        )

        #foreground_pixel = colormap.alloc_named_color(foreground_color).pixel

        self.gc = self.window.create_gc()
        wm_delete_window = self.display.intern_atom("WM_DELETE_WINDOW", 0)
        self.window.change_property("_NET_WM_WINDOW_TYPE_TYPE", 32, X.PropModeReplace, wm_delete_window)
        self.window.set_wm_protocols(wm_delete_window, 1)

        self.window.map()


    def loop(self):
        while True:
            e = self.display.next_event()

            if e.type == X.ClientMessage:
                if e.xclient.message_type == self.display.intern_atom("WM_PROTOCOLS", 1) and e.xclient.data.l[0] == self.display.intern_atom("WM_DELETE_WINDOW", 1):
                    continue
                #self.display.set_foreground(self.gc,)
                #self.display.fill_rectangles(self.gc, )
                #self.display.fill_rectangles(self.gc, )
                #self.window.sync(self.gc, False)
            elif e.type == X.KeyPress:
                raise SystemExit



if __name__ == "__main__":
    #Window(display.Display(), "Hello, World!").loop()
    Frame(display.Display(), 0, 0, 100, 100, 1).loop()