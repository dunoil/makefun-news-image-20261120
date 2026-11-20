// news-image-20261120 entrypoint (Node 22, standard library only).
// The image beside this file is the entry: a 1024x1024 newspaper page
// summing up the world's news of Friday 20 November 2026. This program
// validates the image, then copies it to the output directory.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';

const src = fileURLToPath(new URL('./entry.png', import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const bytes = readFileSync(src);

const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (!bytes.subarray(0, 8).equals(PNG_MAGIC)) {
  throw new Error('entry.png is not a PNG file');
}
if (bytes.length > 1048576) {
  throw new Error(`entry.png is ${bytes.length} bytes, over the 1 MiB limit`);
}
const width = bytes.readUInt32BE(16);
const height = bytes.readUInt32BE(20);
if (width !== 1024 || height !== 1024) {
  throw new Error(`entry.png is ${width}x${height}, expected 1024x1024`);
}
const chunkType = bytes.subarray(12, 16).toString('ascii');
if (chunkType !== 'IHDR') {
  throw new Error(`entry.png has no IHDR chunk, found ${chunkType}`);
}

mkdirSync(outDir, { recursive: true });
const dest = join(outDir, 'entry.png');
writeFileSync(dest, bytes);
const written = readFileSync(dest);
if (!written.equals(bytes)) {
  throw new Error('entry.png was not written back byte for byte');
}
console.log(`copied entry.png (${bytes.length} bytes, 1024x1024) to ${outDir}`);
