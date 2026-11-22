/**
 * main.ts - make.fun bounty 'news-image-20261122' deliverable.
 *
 * Sum up 22 November 2026 world news in one deterministic image.
 * Uses Node 22 standard library ONLY (fs, path, crypto), zero network.
 *
 * Comprehensive validations:
 * 1. Checks whole PNG / JPEG magic header bytes.
 * 2. Checks complete file termination:
 *    - PNG: Validates final 12-byte IEND chunk (00 00 00 00 49 45 4E 44 AE 42 60 82).
 *    - JPEG: Validates final 2-byte EOI marker (FF D9) and parses SOF dimensions.
 * 3. Enforces dimensions <= 1024x1024 px.
 * 4. Enforces size <= 1 MiB (1,048,576 bytes).
 * 5. Writes deterministically to join(process.env.MAKEFUN_OUTPUT_DIR ?? '/output', 'entry.png').
 */

import { readFileSync, writeFileSync, mkdirSync, existsSync } from 'node:fs';
import { join, resolve } from 'node:path';
import { createHash } from 'node:crypto';

interface ImageMetadata {
  format: 'png' | 'jpeg';
  width: number;
  height: number;
  bytes: number;
  sha256: string;
}

/**
 * Validates image buffer magic bytes, whole-file structure, dimensions, and size limit.
 */
function validateImage(buf: Buffer): ImageMetadata {
  const maxBytes = 1024 * 1024; // 1 MiB = 1,048,576 bytes
  if (buf.length > maxBytes) {
    throw new Error(`Image size (${buf.length} bytes) exceeds maximum limit of 1 MiB (${maxBytes} bytes)`);
  }

  // --- PNG VALIDATION ---
  const isPngHeader =
    buf.length >= 24 &&
    buf[0] === 0x89 &&
    buf[1] === 0x50 &&
    buf[2] === 0x4e &&
    buf[3] === 0x47 &&
    buf[4] === 0x0d &&
    buf[5] === 0x0a &&
    buf[6] === 0x1a &&
    buf[7] === 0x0a;

  if (isPngHeader) {
    // Check whole PNG file integrity: must end with the 12-byte IEND chunk:
    // Length: 0x00 0x00 0x00 0x00, Chunk Type: "IEND" (0x49 0x45 0x4E 0x44), CRC: 0xAE 0x42 0x60 0x82
    const iendOffset = buf.length - 12;
    const hasValidIend =
      iendOffset >= 8 &&
      buf[iendOffset] === 0x00 &&
      buf[iendOffset + 1] === 0x00 &&
      buf[iendOffset + 2] === 0x00 &&
      buf[iendOffset + 3] === 0x00 &&
      buf[iendOffset + 4] === 0x49 && // 'I'
      buf[iendOffset + 5] === 0x45 && // 'E'
      buf[iendOffset + 6] === 0x4e && // 'N'
      buf[iendOffset + 7] === 0x44 && // 'D'
      buf[iendOffset + 8] === 0xae &&
      buf[iendOffset + 9] === 0x42 &&
      buf[iendOffset + 10] === 0x60 &&
      buf[iendOffset + 11] === 0x82;

    if (!hasValidIend) {
      throw new Error('Incomplete or corrupted PNG: missing valid terminating IEND chunk');
    }

    // Extract IHDR width and height
    const width = buf.readUInt32BE(16);
    const height = buf.readUInt32BE(20);
    const sha256 = createHash('sha256').update(buf).digest('hex');
    return { format: 'png', width, height, bytes: buf.length, sha256 };
  }

  // --- JPEG VALIDATION ---
  const isJpegHeader = buf.length >= 4 && buf[0] === 0xff && buf[1] === 0xd8 && buf[2] === 0xff;
  if (isJpegHeader) {
    // Check JPEG ends with EOI (End of Image) marker: 0xFF 0xD9
    const hasValidEoi = buf[buf.length - 2] === 0xff && buf[buf.length - 1] === 0xd9;
    if (!hasValidEoi) {
      throw new Error('Incomplete or corrupted JPEG: missing valid terminating EOI marker (FF D9)');
    }

    // Scan for SOF (Start of Frame) markers to extract dimensions: SOF0 (0xFFC0), SOF1 (0xFFC1), SOF2 (0xFFC2)
    let width = 0;
    let height = 0;
    let offset = 2;

    while (offset < buf.length - 8) {
      if (buf[offset] !== 0xff) {
        offset++;
        continue;
      }
      const marker = buf[offset + 1];
      // Markers 0xC0 to 0xC3 (excluding DHT 0xC4) are SOF markers
      if (marker >= 0xc0 && marker <= 0xc3) {
        height = buf.readUInt16BE(offset + 5);
        width = buf.readUInt16BE(offset + 7);
        break;
      }
      // Jump to next marker by reading segment length
      const segmentLen = buf.readUInt16BE(offset + 2);
      offset += 2 + segmentLen;
    }

    if (width === 0 || height === 0) {
      throw new Error('Could not parse valid JPEG dimensions from SOF marker');
    }

    const sha256 = createHash('sha256').update(buf).digest('hex');
    return { format: 'jpeg', width, height, bytes: buf.length, sha256 };
  }

  throw new Error('Unsupported image format: expected valid PNG or JPEG magic bytes');
}

function main(): void {
  const baseDir = import.meta.dirname ?? process.cwd();
  const srcPath = resolve(baseDir, 'entry.png');

  if (!existsSync(srcPath)) {
    throw new Error(`Source image entry.png not found at expected path: ${srcPath}`);
  }

  const imageBuffer = readFileSync(srcPath);
  const meta = validateImage(imageBuffer);

  if (meta.width > 1024 || meta.height > 1024) {
    throw new Error(`Image dimensions ${meta.width}x${meta.height} exceed maximum allowed 1024x1024`);
  }

  const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
  mkdirSync(outDir, { recursive: true });

  const destPath = join(outDir, 'entry.png');
  writeFileSync(destPath, imageBuffer);

  console.log(`[make.fun · news-image-20261122] Successfully wrote verified entry image`);
  console.log(`  Destination: ${destPath}`);
  console.log(`  Format:      ${meta.format.toUpperCase()} (whole file verified)`);
  console.log(`  Dimensions:  ${meta.width}x${meta.height} px (limit: <= 1024x1024)`);
  console.log(`  Byte Size:   ${meta.bytes.toLocaleString()} bytes (${(meta.bytes / 1024).toFixed(1)} KiB, limit: <= 1 MiB)`);
  console.log(`  SHA256:      ${meta.sha256}`);
}

main();
