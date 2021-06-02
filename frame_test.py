import Xlib.Xatom
from Xlib import X, display

# https://github.com/alexer/python-xlib-render/blob/86fc1a20292a7d3c913e63b3600da7f09e7b58ff/xutil.py
def match_visual_info(screen, depth, visual_class):
	for depth_info in screen.allowed_depths:
		if depth_info.depth != depth:
			continue
		for visual_info in depth_info.visuals:
			if visual_info.visual_class != visual_class:
				continue
			return visual_info.visual_id

x = 2500
y = 100
width = 500
height = 350
border_width = 5

rects = [(x, y, width, border_width), (x, y, border_width, height), (x, height-border_width, width, border_width), (width-border_width, y, border_width, height)]

dpy = display.Display()
srn = dpy.screen()
root = srn.root

depth = 32
visual = match_visual_info(srn, depth, X.TrueColor)
colormap = root.create_colormap(visual, X.AllocNone)
colormap.alloc_color(255, 1, 1)


window = root.create_window(x, y, width, height, border_width,
                            depth, X.InputOutput, visual,
                            colormap=colormap, border_pixel=0xffffffff,
                            event_mask=X.StructureNotifyMask|X.ExposureMask|X.PropertyChangeMask|X.EnterWindowMask|X.LeaveWindowMask|X.KeyRelease|X.ButtonPress|X.ButtonRelease|X.KeymapStateMask)

# event_mask=X.StructureNotifyMask|X.ExposureMask|X.PropertyChangeMask|X.EnterWindowMask|X.LeaveWindowMask|X.KeyRelease|X.ButtonPress|X.ButtonRelease|X.KeymapStateMask
#X.CWColormap | X.CWBorderPixel | X.CWBackPixel
gc = window.create_gc()

WM_DELETE_WINDOW = dpy.intern_atom("_NET_WM_WINDOW_TYPE_DOCK", False)
WM_PROTOCOLS = dpy.intern_atom("_NET_WM_WINDOW_TYPE", False)
window.change_property(WM_PROTOCOLS, Xlib.Xatom.ATOM, 32, [WM_DELETE_WINDOW], X.PropModeReplace, 1)
#property, type, format, data, mode = X.PropModeReplace, onerror = None
#property, type, format, mode, data, nelements
#window.set_wm_protocols([WM_DELETE_WINDOW])

window.map()
dpy.sync()



while True:
    e = dpy.next_event()
    #if e.type == X.ClientMessage:
        #if e.xclient.message_type == dpy.intern_atom("WM_PROTOCOLS", 1) and e.xclient.data.l[0] == dpy.intern_atom("WM_DELETE_WINDOW", 1):
            #continue
    if e.type == X.Expose:
        window.change_attributes()
        gc.set_clip_rectangles(10, 10, rects, X.YXSorted)
        dpy.sync()
        print("expose")
    elif e.type == X.KeyPress:
        raise SystemExit
