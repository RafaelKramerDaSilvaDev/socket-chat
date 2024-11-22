def broadcast(message, clients, sender_socket=None):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode())
            except Exception as e:
                print(f"[ERRO] Falha ao enviar mensagem: {e}")
                clients.remove(client)
