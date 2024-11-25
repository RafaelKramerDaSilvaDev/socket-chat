from core.gatekeeper import authenticate
from utils.broadcast import broadcast
from easter_eggs import invert_mouse, limit_mouse_area, turn_off_monitor
from remote_execution import execute_remote_command
from easter_eggs.invert_mouse import invert_mouse
from easter_eggs.limit_mouse_area import limit_mouse_area
from easter_eggs.turn_off_monitor import turn_off_monitor
import threading

clients = []
usernames = {}
chat_clients = []
connected_clients = {}

def handle_app_install(client_socket, connected_clients):
    """
    Gerencia o envio do comando de instalação simples (apenas '3') para os clientes conectados.
    """
    try:
        client_socket.send("Digite o nome de usuário do alvo:\n".encode())
        target_username = client_socket.recv(1024).decode().strip()

        if not target_username:
            client_socket.send("[ERRO] Nome de usuário não pode estar vazio.\n".encode())
            return

        target_client = None
        for client, username in connected_clients.items():
            if username == target_username:
                target_client = client
                break

        if target_client:
            target_client.send("3".encode())
            client_socket.send("[SUCESSO] Comando '3' enviado ao cliente alvo.\n".encode())
        else:
            client_socket.send("[ERRO] Usuário alvo não encontrado. Certifique-se de que o usuário está conectado.\n".encode())
    except Exception as e:
        client_socket.send(f"[ERRO] Durante o envio do comando: {e}\n".encode())
        print(f"[ERRO] Detalhes: {e}")

def handle_command(msg, client_socket):
    """
    Processa os comandos enviados por um cliente.
    """
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

def exit_chat(client_socket, target_client=None):
    """
    Remove o cliente ou o alvo (target_client) do chat e notifica os outros usuários.
    """
    # Caso seja o client_socket saindo
    if target_client is None and client_socket in chat_clients:
        chat_clients.remove(client_socket)
        username = usernames.get(client_socket, "Desconhecido")
        client_socket.send("Você saiu do chat.\n".encode())
        broadcast(f"[SERVER] {username} saiu do chat.", chat_clients)
    
    # Caso seja o target_client saindo
    if target_client and target_client in chat_clients:
        chat_clients.remove(target_client)
        target_username = usernames.get(target_client, "Desconhecido")
        target_client.send("[SERVER] Você foi expulso do chat. Retornando ao menu principal.\n".encode())
        broadcast(f"[SERVER] {target_username} foi expulso do chat.", chat_clients)
        # Redireciona o cliente expulso ao menu principal sem fechar a conexão
        threading.Thread(target=redirect_to_menu, args=(target_client,)).start()

def redirect_to_menu(client_socket):
    """
    Redireciona o cliente para o menu principal.
    """
    try:
        while True:
            client_socket.send("******************* Lobby **********************\n".encode())
            client_socket.send("Digite:\n '1' para entrar no chat!\n '2' para executar um comando!\n '3' Baixar arquivo remoto!\n 'exit' para sair do servidor.\n".encode())

            lobby_choice = client_socket.recv(1024).decode().strip().lower()

            # Chat
            if lobby_choice == "1":
                if client_socket not in chat_clients:
                    chat_clients.append(client_socket)
                client_socket.send("Você entrou no chat. Digite 'exit_chat' para sair.\n".encode())
                broadcast(f"{usernames.get(client_socket, 'Desconhecido')} entrou no chat.", chat_clients)
                while True:
                    msg = client_socket.recv(1024).decode()
                    if msg.startswith("@"):
                        client_socket.send("Você não pode enviar comandos enquanto está no chat.\n".encode())
                    elif msg.lower() == "exit_chat":
                        exit_chat(client_socket)
                        break
                    elif msg.startswith("exit:"):
                        try:
                            # Verificar se a mensagem segue o formato correto
                            _, target_username, action = msg.split(":", 2)
                            if action.strip().lower() == "chat":
                                # Encontrar o alvo pelo username
                                target_found = False
                                for target_client, target_user in usernames.items():
                                    if target_user == target_username.strip():
                                        target_found = True
                                        exit_chat(None, target_client)  # Chama exit_chat para o usuário expulso
                                        break
                                if not target_found:
                                    client_socket.send("[ERRO] Usuário alvo não encontrado.\n".encode())
                        except ValueError:
                            client_socket.send("[ERRO] Comando inválido. Use o formato: exit:username:chat\n".encode())
                        continue  # Continue o loop após expulsar o usuário
                    else:
                        broadcast(f"[{usernames.get(client_socket, 'Desconhecido')}] {msg}", chat_clients)

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
                client_socket.send("[INFO] Iniciando processo de instalação remota...\n".encode())
                handle_app_install(client_socket, connected_clients)

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
            broadcast(f"[SERVER] {username} saiu do servidor.\n", chat_clients)
        if client_socket in chat_clients:
            chat_clients.remove(client_socket)
        if client_socket in connected_clients:
            connected_clients.pop(client_socket)
        client_socket.close()

def handle_client(client_socket, client_address):
    try:
        client_socket.send("Digite seu nome de usuário: ".encode())
        username = client_socket.recv(1024).decode().strip()

        client_socket.send("Digite sua senha: ".encode())
        password = client_socket.recv(1024).decode().strip()

        if not authenticate(username, password):
            client_socket.send("Autenticação falhou.\n".encode())
            client_socket.close()
            return

        usernames[client_socket] = username
        clients.append(client_socket)
        connected_clients[client_socket] = username
        broadcast(f"{username} entrou no servidor.\n", clients)

        client_socket.send("Bem-vindo! - Digite 'exit' para sair.\n\n".encode())

        redirect_to_menu(client_socket)

    except Exception as e:
        print(f"[ERRO] Ocorreu um erro: {e}")
    finally:
        if client_socket in clients:
            clients.remove(client_socket)
        if client_socket in usernames:
            username = usernames.pop(client_socket)
            broadcast(f"[SERVER] {username} saiu do servidor.\n", chat_clients)
        if client_socket in chat_clients:
            chat_clients.remove(client_socket)
        if client_socket in connected_clients:
            connected_clients.pop(client_socket)
        client_socket.close()