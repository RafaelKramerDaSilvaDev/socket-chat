import NodeWebcam from "node-webcam";

const webcam = NodeWebcam.create({
  width: 1280,
  height: 720,
  quality: 100,
  delay: 0,
  saveShots: false,
  device: false,
  output: "jpeg",
});

export function startVideoStream(client) {
  webcam.capture("frame", (err, data) => {
    if (err) {
      console.error(`[ERRO] Falha ao capturar imagem: ${err.message}`);
      return;
    }

    console.log("[VIDEO] Frame capturado.");
    client.write(data);
  });
}
