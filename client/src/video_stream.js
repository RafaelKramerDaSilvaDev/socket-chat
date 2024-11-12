const Webcam = require("webcam-easy");

function startVideoStream(client) {
  const webcam = new Webcam(document.getElementById("webcam"), "user");
  webcam
    .start()
    .then(() => {
      console.log("[VIDEO] Transmissão de vídeo iniciada.");

      setInterval(() => {
        const frame = webcam.snap();
        client.write(frame);
      }, 1000 / 30); // Enviar 30 frames por segundo
    })
    .catch((error) => {
      console.error(`[ERRO] Falha ao iniciar a webcam: ${error.message}`);
    });
}

module.exports = { startVideoStream };
