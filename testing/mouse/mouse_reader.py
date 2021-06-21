from pynput.mouse import Button, Controller as MouseController, Listener

is_p = False

def on_move(x,y):
    if is_p:
        print(f"pressed moved to {x}, {y}")
    else:
        print(f"moved to {x}, {y}")

def on_click(x,y,button,pressed):
    global is_p
    if pressed:
        print(f"clicked at {x}, {y}")
        is_p = True
    else:
        print(f"released at {x}, {y}")
        is_p = False
    # end listener by clicking the right mouse button
    print(pressed)
    if button == Button.right:
        return False

def on_scroll(x,y,dx,dy):
    print(f"scrolled {dx}, {dy}")

#listener = Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll)
#listener.start()

with Listener(
        on_move=on_move,
        on_click=on_click,
        on_scroll=on_scroll) as listener:
    listener.join()