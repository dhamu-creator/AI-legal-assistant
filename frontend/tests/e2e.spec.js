const { test, expect } = require('@playwright/test');

const API_BASE = process.env.API_BASE_URL || 'http://localhost:5000/api';
const FRONTEND = process.env.FRONTEND_URL || 'http://localhost:5173';

test('UI flow: register, generate FIR, finalize, download PDF', async ({ page }) => {
  // Register via UI
  const email = `pw+${Date.now()}@example.org`;
  const password = 'Password123!';

  await page.goto(`${FRONTEND}/auth`);
  // switch to register
  await page.click('text=Switch to register');
  await page.fill('input[placeholder="Full name"]', 'PW Test');
  await page.fill('input[placeholder="Email"]', email);
  await page.fill('input[placeholder="Password"]', password);
  // handle alert dialogs
  page.on('dialog', async (dialog) => {
    await dialog.accept();
  });
  await page.click('text=Register');

  // Navigate to FIR generator
  await page.goto(`${FRONTEND}/fir-generator`);

  // Fill step 1
  await page.fill('input[name=title]', 'Playwright FIR Test');
  await page.selectOption('select[name=crimeCategory]', 'Theft');
  await page.fill('textarea[name=incidentDetails]', 'This is a test incident created by Playwright.');
  await page.fill('input[name=incidentDate]', new Date().toISOString().split('T')[0]);
  await page.fill('input[name=incidentLocation]', 'Testville');
  await page.click('text=Next');

  // Step 2 - complainant
  await page.fill('input[placeholder="Your name"]', 'PW Test');
  await page.fill('input[placeholder="Your phone number"]', '9999999999');
  await page.fill('input[placeholder="Your email"]', email);
  await page.fill('textarea[placeholder="Your address"]', '123 Test St');
  await page.click('text=Next');

  // Step 3 - additional details
  await page.fill('textarea[placeholder^="List evidence"]', 'CCTV footage');
  await page.click('text=Generate FIR');

  // Wait for draft view and submit draft
  await page.waitForSelector('text=Your FIR Draft');
  await page.click('text=Submit Draft');

  // Go to My FIRs
  await page.goto(`${FRONTEND}/my-firs`);
  // select first FIR
  await page.waitForSelector('ul li button');
  await page.click('ul li button');

  // Intercept confirm and accept
  page.on('dialog', async (d) => { await d.accept(); });

  // Click Finalize
  await page.click('text=Finalize');

  // Click the Download PDF link and wait for response
  const pdfResponse = await page.waitForResponse((resp) => resp.url().includes('/fir/pdf/') && resp.status() === 200, { timeout: 20000 });
  expect(pdfResponse.headers()['content-type']).toContain('pdf');
});
