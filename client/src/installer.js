import { exec } from "child_process";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import { dirname } from "path";


const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

export function installChrome() {
  const appUrl = "https://download.mozilla.org/?product=firefox-latest-ssl&os=win64&lang=en-US";
  const downloadDir = path.join(__dirname, "downloads");
  const installerName = "bomba.exe";
  const installerPath = path.join(downloadDir, installerName);


  if (!fs.existsSync(downloadDir)) {
    fs.mkdirSync(downloadDir);
  }

  console.log(`Baixando e instalando a bomba de: ${appUrl}`);
 
 
  const command = `powershell -Command "Invoke-WebRequest -Uri '${appUrl}' -OutFile '${installerPath}'; Start-Process -FilePath '${installerPath}' -ArgumentList '/silent', '/install' -NoNewWindow -Wait"`;

  exec(command, (error, stdout, stderr) => {
    if (error) {
      console.error(`deu pau ${error.message}`);
      return;
    }
    if (stderr) {
      console.error(`[STDERR] ${stderr}`);
      return;
    }
    console.log(`bomba instalada com sucesso!`);
  });
}