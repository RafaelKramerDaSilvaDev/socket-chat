from gatekeeper import authenticate
from utils import broadcast
from easter_eggs import invert_mouse, limit_mouse_area, turn_off_monitor
from remote_execution import execute_remote_command

clients = []
usernames = {}
chat_clients = []

def handle_command(msg, client_socket):
    try:
        command, target_username, content = msg.split(":", 2)

        if command == "@comando":
            for client, username in usernames.items():
                if username == target_username.strip():
                    try:
                        client.send(f"[COMANDO] {content}".encode())
                    except Exception as e:
                        print(f"[ERRO] Não foi possível enviar o comando: {e}")

        elif command == "@easteregg":
            for client, username in usernames.items():
                if username == target_username.strip():
                    if content.strip() == "invert_mouse":
                        invert_mouse()
                    elif content.strip() == "limit_mouse":
                        limit_mouse_area()
                    elif content.strip() == "turn_off_monitor":
                        turn_off_monitor()
                    break
        elif command == "@execute":
            for client, username in usernames.items():
                if username == target_username.strip():
                    execute_remote_command(content.strip())
                    break
    except ValueError:
        client_socket.send("Formato de comando inválido. Use @comando:target_username:content\n".encode())

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
        broadcast(f"{username} entrou/n", clients)

        client_socket.send("Bem-vindo! - Digite 'exit' para sair\n\n\n".encode())

        while True:
            client_socket.send("******************* Lobby **********************\n\n".encode())
            client_socket.send("Digite:\n '1' para entrar no chat!\n '2' para executar um comando!\n 'exit' para sair do servidor.\n".encode())

            lobby_choice = client_socket.recv(1024).decode().strip().lower()

            # Chat
            if lobby_choice == "1":
                chat_clients.append(client_socket)
                client_socket.send("Você entrou no chat. Digite 'exit_chat' para sair.\n".encode())
                broadcast(f"{username} entrou no chat.", clients)
                while True:
                    msg = client_socket.recv(1024).decode()
                    if msg.startswith("@"):
                        client_socket.send("Você não pode enviar comandos enquanto está no chat.\n".encode())
                    elif msg.lower() == "exit_chat":
                        client_socket.send("Você saiu do chat.\n".encode())
                        chat_clients.remove(client_socket)
                        break
                    else:
                        broadcast(f"[{username}] {msg}", chat_clients)

            # Comandos
            elif lobby_choice == "2":

                client_socket.send("Você entrou na seção de comandos. Digite 'exit_comandos' para sair.\n".encode())
                
                client_socket.send("Lista de comandos.\n\n".encode())
                client_socket.send("@easteregg:nomeUsuario:turn_off_monitor - Desliga o monitor do usuário selecionado.\n".encode())
                client_socket.send("@easteregg:nomeUsuario:limit_mouse - Limita o movimento do mouse do usuário selecionado.\n".encode())
                client_socket.send("@easteregg:nomeUsuario:invert_mouse - Inverte o mouse do usuário selecionado.\n".encode())
                client_socket.send("Digite seu comando!\n".encode())

                while True:
                    command_msg = client_socket.recv(1024).decode()
                    if command_msg.lower() == "exit_comandos":
                        client_socket.send("Você saiu da seção de comandos.\n".encode())
                        break
                    elif command_msg.startswith("@"):
                        handle_command(command_msg, client_socket)
                    else:
                        client_socket.send("Formato de comando inválido. Use @comando:target_username:content\n".encode())
            elif lobby_choice == "exit":
                client_socket.send("Você saiu do servidor.\n".encode())
                break
            else:
                client_socket.send("Opção inválida. Tente novamente.\n".encode())

    except Exception as e:

        print(f"[ERRO] Ocorreu um erro: {e}")

    finally:
        if client_socket in clients:
            clients.remove(client_socket)
        if client_socket in usernames:
            username = usernames.pop(client_socket)
            broadcast(f"[SERVER] {username} saiu do chat.", chat_clients)
        if client_socket in chat_clients:
            chat_clients.remove(client_socket)
        client_socket.close()

