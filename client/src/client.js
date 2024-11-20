import { startChat } from "./chat_handler.js";
// import { handleCommand } from "./command_handler.js";
import { connectToServer } from "./connection.js";
// import { startVideoStream } from "./video_stream.js";

const client = connectToServer();

client.on("connect", () => {
  console.log("[CLIENT] Digite seu nome de usuário e senha.");
  startChat(client);

  // Teste de envio de comando e vídeo
  // handleCommand(client, "@easteregg:invert_mouse");
  // startVideoStream(client);
});
