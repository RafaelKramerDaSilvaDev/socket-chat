from core.gatekeeper import authenticate

from utils.broadcast import broadcast
from utils.execute_remote_command import execute_remote_command
from utils.receive_file import receive_file

from easter_eggs.invert_mouse import invert_mouse
from easter_eggs.limit_mouse_area import limit_mouse_area
from easter_eggs.turn_off_monitor import turn_off_monitor

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

        elif command == "@sendfile":
            try:
                _, target_username, file_size, file_name = msg.split(":", 3)
                file_size = int(file_size)

                if "\\" in file_name or "/" in file_name:
                    file_name = file_name.split("\\")[-1].split("/")[-1]

                if target_username.strip() not in usernames.values():
                    client_socket.send("Usuário não encontrado.\n".encode())
                    return

                # Encontrar o cliente destinatário
                dest_client = None
                for client, username in usernames.items():
                    if username == target_username.strip():
                        dest_client = client
                        break

                if dest_client:
                    dest_client.send(
                        f"RECEIVEFILE:{file_size}:{file_name}:{usernames[client_socket]}".encode()
                    )

                    # Transferir os dados do arquivo para o destinatário
                    bytes_sent = 0
                    while bytes_sent < file_size:
                        chunk = client_socket.recv(min(file_size - bytes_sent, 4096))
                        dest_client.send(chunk)  # Transfere os bytes diretamente
                        bytes_sent += len(chunk)

                    client_socket.send(f"Arquivo enviado para {target_username}.\n".encode())
                else:
                    client_socket.send("Não foi possível encontrar o destinatário.\n".encode())
            except Exception as e:
                print(f"[ERRO] Ocorreu um erro ao enviar o arquivo: {e}")
                client_socket.send(f"Erro ao enviar arquivo: {e}\n".encode())


        elif command.startswith("RECEIVEFILE"):
            try:
                _, file_size, file_name, sender_username = command.split(":", 3)
                file_size = int(file_size)

                client_socket.send(f"Recebendo arquivo '{file_name}' de {sender_username}...\n".encode())
                
                # Salvar o arquivo
                with open(f"recebido_{file_name}", "wb") as file:
                    bytes_received = 0
                    while bytes_received < file_size:
                        chunk = client_socket.recv(min(file_size - bytes_received, 4096))
                        file.write(chunk)
                        bytes_received += len(chunk)

                client_socket.send(f"Arquivo '{file_name}' recebido com sucesso.\n".encode())
            except Exception as e:
                print(f"[ERRO] Ocorreu um erro ao receber o arquivo: {e}")
                client_socket.send(f"Erro ao receber arquivo: {e}\n".encode())


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
        broadcast(f"{username} entrou\n", clients, sender_socket=client_socket)


        while True:
            client_socket.send("******************** Lobby ********************\n".encode())
            client_socket.send("Opções:\n".encode())
            client_socket.send("[1] para entrar no chat!\n".encode())
            client_socket.send("[2] para executar um comando!\n".encode())
            client_socket.send("[3] para enviar um arquivo!\n".encode())
            client_socket.send("[exit] para sair do servidor.\n".encode())

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

            elif lobby_choice == "3":
                client_socket.send("Digite o nome do usuário destino: ".encode())
                target_username = client_socket.recv(1024).decode().strip()

                if target_username not in usernames.values():
                    client_socket.send("Usuário não encontrado.\n".encode())
                    continue

                client_socket.send("Digite o tamanho do arquivo (em bytes): ".encode())
                try:
                    file_size = int(client_socket.recv(1024).decode().strip())
                except ValueError:
                    client_socket.send("Tamanho do arquivo inválido.\n".encode())
                    continue

                client_socket.send("Digite o nome do arquivo (incluindo a extensão): ".encode())
                file_name = client_socket.recv(1024).decode().strip()

                client_socket.send(f"Preparando para enviar o arquivo '{file_name}'...\n".encode())
                handle_command(
                    f"@sendfile:{target_username}:{file_size}:{file_name}", client_socket
                )

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
