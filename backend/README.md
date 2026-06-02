# Backend configuration

This document explains minimal environment and run steps for the backend features added (PDF generation, QR codes, email-on-finalize).

Required environment variables

- `APP_BASE_URL` (or `FRONTEND_URL`): Public URL where the frontend is served. Used to build QR links included in PDFs. Default: `http://localhost:5173`.
- `SMTP_HOST`: SMTP server host (required to enable email sending).
- `SMTP_PORT`: SMTP port (default `587`).
- `SMTP_USER`: SMTP username (for auth).
- `SMTP_PASS`: SMTP password (for auth).
- `SMTP_SECURE`: Set to `true` (or any non-empty value) if using a secure port (465).
- `MAIL_FROM`: Optional from address (e.g. `"AI Legal Assistant <no-reply@example.org>"`). If not set, `SMTP_USER` will be used.

Notes

- Puppeteer is used to render HTML → PDF. Installing dependencies will download a Chromium binary which can be large.
  - In production, consider using `puppeteer-core` and supplying an existing Chromium/Chrome binary to reduce install size.
- If SMTP is not configured, finalize will still mark the FIR submitted but skip sending email and log a message.
- QR codes are generated using the `qrcode` package and embedded as data URLs into the PDF header.

Run locally

1. Install backend dependencies (may download Chromium):

```bash
cd backend
npm install
```

2. Create a `.env` file using `.env.example` as a template and set real values.

3. Start the dev server:

```bash
npm run dev
```

Testing email flow

- Set valid SMTP settings in `.env` and ensure the complainant or user email exists on the FIR record.
- Finalize a FIR via the API or the frontend; the server will generate a PDF and attempt to send it as an attachment.

Security

- Do not commit `.env` with real credentials to source control. Use secrets management in production.
- Consider using transactional email providers (SendGrid, Mailgun) for reliable delivery and monitoring.

Contact

For further changes (logo, QR placement, localized templates), edit `backend/services/FIRService.js` where the HTML template is constructed.
