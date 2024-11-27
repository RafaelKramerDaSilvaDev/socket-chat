import cv2
import base64
import numpy as np

def receive_webcam(client_socket):
    """
    Recebe e exibe o feed da webcam transmitido pelo servidor.
    """
    try:
        while True:
            # Recebe o tamanho do frame
            frame_size = client_socket.recv(8)
            if not frame_size:
                break  # Conexão encerrada
            frame_size = int(frame_size.decode())

            # Recebe o frame completo em Base64
            frame_data = b''
            while len(frame_data) < frame_size:
                packet = client_socket.recv(frame_size - len(frame_data))
                if not packet:
                    break
                frame_data += packet

            # Decodifica o Base64 e reconstrói o frame
            frame_base64 = frame_data.decode()
            frame_bytes = base64.b64decode(frame_base64)
            frame = cv2.imdecode(np.frombuffer(frame_bytes, np.uint8), cv2.IMREAD_COLOR)

            # Exibe o frame
            cv2.imshow("Webcam", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except Exception as e:
        print(f"[ERRO] Durante a recepção: {e}")
    finally:
        cv2.destroyAllWindows()
        client_socket.close()