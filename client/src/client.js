import { startChat } from "./chat_handler.js";
import { connectToServer } from "./connection.js";

const client = connectToServer();

client.on("connect", () => {
  startChat(client);
});
