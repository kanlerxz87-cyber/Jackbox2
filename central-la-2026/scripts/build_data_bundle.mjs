#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const dataDir = path.join(root, 'data');
const outFile = path.join(root, 'assets', 'js', 'data-bundle.js');

const files = {
  tenant: 'tenant.json',
  market: 'market-w01.json',
  hazards: 'hazards-w04.json',
  taxLease: 'tax-lease.json',
  gates: 'gates-w03.json',
  flagged: 'flagged.json',
  qaSuggestions: 'questions-suggestions.json'
};

const bundle = {};
for (const [key, fname] of Object.entries(files)) {
  const fullPath = path.join(dataDir, fname);
  const raw = fs.readFileSync(fullPath, 'utf8');
  bundle[key] = JSON.parse(raw);
}

fs.mkdirSync(path.dirname(outFile), { recursive: true });
const jsContent = `/* Auto-generated from data/*.json by scripts/build_data_bundle.mjs — do not edit manually. */\nwindow.JACKBOX_DATA = ${JSON.stringify(bundle, null, 2)};\n`;
fs.writeFileSync(outFile, jsContent, 'utf8');
console.log(`Built ${outFile} (${Object.keys(bundle).length} datasets)`);
