import os

def receive_file(client_socket, save_directory="received_files"):
    """
    Recebe um arquivo de um cliente e o salva em disco.

    Args:
        client_socket: O socket do cliente que está enviando o arquivo.
        save_directory: O diretório onde o arquivo será salvo.

    Returns:
        O caminho completo do arquivo salvo.
    """
    try:
        # Receber informações sobre o arquivo
        file_info = client_socket.recv(1024).decode()  # Espera: "file_name:file_size"
        file_name, file_size = file_info.split(":")
        file_size = int(file_size)

        # Certificar-se de que o diretório de destino existe
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)

        # Caminho completo para salvar o arquivo
        file_path = os.path.join(save_directory, file_name)

        # Receber os dados do arquivo
        with open(file_path, "wb") as file:
            bytes_received = 0
            while bytes_received < file_size:
                chunk = client_socket.recv(min(4096, file_size - bytes_received))
                if not chunk:
                    raise Exception("Conexão encerrada antes da recepção completa.")
                file.write(chunk)
                bytes_received += len(chunk)

        print(f"[SUCESSO] Arquivo recebido e salvo em: {file_path}")
        return file_path

    except Exception as e:
        print(f"[ERRO] Erro ao receber arquivo: {e}")
        raise
