const net = require("net");
require("dotenv").config();

const HOST = process.env.SERVER_HOST || "127.0.0.1";
const PORT = process.env.SERVER_PORT || 9999;

let client;

function connectToServer() {
  client = new net.Socket();

  client.connect(PORT, HOST, () => {
    console.log(`[CLIENT] Conectado ao servidor em ${HOST}:${PORT}`);
  });

  client.on("data", (data) => {
    console.log(`[SERVER] ${data.toString()}`);
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

module.exports = { connectToServer };
