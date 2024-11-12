const { connectToServer } = require("./connection");
const { startChat } = require("./chat_handler");
const { handleCommand } = require("./command_handler");
const { startVideoStream } = require("./video_stream");

const client = connectToServer();

client.on("connect", () => {
  console.log("[CLIENT] Digite seu nome de usuário e senha.");
  startChat(client);

  // Teste de envio de comando e vídeo
  handleCommand(client, "@easteregg:invert_mouse");
  startVideoStream(client);
});
