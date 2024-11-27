import cv2
import base64
import time

def transmit_webcam(client_socket):
    """
    Transmite o feed da webcam para o servidor usando Base64.
    """
    cap = cv2.VideoCapture(0)  # Inicializa a captura da webcam

    # Ajustar a resolução da webcam (opcional)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("[ERRO] Não foi possível capturar o frame.")
                break

            # Codifica o frame em JPEG e converte para Base64
            _, buffer = cv2.imencode('.jpg', frame)
            frame_base64 = base64.b64encode(buffer).decode('utf-8')

            # Envia o tamanho do frame seguido pelos dados
            frame_size = str(len(frame_base64)).zfill(8).encode()  # Header com 8 bytes
            client_socket.sendall(frame_size + frame_base64.encode())

            # Adicionar um pequeno atraso para reduzir a taxa de quadros
            time.sleep(0.1)  # Atraso de 100ms (10 frames por segundo)
    except Exception as e:
        print(f"[ERRO] Durante a transmissão: {e}")
    finally:
        cap.release()
        client_socket.close()