import { test, expect } from '@playwright/test';

const FRONTEND = process.env.FRONTEND_URL || 'http://localhost:3000';

test('UI flow: register, generate FIR, finalize, download PDF', async ({ page }) => {
  // Debug logging
  page.on('console', msg => console.log('BROWSER CONSOLE:', msg.text()));
  page.on('pageerror', err => console.log('BROWSER ERROR:', err.message));
  page.on('requestfailed', req => console.log('BROWSER REQ FAILED:', req.url(), req.failure().errorText));

  // Auto-accept ALL dialogs (confirms + alerts) throughout the test
  page.on('dialog', async (dialog) => {
    console.log(`DIALOG [${dialog.type()}]: ${dialog.message()}`);
    await dialog.accept();
  });

  // ── Step 1: Register via UI ────────────────────────────────────────────
  const email = `pw+${Date.now()}@example.org`;
  const password = 'Password123!';

  await page.goto(`${FRONTEND}/auth`);
  await page.click('button:has-text("Register")');
  await page.fill('input[placeholder="Rajesh Kumar"]', 'PW Test');
  await page.fill('input[placeholder="you@example.com"]', email);
  await page.fill('input[placeholder="••••••••"]', password);
  await page.click('button:has-text("Create Account")');

  // Wait for registration to complete (dialog auto-accepted)
  await page.waitForTimeout(2000);

  // ── Step 2: Navigate to FIR generator ──────────────────────────────────
  await page.goto(`${FRONTEND}/fir-generator`);

  // Fill step 1 - incident info
  await page.fill('input[name=title]', 'Playwright FIR Test');
  await page.selectOption('select[name=crimeCategory]', 'Theft');
  await page.fill('textarea[name=incidentDetails]', 'This is a test incident created by Playwright.');
  await page.fill('input[name=incidentDate]', new Date().toISOString().split('T')[0]);
  await page.fill('input[name=incidentLocation]', 'Testville');
  await page.click('text=Next');

  // Fill step 2 - complainant details
  await page.fill('input[placeholder="Your name"]', 'PW Test');
  await page.fill('input[placeholder="Your phone number"]', '9999999999');
  await page.fill('input[placeholder="Your email"]', email);
  await page.fill('textarea[placeholder="Your address"]', '123 Test St');
  await page.click('text=Next');

  // Fill step 3 - additional details & generate
  await page.fill('textarea[placeholder^="List evidence"]', 'CCTV footage');
  await page.click('text=Generate FIR');

  // ── Step 3: Wait for draft and submit ──────────────────────────────────
  await page.waitForSelector('text=Submit Draft', { timeout: 60000 });
  await page.click('text=Submit Draft');

  // Wait for submission to complete
  await page.waitForTimeout(2000);

  // ── Step 4: Go to My FIRs, select, finalize ───────────────────────────
  await page.goto(`${FRONTEND}/my-firs`);
  await page.waitForSelector('ul li button', { timeout: 15000 });
  await page.click('ul li button');

  // Click Finalize (confirm dialog auto-accepted, then alert auto-accepted)
  await page.click('text=Finalize');

  // Wait for finalize flow (API call + alert + page refresh)
  await page.waitForTimeout(5000);

  // ── Step 5: Verify PDF download endpoint ──────────────────────────────
  const pdfLink = page.locator('a:has-text("Download PDF")');
  await pdfLink.waitFor({ state: 'visible', timeout: 10000 });
  const href = await pdfLink.getAttribute('href');
  expect(href).toBeTruthy();
  console.log('PDF link href:', href);

  // Fetch the PDF directly via Playwright's API request context
  const fullUrl = href.startsWith('http') ? href : `http://localhost:3000${href}`;
  const pdfResponse = await page.request.get(fullUrl);
  expect(pdfResponse.status()).toBe(200);
  expect(pdfResponse.headers()['content-type']).toContain('pdf');
  console.log('PDF response OK, content-type:', pdfResponse.headers()['content-type']);
});
