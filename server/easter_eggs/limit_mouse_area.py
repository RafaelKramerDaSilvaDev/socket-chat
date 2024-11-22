import pyautogui
import time

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