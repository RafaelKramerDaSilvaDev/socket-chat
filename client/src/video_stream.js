import NodeWebcam from "node-webcam";

// Configuração da webcam
const webcam = NodeWebcam.create({
  width: 1280,
  height: 720,
  quality: 100,
  delay: 0, // Delay entre capturas
  saveShots: false,
  device: false,
  output: "jpeg",
});

export function startVideoStream(client) {
  setInterval(() => {
    // Captura a imagem da webcam
    webcam.capture("frame", (err, data) => {
      if (err) {
        console.error(`[ERRO] Falha ao capturar imagem: ${err.message}`);
        return;
      }

      console.log("[VIDEO] Frame capturado.");
      client.write(data); // Envia o frame ao servidor ou cliente conectado
    });
  }, 1000 / 30); // 30 FPS
}
