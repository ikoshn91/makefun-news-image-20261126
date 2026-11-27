// make.fun entry: news-image-20261126
// Copies the pre-rendered entry.png (drawn by gen_image.py) to the output
// directory. Node 22, standard library only, no network.
// Validates the file is a whole PNG before copying, and reports its size.
import * as fs from "node:fs";
import * as path from "node:path";

// `node main.ts` loads this file as ESM (Node type-stripping), so the
// script directory comes from import.meta.dirname, not __dirname.
const scriptDir = import.meta.dirname;
const outDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";
const src = path.join(scriptDir, "entry.png");
const dst = path.join(outDir, "entry.png");

const buf = fs.readFileSync(src);
const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (buf.length < 8 || !buf.subarray(0, 8).equals(PNG_MAGIC)) {
  throw new Error("entry.png is not a PNG file");
}
if (buf.length > 1048576) {
  throw new Error(`entry.png is ${buf.length} bytes, over the 1 MiB limit`);
}

fs.mkdirSync(outDir, { recursive: true });
fs.writeFileSync(dst, buf);
console.log(`wrote ${dst} (${buf.length} bytes)`);
