import subprocess
import os

def execute_remote_command(command):
    """
    Executa um comando remoto no cliente.
    :param command: Comando a ser executado.
    """
    try:
      
        print(f"Executando comando remoto: {command}")

        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(f"Erro ao executar comando: {result.stderr}")
        return result.stdout
    except Exception as e:
        print(f"Erro ao executar comando remoto: {e}")
        return str(e)

def install_and_run_app(app_url, client_socket):
    """
    Baixa, instala e executa um aplicativo remoto no cliente.
    :param app_url: URL para o download do aplicativo.
    :param client_socket: Conexão com o cliente.
    """
    try:

        app_name = os.path.basename(app_url)
        download_dir = os.path.join(os.getcwd(), "downloads")
        local_path = os.path.join(download_dir, app_name)


        if not os.path.exists(download_dir):
            os.makedirs(download_dir)


        client_socket.send("[INFO] Verificando se o PowerShell está disponível...\n".encode())
        result = subprocess.run(["powershell", "-Command", "Get-Command powershell"], capture_output=True, text=True)
        if result.returncode != 0:
            client_socket.send("[ERROR] PowerShell não está disponível no sistema.\n".encode())
            return


        client_socket.send(f"[INFO] Baixando aplicativo de {app_url}...\n".encode())
        result = subprocess.run(["powershell", "-Command", f"Invoke-WebRequest -Uri '{app_url}' -OutFile '{local_path}'"], capture_output=True, text=True)
        if result.returncode != 0:
            client_socket.send(f"[ERROR] Falha ao baixar o aplicativo: {result.stderr}\n".encode())
            return
        client_socket.send("[INFO] Aplicativo baixado com sucesso.\n".encode())


        client_socket.send("[INFO] Iniciando o aplicativo...\n".encode())
        subprocess.Popen([local_path, "/silent", "/install"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        client_socket.send("[SUCCESS] Aplicativo executado com sucesso. Por favor, siga as instruções para concluir a instalação.\n".encode())

    except subprocess.CalledProcessError as e:
        client_socket.send(f"[ERROR] Falha ao baixar ou instalar o aplicativo: {e}\n".encode())
    except Exception as e:
        client_socket.send(f"[ERROR] Ocorreu um erro inesperado: {e}\n".encode())