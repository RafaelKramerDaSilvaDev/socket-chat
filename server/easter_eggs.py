import ctypes
import pyautogui
import pynput
from pynput.mouse import Controller, Listener
import threading
import time

inverted = False

def invert_mouse():
    """
    Inverte o movimento do mouse por 30 segundos.
    """
    global inverted
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


def limit_mouse_area():

    duration = 30
    grid_size = 5
    step = 10

    screen_width, screen_height = pyautogui.size()
    center_x, center_y = screen_width // 2, screen_height // 2

    start_x = center_x - (grid_size // 2) * step
    start_y = center_y - (grid_size // 2) * step

    start_time = time.time()

    try:
        while time.time() - start_time < duration:
            for i in range(grid_size):
                for j in range(grid_size):

                    x = start_x + i * step
                    y = start_y + j * step
                    pyautogui.moveTo(x, y, duration=0.05)  
                    if time.time() - start_time >= duration:
                        break
                if time.time() - start_time >= duration:
                    break
    except KeyboardInterrupt:
        print("Movimento interrompido pelo usuário.")
        

def turn_off_monitor():
    try:
        ctypes.windll.user32.SendMessageW(0xFFFF, 0x0112, 0xF170, 2)
        print("Monitor desligado com sucesso.")
    except Exception as e:
        print(f"Erro ao desligar o monitor: {e}")
