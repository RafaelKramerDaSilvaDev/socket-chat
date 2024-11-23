import os

BUFFER_SIZE = 4096

def save_file(client_socket):
    try:
        # Receber o nome do arquivo e o tamanho do arquivo
        received = client_socket.recv(BUFFER_SIZE).decode()
        filename, filesize = received.split("<SEPARATOR>")
        filename = os.path.basename(filename)
        filesize = int(filesize)

        # Caminho para salvar o arquivo recebido
        received_files_dir = "./data/received_files"
        if not os.path.exists(received_files_dir):
            os.makedirs(received_files_dir)
        filepath = os.path.join(received_files_dir, filename)

        # Receber o arquivo
        with open(filepath, "wb") as f:
            while True:
                bytes_read = client_socket.recv(BUFFER_SIZE)
                if not bytes_read:
                    break
                f.write(bytes_read)

        print(f"[INFO] Arquivo {filename} recebido e salvo em {filepath}")
    except Exception as e:
        print(f"[ERRO] Ocorreu um erro ao receber o arquivo: {e}")
    finally:
        client_socket.close()