from gatekeeper import authenticate
from utils import broadcast
from easter_eggs import invert_mouse, limit_mouse_area, turn_off_monitor
from remote_execution import execute_remote_command

clients = []
usernames = {}

def handle_command(msg, client_socket):
    command, target_username, content = msg.split(":", 2)

    if command == "@comando":
        for client, username in usernames.items():
            if username == target_username.strip():
                try:
                    client.send(f"[COMANDO] {content}".encode())
                except Exception as e:
                    print(f"[ERRO] Não foi possível enviar o comando: {e}")
    elif command == "@easteregg":
        if content.strip() == "invert_mouse":
            invert_mouse()
        elif content.strip() == "limit_mouse":
            limit_mouse_area()
        elif content.strip() == "turn_off_monitor":
            turn_off_monitor()
    elif command == "@execute":
        execute_remote_command(content.strip())

def handle_client(client_socket, client_address):
    try:
        client_socket.send("Digite seu nome de usuário: ".encode())
        username = client_socket.recv(1024).decode()

        client_socket.send("Digite sua senha: ".encode())
        password = client_socket.recv(1024).decode()

        if not authenticate(username, password):
            client_socket.send("Autenticação falhou.".encode())
            client_socket.close()
            return

        usernames[client_socket] = username
        clients.append(client_socket)
        broadcast(f"[SERVER] {username} entrou no chat.", clients)

        while True:
            msg = client_socket.recv(1024).decode()
            if msg.startswith("@"):
                handle_command(msg, client_socket)
            elif msg.lower() == "exit":
                break
            else:
                broadcast(f"[{username}] {msg}", clients)
    finally:
        clients.remove(client_socket)
        broadcast(f"[SERVER] {username} saiu do chat.", clients)
        client_socket.close()
