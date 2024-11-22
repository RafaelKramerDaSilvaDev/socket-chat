import { Socket } from "net";

const HOST = "0.0.0.0";
const PORT = 9999;

let client;

export function connectToServer() {
  client = new Socket();

  client.connect(PORT, HOST, () => {
    console.log(`[CLIENT] Conectado ao servidor em ${HOST}:${PORT}`);
  });

  client.on("data", (data) => {
    const message = data.toString();
    if (message.startsWith("RECEIVEFILE")) {
      const [, fileSize, fileName, senderUsername] = message.split(":");

      const fileStream = fs.createWriteStream(`recebido_${fileName}`);

      console.log(`Recebendo arquivo '${fileName}' de ${senderUsername}...`);
      let bytesReceived = 0;

      client.on("data", (chunk) => {
        bytesReceived += chunk.length;
        fileStream.write(chunk); // Grava os bytes recebidos no arquivo

        if (bytesReceived >= parseInt(fileSize)) {
          console.log(`Arquivo '${fileName}' recebido com sucesso.`);
          fileStream.end();
        }
      });
    } else {
      console.log(message);
    }
  });

  client.on("close", () => {
    console.log("[CLIENT] Conexão encerrada pelo servidor.");
    process.exit();
  });

  client.on("error", (error) => {
    console.error(`[ERRO] ${error.message}`);
  });

  return client;
}
