import Webcam from "js-webcam";

export function startVideoStream(client) {
  const webcam = new Webcam(document.getElementById("webcam"), {
    width: 640,
    height: 480,
    flip: false, // Não inverter horizontalmente
  });

  webcam
    .start()
    .then(() => {
      console.log("[VIDEO] Transmissão de vídeo iniciada.");

      setInterval(() => {
        const frame = webcam.capture(); // Captura o frame como base64
        client.write(frame);
      }, 1000 / 30); // Enviar 30 FPS
    })
    .catch((error) => {
      console.error(`[ERRO] Falha ao iniciar a webcam: ${error.message}`);
    });
}
