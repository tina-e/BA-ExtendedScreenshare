// orientiert an: https://stackoverflow.com/questions/57078155/draw-border-frame-using-xlib

#include <X11/Xlib.h>
#include <X11/Xutil.h>
#include <X11/Xatom.h>
#include <X11/extensions/shape.h>
#include <X11/extensions/Xfixes.h>
#include <stdio.h>

Display *dpy;
Window w;
GC gc;

XColor red_color;
XColor grey_color;

int x, y, width, height, border;
XInitThreads();

void setup_rect(int rectX, int rectY, int rectWidth, int rectHeight, int borderWidth){
    x = rectX;
    y = rectY;
    width = rectWidth;
    height = rectHeight;
    border = borderWidth;

    dpy = XOpenDisplay(NULL);

    XSetWindowAttributes attr = {0};
    XGCValues gcv = {0};
    XVisualInfo vinfo;

    XMatchVisualInfo(dpy, DefaultScreen(dpy), 32, TrueColor, &vinfo);
    attr.colormap = XCreateColormap(dpy, DefaultRootWindow(dpy), vinfo.visual, AllocNone);
    attr.override_redirect = True;

    char color_code_red[] = "#fc0303";
    XParseColor(dpy, attr.colormap, color_code_red, &red_color);
    XAllocColor(dpy, attr.colormap, &red_color);

    char color_code_grey[] = "#c9c9c9";
    XParseColor(dpy, attr.colormap, color_code_grey, &grey_color);
    XAllocColor(dpy, attr.colormap, &grey_color);

    w = XCreateWindow(dpy, DefaultRootWindow(dpy), 0, 0, width + x + border, height + y + border, 0, vinfo.depth,
                      InputOutput, vinfo.visual, CWColormap | CWBorderPixel | CWBackPixel | CWOverrideRedirect, &attr); // CWOverrideRedirect from ChatGPT
    // ChatGPT
    XSetTransientForHint(dpy, w, RootWindow(dpy, DefaultScreen(dpy)));

    gcv.line_width = borderWidth;
    gc = XCreateGC(dpy, w, GCLineWidth, &gcv);

    XserverRegion region = XFixesCreateRegion (dpy, NULL, 0);
    //XFixesSetWindowShapeRegion (dpy, w, ShapeBounding, 0, 0, 0);
    XFixesSetWindowShapeRegion (dpy, w, ShapeInput, 0, 0, region);
    XFixesDestroyRegion (dpy, region);

    XSelectInput(dpy, w, ExposureMask);
    //long value = XInternAtom(dpy, "_NET_WM_WINDOW_TYPE_DOCK", False);
    long value = XInternAtom(dpy, "_NET_WM_WINDOW_TYPE_UTILITY", False);
    XChangeProperty(dpy, w, XInternAtom(dpy, "_NET_WM_WINDOW_TYPE", False), XA_ATOM, 32, PropModeReplace, (unsigned char *) &value, 1);
    XMapWindow(dpy, w);
    XSync(dpy, False);
}

void draw(int is_visible, int mouse_x, int mouse_y) {
    XClearWindow(dpy, w);
    if(is_visible){
        XSetForeground(dpy, gc, red_color.pixel);
    }
    else{
        XSetForeground(dpy, gc, grey_color.pixel);
    }
    XDrawRectangle(dpy, w, gc, x, y, width, height);
    XFillArc(dpy, w, gc, mouse_x+x, mouse_y+y, 10, 10, 0, 360*64);
    XSync(dpy, False);
}

void end() {
    XDestroyWindow(dpy, w);
    XCloseDisplay(dpy);
}
