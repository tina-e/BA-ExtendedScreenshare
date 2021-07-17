#include <X11/Xlib.h>
#include <X11/Xutil.h>
#include <X11/Xatom.h>

#define W_WIDTH 640
#define W_HEIGHT 480

#define X_POS 100
#define Y_POS 120
#define BORDER_WIDTH 2

int main(int argc, char *argv[]) {
    XRectangle rectangles[4] = {
        { X_POS, Y_POS, W_WIDTH, BORDER_WIDTH },
        { X_POS, Y_POS, BORDER_WIDTH, W_HEIGHT },
        { X_POS, W_HEIGHT - BORDER_WIDTH, W_WIDTH, BORDER_WIDTH },
        { W_WIDTH - BORDER_WIDTH, Y_POS, BORDER_WIDTH, W_HEIGHT }
    };
    Display *dpy = XOpenDisplay(NULL);
    XSetWindowAttributes attr = {0};
    XGCValues gcv = {0};
    XVisualInfo vinfo;
    GC gc;

    Window w;

    int run = 1;

    XMatchVisualInfo(dpy, DefaultScreen(dpy), 32, TrueColor, &vinfo);
    attr.colormap = XCreateColormap(dpy, DefaultRootWindow(dpy), vinfo.visual, AllocNone);

    XColor color;
    char orangeDark[] = "#FF8000";
    XParseColor(dpy, attr.colormap, orangeDark, &color);
    XAllocColor(dpy, attr.colormap, &color);

    w = XCreateWindow(dpy, DefaultRootWindow(dpy), X_POS, Y_POS,
                      W_WIDTH, W_HEIGHT, BORDER_WIDTH, vinfo.depth,
                      InputOutput, vinfo.visual, CWColormap | CWBorderPixel | CWBackPixel, &attr);

    gcv.line_width = BORDER_WIDTH;
    gc = XCreateGC(dpy, w, GCLineWidth, &gcv);

    XSelectInput(dpy, w, ExposureMask);
    long value = XInternAtom(dpy, "_NET_WM_WINDOW_TYPE_DOCK", False);
    XChangeProperty(dpy, w, XInternAtom(dpy, "_NET_WM_WINDOW_TYPE", False),
                    XA_ATOM, 32, PropModeReplace, (unsigned char *) &value, 1);
    XMapWindow(dpy, w);
    XSync(dpy, False);

    while(run) {
        XEvent xe;
        XNextEvent(dpy, &xe);
        switch (xe.type) {
            case Expose:
                XSetForeground(dpy, gc, color.pixel);
                XDrawRectangles(dpy, w, gc, rectangles, 4);
                XFillRectangles(dpy, w, gc, rectangles, 4);
                XSync(dpy, False);
                break;

            default:
                break;
        }
    }

    XDestroyWindow(dpy, w);
    XCloseDisplay(dpy);

    return 0;
}
/*https://stackoverflow.com/questions/57078155/draw-border-frame-using-xlib*/