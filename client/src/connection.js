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
    console.log(data.toString());
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
