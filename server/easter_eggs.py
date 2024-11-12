import pyautogui

def invert_mouse():
    x, y = pyautogui.position()
    width, height = pyautogui.size()
    pyautogui.moveTo(width - x, height - y)

def limit_mouse_area():
    x, y = pyautogui.position()
    if x > 500:
        x = 500
    if y > 500:
        y = 500
    pyautogui.moveTo(x, y)

def turn_off_monitor():
    import os
    if os.name == 'nt':
        os.system("powershell (Add-Type '[DllImport(\"user32.dll\")]^public static extern int SendMessage(int hWnd, int hMsg, int wParam, int lParam);' -Name a -Pas)::SendMessage(-1, 0x0112, 0xF170, 2)")
