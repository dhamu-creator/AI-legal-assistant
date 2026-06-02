import fs from 'fs/promises';
import pdfParse from 'pdf-parse';

async function main() {
    const pdfPath = process.argv[2];
    const lang = process.argv[3] || 'en';
    if (!pdfPath) {
        console.error('Usage: node verify-pdf.js <pdf-path> [lang]');
        process.exit(2);
    }

    const buf = await fs.readFile(pdfPath);
    const data = await pdfParse(buf);
    const text = data.text || '';

    const labels = {
        en: 'FIR ID',
        hi: 'FIR आईडी',
        ta: 'FIR ஐடி',
        te: 'FIR ఐడీ',
        ml: 'FIR ഐഡി',
        ka: 'FIR ಐಡಿ',
    };

    const label = labels[lang] || labels.en;
    console.log('Extracted text length:', text.length);
    if (text.includes(label)) {
        console.log('Verified: label found for', lang);
        process.exit(0);
    } else {
        console.error('Label not found for', lang);
        process.exit(3);
    }
}

main().catch((e) => { console.error(e); process.exit(1); });
