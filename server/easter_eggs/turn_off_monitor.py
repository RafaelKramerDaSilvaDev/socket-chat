import ctypes

def turn_off_monitor():
    try:
        ctypes.windll.user32.SendMessageW(0xFFFF, 0x0112, 0xF170, 2)
        print("Monitor desligado com sucesso.")
    except Exception as e:
        print(f"Erro ao desligar o monitor: {e}")
