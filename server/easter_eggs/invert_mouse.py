import threading
import time
import pyautogui

def invert_mouse():
    inverted = True
    start_time = time.time()

    def move_mouse():
        while inverted:
            x, y = pyautogui.position()
            screen_width, screen_height = pyautogui.size()
            new_x = screen_width - x
            new_y = screen_height - y
            pyautogui.moveTo(new_x, new_y)
            time.sleep(0.01)

    move_thread = threading.Thread(target=move_mouse)
    move_thread.daemon = True
    move_thread.start()

    while time.time() - start_time < 30:
        time.sleep(0.1)

    inverted = False
    print("Movimento do mouse voltou ao normal.")