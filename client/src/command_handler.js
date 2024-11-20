export function handleCommand(client, command) {
  const [action, target, content] = command.split(":");

  if (action === "@comando") {
    client.write(`@comando:${target}:${content}`);
  } else if (action === "@easteregg") {
    client.write(`@easteregg:${target}:${content}`);
  } else if (action === "@execute") {
    client.write(`@execute:${content}`);
  } else {
    console.log("[ERRO] Comando desconhecido.");
  }
}
