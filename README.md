# 🖥️ Projeto Socket Chat

## 📋 **Descrição**

Este projeto é um sistema de chat com controle remoto utilizando **Sockets TCP**. O servidor foi desenvolvido em **Python**, e o cliente em **Node.js**. O sistema permite:

- Comunicação de chat entre vários clientes.
- Autenticação de usuários (Gatekeeper).
- Execução de comandos remotos e Easter Eggs (como controle de mouse e desligamento de monitor).
- Transmissão de vídeo da webcam.
- Execução remota de aplicativos.

## 🗂️ **Estrutura do Projeto**

```plaintext
socket-chat/
├── server/                 # Código do servidor em Python
│   ├── client_handler.py
│   ├── easter_eggs.py
│   ├── gatekeeper.py
│   ├── remote_execution.py
│   ├── server.py
│   ├── utils.py
│   └── video_stream.py
├── client/                 # Código do cliente em Node.js
│   ├── src/
│   │   ├── client.js
│   │   ├── connection.js
│   │   ├── chat_handler.js
│   │   ├── command_handler.js
│   │   └── video_stream.js
├── data/                   # Arquivo JSON para autenticação
│   └── users.json
├── README.md               # Instruções do projeto
└── requirements.txt        # Dependências do servidor
```

## 🛠️ **Pré-requisitos**

- Python 3.x
- Node.js
- Bibliotecas adicionais:
  - Python: `opencv-python`, `pyautogui`
  - Node.js: `readline`, `webcam-easy`

## 💻 **Instalação e Execução**

### **1. Configuração do Servidor (Python)**

1. Instale as dependências:
   ```bash
   pip install -r server/requirements.txt
   ```
2. Execute o servidor:
   ```bash
   python server/server.py
   ```

### **2. Configuração do Cliente (Node.js)**

1. Instale as dependências:
   ```bash
   cd client/
   npm install
   ```
2. Execute o cliente:
   ```bash
   node src/client.js
   ```

## 🔒 **Autenticação**

Os usuários e senhas estão armazenados no arquivo `data/users.json`. Exemplo:

```json
{
  "users": {
    "admin": "admin123",
    "user1": "password1"
  }
}
```

## 📝 **Comandos Disponíveis**

- **Chat**: Digite qualquer mensagem para enviar ao chat.
- **Comando Remoto**: `@comando:<destino>:<comando>`
- **Easter Egg**: `@easteregg:<destino>:<ação>` (ex: `invert_mouse`, `limit_mouse`, `turn_off_monitor`)
- **Execução de Aplicação**: `@execute:<comando>` (ex: `calc.exe`)

## 🎥 **Transmissão de Vídeo**

A transmissão de vídeo da webcam é iniciada automaticamente pelo cliente. O vídeo é enviado para o servidor e retransmitido para todos os clientes conectados.

## 🛡️ **Segurança**

Este projeto permite execução de comandos remotos, portanto, use apenas em um ambiente controlado para evitar riscos de segurança.

## 🤝 **Contribuições**

Sinta-se à vontade para fazer contribuições ao projeto via Pull Request.

## 📄 **Licença**

Este projeto é de uso educacional e foi criado para fins de aprendizado.

---

**Autor:** Sua Equipe de Desenvolvimento
