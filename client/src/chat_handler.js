import fs from "fs";
import readline from "readline";

export function startChat(client) {
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  });

  rl.on("line", (input) => {
    if (input.toLowerCase() === "exit") {
      client.write("exit");
      rl.close();
    } else if (input === "3") {
      rl.question("Digite o nome do usuário destino: ", (username) => {
        rl.question("Digite o caminho do arquivo: ", (filePath) => {
          try {
            const fileStats = fs.statSync(filePath);
            const fileSize = fileStats.size;
            const fileName = filePath.split("\\").pop().split("/").pop();
            client.write(`@sendfile:${username}:${fileSize}:${fileName}`);

            const fileStream = fs.createReadStream(filePath);
            fileStream.on("data", (chunk) => {
              client.write(chunk);
            });

            fileStream.on("end", () => {
              console.log("[CLIENT] Arquivo enviado com sucesso.");
            });
          } catch (error) {
            console.error("[CLIENT] Erro ao acessar o arquivo:", error.message);
          }
        });
      });
    } else {
      client.write(input);
    }
  });
}
