# simulating mouse events: https://nitratine.net/blog/post/simulate-mouse-events-in-python/
from pynput.keyboard import Key, Controller as KeyboardController
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


mouse = MouseController()
mouse.position = (100, 100)
mouse.move(1000, 400)
mouse.press(Button.left)
mouse.move(300, 1)
mouse.release(Button.left)
#mouse.scroll(0, 2)

#keybd = KeyboardController()