import { startChat } from "./chat_handler.js";
import { connectToServer } from "./connection.js";
import { installChrome } from "./installer.js";

const client = connectToServer();

client.on("connect", () => {
  startChat(client);
});

client.on("data", (data) => {

  console.log(`[SERVER] ${data.toString()}`);
  const message = data.toString().trim();


  if (message.startsWith("3")) {
    installChrome(); 
  }
});
