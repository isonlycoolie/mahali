// Renders ../svg into ../png with sharp. Point SHARP_FROM at any folder whose node_modules holds sharp.
// Run from the repo root: SHARP_FROM=<folder> node brand/build/rasterize.mjs

import { mkdirSync } from "node:fs";
import { createRequire } from "node:module";
import { join } from "node:path";

const sharp = createRequire(join(process.env.SHARP_FROM ?? process.cwd(), "noop.js"))("sharp");
const svg = new URL("../svg/", import.meta.url);
const png = new URL("../png/", import.meta.url);
mkdirSync(png, { recursive: true });

const jobs = { banner: [1600, 3200], "app-icon": [180, 512, 1024], "app-icon-light": [512], "lockup-on-dark": [600], lockup: [600] };

for (const [name, widths] of Object.entries(jobs)) {
  for (const width of widths) {
    const file = new URL(`${name}.svg`, svg).pathname.slice(1);
    const { width: natural = width } = await sharp(file).metadata();
    await sharp(file, { density: (72 * width) / natural })
      .resize({ width })
      .png({ compressionLevel: 9 })
      .toFile(new URL(`${name}-${width}.png`, png).pathname.slice(1));
  }
}
console.log("rendered", Object.keys(jobs).length, "files");
