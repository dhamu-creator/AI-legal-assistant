import { spawn } from 'child_process';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const script = path.join(__dirname, '..', 'dev-with-memory.js');
console.log('Running E2E memory test:', script);

const proc = spawn(process.execPath, [script], { stdio: 'inherit' });

proc.on('close', (code) => {
  console.log('E2E memory test exited with code', code);
  process.exit(code);
});

proc.on('error', (err) => {
  console.error('Failed to start E2E memory test:', err);
  process.exit(1);
});
