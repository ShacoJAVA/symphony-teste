import { init } from "@heyputer/puter.js/src/init.cjs";
import fs from "node:fs";
import path from "node:path";

const prompt = process.argv[2];
const outputBase = process.argv[3];

if (!prompt || !outputBase) {
  console.error(
    'Uso: node executors/puter_image.mjs "PROMPT" "CAMINHO/ARQUIVO"'
  );
  process.exit(1);
}

if (!process.env.PUTER_AUTH_TOKEN) {
  console.error("Erro: PUTER_AUTH_TOKEN não configurado.");
  process.exit(1);
}

const puter = init(process.env.PUTER_AUTH_TOKEN);

const model = "google/gemini-3.1-flash-image";

console.log("=== GALAEM IMAGE EXECUTOR ===");
console.log("Provider: Puter");
console.log("Model:", model);
console.log("Gerando imagem...");

const image = await puter.ai.txt2img(prompt, {
  model
});

const match = image.src?.match(/^data:(image\/[^;]+);base64,(.+)$/);

if (!match) {
  throw new Error("O provedor retornou um formato de imagem inesperado.");
}

const mime = match[1];
const base64 = match[2];

const extension =
  mime === "image/png" ? ".png" :
  mime === "image/jpeg" ? ".jpg" :
  ".img";

const output = outputBase + extension;

fs.mkdirSync(path.dirname(output), {
  recursive: true
});

fs.writeFileSync(
  output,
  Buffer.from(base64, "base64")
);

console.log("STATUS: SUCESSO");
console.log("Formato:", mime);
console.log("Arquivo:", output);
