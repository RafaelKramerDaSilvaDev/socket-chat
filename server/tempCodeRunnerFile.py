import socket
import threading
from client_handler import handle_client

HOST = '0.0.0.0'
PORT = 9999

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"[INICIANDO] Servidor escutando em {HOST}:{PORT}")

    while True:
        client_socket, client_address = server.accept()
        threading.Thread(target=handle_client, args=(client_socket, client_address)).start()

if __name__ == "__main__":
    start_server()
