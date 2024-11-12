const readline = require("readline");

function startChat(client) {
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  });

  rl.on("line", (input) => {
    if (input.toLowerCase() === "exit") {
      client.write("exit");
      rl.close();
    } else {
      client.write(input);
    }
  });
}

module.exports = { startChat };
