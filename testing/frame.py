# rewritten for python from c-code: https://stackoverflow.com/questions/23074054/why-i-set-xlib-window-background-transparent-failed
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
border_width = 50

rects = [(x, y, width, border_width), (x, y, border_width, height), (x, height-border_width, width, border_width), (width-border_width, y, border_width, height)]

dpy = display.Display()
srn = dpy.screen()
root = srn.root

depth = 32
visual = match_visual_info(srn, depth, X.TrueColor)
colormap = root.create_colormap(visual, X.AllocNone)
#colormap.alloc_color(255, 1, 1)


window = root.create_window(x, y, width, height, border_width,
                            depth, X.InputOutput, visual,
                            event_mask=X.StructureNotifyMask | X.CWColormap | X.CWBorderPixel | X.CWBackPixel,
                            border_pixel=200, background_pixel=0, colormap=colormap)


# event_mask=X.StructureNotifyMask|X.ExposureMask|X.PropertyChangeMask|X.EnterWindowMask|X.LeaveWindowMask|X.KeyRelease|X.ButtonPress|X.ButtonRelease|X.KeymapStateMask
#X.CWColormap | X.CWBorderPixel | X.CWBackPixel
gc = window.create_gc()

wm_delete_window = dpy.intern_atom("WM_DELETE_WINDOW", 0)
window.set_wm_protocols([wm_delete_window], 1)

window.map()

while True:
    e = dpy.next_event()
    if e.type == X.ClientMessage:
        if e.xclient.message_type == dpy.intern_atom("WM_PROTOCOLS", 1) and e.xclient.data.l[0] == dpy.intern_atom("WM_DELETE_WINDOW", 1):
            break