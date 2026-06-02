import FIRReport from '../models/FIRReport.js';
import AIService from './AIService.js';
import User from '../models/User.js';

import QRCode from 'qrcode';
import nodemailer from 'nodemailer';
import sgMail from '@sendgrid/mail';
import fs from 'fs/promises';
import path from 'path';

function escapeHtml(input) {
    if (input === null || input === undefined) return '';
    return String(input)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
}

class FIRService {
    /**
     * Create new FIR report
     */
    async createFIRReport(userId, firData) {
        try {
            const firReport = new FIRReport({
                userId,
                ...firData,
            });
            await firReport.save();
            return firReport;
        } catch (error) {
            console.error('Error creating FIR report:', error);
            throw new Error('Failed to create FIR report');
        }
    }

    /**
     * Generate FIR draft from incident details
     */
    async generateFIRDraft(userId, incidentData, language = 'en') {
        try {
            // If crimeCategory not provided, attempt to analyze from incidentDetails
            let crimeCategory = incidentData.crimeCategory;
            let ipcSections = incidentData.ipcSections || [];
            if (!crimeCategory && incidentData.incidentDetails) {
                try {
                    const analysis = await AIService.analyzeCrimeCategory(incidentData.incidentDetails, language);
                    crimeCategory = analysis.category;
                    ipcSections = analysis.ipcSections || ipcSections;
                } catch (e) {
                    console.warn('Crime category analysis failed, proceeding without it', e.message);
                }
            }

            const draft = await AIService.generateFIRDraft(incidentData, language);

            // Create FIR report record
            const firReport = await this.createFIRReport(userId, {
                title: incidentData.title || `FIR - ${new Date().toLocaleDateString()}`,
                incidentDetails: incidentData.incidentDetails,
                incidentDate: incidentData.incidentDate,
                incidentLocation: incidentData.incidentLocation,
                crimeCategory,
                ipcSections,
                complainantDetails: incidentData.complainantDetails,
                suspectDetails: incidentData.suspectDetails,
                witnessDetails: incidentData.witnessDetails,
                evidence: incidentData.evidence,
                firDraft: draft,
                language,
            });

            return firReport;
        } catch (error) {
            console.error('Error generating FIR draft:', error);
            throw new Error('Failed to generate FIR draft');
        }
    }

    /**
     * Get user's FIR reports
     */
    async getUserFIRReports(userId) {
        try {
            const reports = await FIRReport.find({ userId }).sort({ createdAt: -1 });
            return reports;
        } catch (error) {
            console.error('Error retrieving FIR reports:', error);
            throw new Error('Failed to retrieve FIR reports');
        }
    }

    /**
     * Get specific FIR report
     */
    async getFIRReport(firId) {
        try {
            const report = await FIRReport.findById(firId);
            if (!report) {
                throw new Error('FIR report not found');
            }
            return report;
        } catch (error) {
            console.error('Error retrieving FIR report:', error);
            throw new Error('Failed to retrieve FIR report');
        }
    }

    /**
     * Update FIR report
     */
    async updateFIRReport(firId, updateData) {
        try {
            const report = await FIRReport.findByIdAndUpdate(firId, updateData, { new: true });
            if (!report) {
                throw new Error('FIR report not found');
            }
            return report;
        } catch (error) {
            console.error('Error updating FIR report:', error);
            throw new Error('Failed to update FIR report');
        }
    }

    /**
     * Delete FIR report
     */
    async deleteFIRReport(firId) {
        try {
            await FIRReport.findByIdAndDelete(firId);
            return { success: true, message: 'FIR report deleted' };
        } catch (error) {
            console.error('Error deleting FIR report:', error);
            throw new Error('Failed to delete FIR report');
        }
    }

    /**
     * Convert FIR to PDF (placeholder for actual implementation)
     */
        async generatePDF(firId, language = 'en') {
                try {
                        const report = await this.getFIRReport(firId);

                            // Resolve language: prefer explicit param, then report.language, fallback to 'en'
                            const lang = (language || (report && report.language) || 'en').toLowerCase();

                            // Localized labels for PDF template
                            const labelsMap = {
                                en: {
                                    titleMain: 'First Information Report (FIR)',
                                    meta: 'AI Legal Assistant — Official Draft',
                                    generated: 'Generated',
                                    firId: 'FIR ID',
                                    title: 'Title',
                                    status: 'Status',
                                    submittedAt: 'Submitted At',
                                    complainantDetails: 'Complainant Details',
                                    name: 'Name',
                                    phone: 'Phone',
                                    email: 'Email',
                                    address: 'Address',
                                    incidentDetails: 'Incident Details',
                                    date: 'Date',
                                    location: 'Location',
                                    crimeCategory: 'Crime Category',
                                    details: 'Details',
                                    witnesses: 'Witnesses',
                                    evidence: 'Evidence',
                                    aiDraft: 'AI-generated FIR Draft',
                                    footer: 'AI Legal Assistant — For informational purposes only. Contact: support@example.org',
                                },
                                hi: {
                                    titleMain: 'प्राथमिक सूचना रिपोर्ट (FIR)',
                                    meta: 'AI लीगल असिस्टेंट — आधिकारिक मसौदा',
                                    generated: 'जनरेट किया गया',
                                    firId: 'FIR आईडी',
                                    title: 'शीर्षक',
                                    status: 'स्थिति',
                                    submittedAt: 'प्रस्तुत किया गया',
                                    complainantDetails: 'शिकायतकर्ता का विवरण',
                                    name: 'नाम',
                                    phone: 'फ़ोन',
                                    email: 'ईमेल',
                                    address: 'पता',
                                    incidentDetails: 'घटना का विवरण',
                                    date: 'तारीख',
                                    location: 'स्थान',
                                    crimeCategory: 'अपराध श्रेणी',
                                    details: 'विवरण',
                                    witnesses: 'गवाह',
                                    evidence: 'साक्ष्य',
                                    aiDraft: 'एआई-जनित FIR मसौदा',
                                    footer: 'सूचना के लिए: AI लीगल असिस्टेंट। हमेशा वकील से परामर्श करें।',
                                },
                                ta: {
                                    titleMain: 'முதல் தகவல் அறிக்கை (FIR)',
                                    meta: 'AI லீகல் அசிஸ்டண்ட் — அதிகாரப்பூர்வ வரைவு',
                                    generated: 'உருவாக்கப்பட்டது',
                                    firId: 'FIR ஐடி',
                                    title: 'தலைப்பு',
                                    status: 'நிலை',
                                    submittedAt: 'சமர்ப்பிக்கப்பட்ட தேதி',
                                    complainantDetails: 'புகார் தருமவர் விவரங்கள்',
                                    name: 'பெயர்',
                                    phone: 'தெலைபேசி',
                                    email: 'மின்னஞ்சல்',
                                    address: 'முகவரி',
                                    incidentDetails: 'நிகழ்வு விவரம்',
                                    date: 'தேதி',
                                    location: 'இடம்',
                                    crimeCategory: 'குற்ற வகை',
                                    details: 'விவரங்கள்',
                                    witnesses: 'சாட்சிகள்',
                                    evidence: 'சான்றுகள்',
                                    aiDraft: 'ஏ.ஐ. உருவாக்கிய FIR வரைவு',
                                    footer: 'அறிவிப்பு: AI லீகல் அசிஸ்டண்ட் — தகவல उद्देश्यத்திற்காக. ஆலோசனைக்கு வழக்கு வழக்கறிஞரை அணுகவும்.',
                                },
                                te: {
                                    titleMain: 'మొదటి సమాచారం నివేదనం (FIR)',
                                    meta: 'AI లీగల్ అసిస్టెంట్ — అధికారిక ముసాయిదా',
                                    generated: 'సృష్టించబడినది',
                                    firId: 'FIR ఐడీ',
                                    title: 'శీర్షిక',
                                    status: 'స్థితి',
                                    submittedAt: 'సమర్పించిన సమయం',
                                    complainantDetails: 'ఫిర్యాదుదారు వివరాలు',
                                    name: 'పేరు',
                                    phone: 'ఫోన్',
                                    email: 'ఈమెయిల్',
                                    address: 'చిరునామా',
                                    incidentDetails: ' సంఘటన వివరాలు',
                                    date: 'తేదీ',
                                    location: 'స్థానం',
                                    crimeCategory: 'నేర వర్గం',
                                    details: 'వివరాలు',
                                    witnesses: 'సాక్షులు',
                                    evidence: 'సాక్ష్యాలు',
                                    aiDraft: 'ఏఐ రూపొందించిన FIR ముసాయిదా',
                                    footer: 'సూచన: AI లీగల్ అసిస్టెంట్ — సమాచారపూర్వకంగా మాత్రమే. చట్టసంబంధి సలహాల కోసం న్యాయవాది ని సంప్రదించండి.',
                                },
                                ml: {
                                    titleMain: 'ആദ്യ റിപ്പോർട്ട് (FIR)',
                                    meta: 'AI ലീഗൽ അസിസ്റ്റന്റ് — ഔദ്യോഗിക ഡ്രാഫ്റ്റ്',
                                    generated: 'സൃഷ്ടിച്ചത്',
                                    firId: 'FIR ഐഡി',
                                    title: 'തലക്കെട്ട്',
                                    status: ' നില',
                                    submittedAt: 'സമർപ്പിച്ചത്',
                                    complainantDetails: 'പരാതികര് വിവരങ്ങള്',
                                    name: 'പേര്',
                                    phone: 'ഫോൺ',
                                    email: 'ഇമെയിൽ',
                                    address: 'വിലാസം',
                                    incidentDetails: 'സംഭവത്തിന്റെ വിശദാംശങ്ങൾ',
                                    date: 'തിയതി',
                                    location: 'സ്ഥലം',
                                    crimeCategory: 'ഒരു കുറ്റ വക klase',
                                    details: 'വിവരങ്ങൾ',
                                    witnesses: 'സാക്ഷികൾ',
                                    evidence: 'സാക്ഷ്യങ്ങൾ',
                                    aiDraft: 'AI-ചെയ്ത FIR ഡ്രാഫ്റ്റ്',
                                    footer: 'അറിയിപ്പ്: AI ലീഗൽ അസിസ്റ്റന്റ് — വെറും വിവരാനുകൂല്യത്തിന്. നിയമസഹായത്തിന് ഒരു അഭിഭാഷകനെ സമീപിക്കുക.',
                                },
                                ka: {
                                    titleMain: 'ಪ್ರಾಥಮಿಕ ಮಾಹಿತಿ ವರದಿ (FIR)',
                                    meta: 'AI ಲೆಗ್ಗಲ್ ಅಸಿಸ್ಟೆಂಟ್ — ಅಧಿಕೃತ návrہ',
                                    generated: 'ರಚಿಸಲಾಗಿದೆ',
                                    firId: 'FIR ಐಡಿ',
                                    title: 'ಶೀರ್ಷಿಕೆ',
                                    status: 'ಸ್ಥಿತಿ',
                                    submittedAt: 'ಸಲ್ಲಿಸಲಾಗಿದೆ',
                                    complainantDetails: 'ಫಿರ್ಯಾದಿದಾರರ ವಿವರಗಳು',
                                    name: 'ಹೆಸರು',
                                    phone: 'ದೂರವಾಣಿ',
                                    email: 'ಇಮೇಲ್',
                                    address: 'ವಿಳಾಸ',
                                    incidentDetails: 'ಘಟನೆಯ ವಿವರಗಳು',
                                    date: 'ದಿನಾಂಕ',
                                    location: 'ಸ್ಥಳ',
                                    crimeCategory: ' ಅಪರಾಧ ವರ್ಗ',
                                    details: 'ವಿವರಗಳು',
                                    witnesses: 'ಪ್ರಕಾಶಕರು',
                                    evidence: 'ಸಾಕ್ಷಿಗಳು',
                                    aiDraft: 'AI ರಚಿತ FIR খಾಕು',
                                    footer: 'ಯುಪಯೋಗಕ್ಕಾಗಿ: AI ಲೆಗ್ಗಲ್ ಅಸಿಸ್ಟೆಂಟ್ — ಮಾಹಿತಿಪೂರಕ ಮಾತ್ರ. ಕಾನೂನು ಸಲಹೆಗೆ ವಕೀಲರನ್ನು ಸಂಪರ್ಕಿಸಿ.',
                                },
                            };

                            const labels = labelsMap[lang] || labelsMap.en;

                        // Render HTML and convert to PDF using Puppeteer for richer styling
                        const puppeteerModule = await import('puppeteer');
                        const puppeteer = puppeteerModule.default || puppeteerModule;
                        const browser = await puppeteer.launch({ args: ['--no-sandbox', '--disable-setuid-sandbox'] });
                        const page = await browser.newPage();

                        const witnessesHtml = (report.witnessDetails || [])
                                .map((w, i) => `<div class="item"><div class="item-title">${i + 1}. ${escapeHtml(w.name || '—')}</div><div class="item-meta">Phone: ${escapeHtml(w.phone || '—')}</div><div class="item-text">${escapeHtml(w.statement || '')}</div></div>`)
                                .join('');

                        const evidenceHtml = (report.evidence || []).map((e, i) => `<div class="item">${i + 1}. ${escapeHtml(e)}</div>`).join('');

                        const watermark = report.status === 'draft' ? `<div class="watermark">DRAFT</div>` : '';

                        // Generate QR code pointing to the FIR view page
                        const baseUrl = (process.env.APP_BASE_URL || process.env.FRONTEND_URL || 'http://localhost:5173').replace(/\/$/, '');
                        const firUrl = `${baseUrl}/my-firs?fir=${report._id}`;
                        let qrDataUrl = '';
                        try {
                            qrDataUrl = await QRCode.toDataURL(firUrl);
                        } catch (e) {
                            console.warn('QR generation failed', e.message);
                        }

                        // Translate FIR draft/details when requested language is not English
                        let draftText = report.firDraft || report.incidentDetails || '';
                        let detailsText = report.incidentDetails || report.firDraft || '';
                        if (lang !== 'en') {
                            try {
                                draftText = await AIService.translateText(draftText, lang);
                                detailsText = await AIService.translateText(detailsText, lang);
                            } catch (e) {
                                console.warn('Translation for PDF failed, falling back to original:', e.message);
                            }
                        }

                        // Try to embed a logo image if available
                        let logoImgTag = `<svg class="logo" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="logo">
                                            <rect width="48" height="48" rx="6" fill="#0f172a" />
                                            <path d="M14 24h20M14 18h20M14 30h20" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                                        </svg>`;
                        try {
                            const logoPath = path.resolve(process.cwd(), 'backend', 'assets', 'logo.png');
                            const logoBuffer = await fs.readFile(logoPath);
                            const logoBase64 = logoBuffer.toString('base64');
                            logoImgTag = `<img class="logo" src="data:image/png;base64,${logoBase64}" alt="logo" style="width:48px;height:48px;border-radius:6px;object-fit:cover;"/>`;
                        } catch (e) {
                            // no logo found, keep svg
                        }

                        const html = `<!doctype html>
                        <html>
                        <head>
                            <meta charset="utf-8" />
                            <meta name="viewport" content="width=device-width,initial-scale=1" />
                            <style>
                                body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial; color:#111; }
                                .container { max-width:820px; margin:0 auto; padding:28px; position:relative; }
                                .header { background:#0f172a; color: #fff; padding:14px 18px; display:flex; justify-content:space-between; align-items:center; border-radius:6px; }
                                .brand { display:flex; align-items:center; gap:12px; }
                                .logo { width:48px; height:48px; }
                                .title { font-size:18px; font-weight:800; letter-spacing:0.4px; }
                                .meta { font-size:11px; color:#e2e8f0; }
                                .hr { height:1px; background:#e5e7eb; margin:18px 0; }
                                .section { margin-top:12px; }
                                .kv { display:flex; margin:8px 0; }
                                .label { width:160px; font-weight:700; color:#0f172a; }
                                .value { flex:1; }
                                .section-title { font-size:13px; font-weight:700; margin-top:6px; color:#0b1220; }
                                .item { margin-bottom:8px; }
                                .item-title { font-weight:700; }
                                .draft { page-break-before: always; white-space: pre-wrap; }
                                .watermark { position:fixed; top:40%; left:10%; font-size:80px; color:rgba(0,0,0,0.08); transform:rotate(-25deg); pointer-events:none; z-index:0; }
                                .footer { position:fixed; bottom:18px; left:0; right:0; font-size:10px; color:#666; text-align:center; }
                                .card { background:#fff; border-radius:6px; padding:12px; box-shadow:0 1px 2px rgba(15,23,42,0.04); }
                            </style>
                        </head>
                        <body>
                            <div class="container card">
                                ${watermark}
                                <div class="header">
                                    <div class="brand">
                                        ${logoImgTag}
                                        <div>
                                            <div class="title">${escapeHtml(labels.titleMain)}</div>
                                            <div class="meta">${escapeHtml(labels.meta)}</div>
                                        </div>
                                    </div>
                                    <div style="display:flex;flex-direction:column;align-items:flex-end;gap:6px;">
                                        <div class="meta">${escapeHtml(labels.generated)}: ${new Date().toLocaleString()}</div>
                                        ${qrDataUrl ? `<img src="${qrDataUrl}" style="width:84px;border:1px solid rgba(0,0,0,0.06);border-radius:6px;" alt="QR"/>` : ''}
                                    </div>
                                </div>
                                <div class="hr"></div>

                                <div class="section">
                                    <div class="kv"><div class="label">${escapeHtml(labels.firId)}</div><div class="value">${escapeHtml(String(report._id))}</div></div>
                                    <div class="kv"><div class="label">${escapeHtml(labels.title)}</div><div class="value">${escapeHtml(report.title || '—')}</div></div>
                                    <div class="kv"><div class="label">${escapeHtml(labels.status)}</div><div class="value">${escapeHtml(report.status || 'draft')}</div></div>
                                    <div class="kv"><div class="label">${escapeHtml(labels.submittedAt)}</div><div class="value">${report.submittedAt ? escapeHtml(new Date(report.submittedAt).toLocaleString()) : '—'}</div></div>
                                </div>

                                <div class="section">
                                    <div class="section-title">${escapeHtml(labels.complainantDetails)}</div>
                                    <div class="kv"><div class="label">${escapeHtml(labels.name)}</div><div class="value">${escapeHtml((report.complainantDetails && report.complainantDetails.name) || '—')}</div></div>
                                    <div class="kv"><div class="label">${escapeHtml(labels.phone)}</div><div class="value">${escapeHtml((report.complainantDetails && report.complainantDetails.phone) || '—')}</div></div>
                                    <div class="kv"><div class="label">${escapeHtml(labels.email)}</div><div class="value">${escapeHtml((report.complainantDetails && report.complainantDetails.email) || '—')}</div></div>
                                    <div class="kv"><div class="label">${escapeHtml(labels.address)}</div><div class="value">${escapeHtml((report.complainantDetails && report.complainantDetails.address) || '—')}</div></div>
                                </div>

                                <div class="section">
                                    <div class="section-title">${escapeHtml(labels.incidentDetails)}</div>
                                    <div class="kv"><div class="label">${escapeHtml(labels.date)}</div><div class="value">${report.incidentDate ? escapeHtml(new Date(report.incidentDate).toLocaleString()) : '—'}</div></div>
                                    <div class="kv"><div class="label">${escapeHtml(labels.location)}</div><div class="value">${escapeHtml(report.incidentLocation || '—')}</div></div>
                                    <div class="kv"><div class="label">${escapeHtml(labels.crimeCategory)}</div><div class="value">${escapeHtml(report.crimeCategory || '—')}</div></div>
                                </div>

                                <div class="section">
                                    <div class="section-title">${escapeHtml(labels.details)}</div>
                                    <div class="value">${escapeHtml(detailsText || '—')}</div>
                                </div>

                                ${report.witnessDetails && report.witnessDetails.length ? `<div class="section"><div class="section-title">${escapeHtml(labels.witnesses)}</div>${witnessesHtml}</div>` : ''}

                                ${report.evidence && report.evidence.length ? `<div class="section"><div class="section-title">${escapeHtml(labels.evidence)}</div>${evidenceHtml}</div>` : ''}

                                <div class="draft">
                                    <div class="section-title">${escapeHtml(labels.aiDraft)}</div>
                                    <div class="value">${escapeHtml(draftText || '—')}</div>
                                </div>
                            </div>
                            <div class="footer">${escapeHtml(labels.footer)}</div>
                        </body>
                        </html>`;

                        await page.setContent(html, { waitUntil: 'networkidle0' });

                        const pdfBuffer = await page.pdf({
                                format: 'A4',
                                printBackground: true,
                                margin: { top: '40px', bottom: '60px', left: '40px', right: '40px' },
                                displayHeaderFooter: true,
                                headerTemplate: '<div></div>',
                                footerTemplate: '<div style="font-size:10px; width:100%; text-align:center; color:#666;"><span class="pageNumber"></span> / <span class="totalPages"></span></div>',
                        });

                        await browser.close();
                        return pdfBuffer;
                } catch (error) {
                        console.error('Error generating PDF:', error);
                        throw new Error('Failed to generate PDF');
                }
        }

    /**
     * Finalize (submit) FIR report: mark as submitted and trigger PDF generation
     */
    async finalizeFIR(firId) {
        try {
            const now = new Date();
            const report = await FIRReport.findByIdAndUpdate(
                firId,
                { status: 'submitted', submittedAt: now },
                { new: true }
            );
            if (!report) throw new Error('FIR report not found');

            // Generate PDF and email to complainant/user if email configured
            try {
                const pdfBuffer = await this.generatePDF(firId, report.language);

                // Determine recipient
                let recipient = report.complainantDetails && report.complainantDetails.email;
                if (!recipient && report.userId) {
                    const user = await User.findById(report.userId).select('email');
                    if (user && user.email) recipient = user.email;
                }

                const smtpHost = process.env.SMTP_HOST;
                if (recipient && smtpHost) {
                    const transporter = nodemailer.createTransport({
                        host: process.env.SMTP_HOST,
                        port: Number(process.env.SMTP_PORT || 587),
                        secure: !!process.env.SMTP_SECURE, // true for 465, false for other ports
                        auth: {
                            user: process.env.SMTP_USER,
                            pass: process.env.SMTP_PASS,
                        },
                    });

                    const mailFrom = process.env.MAIL_FROM || process.env.SMTP_USER;
                    const mailOptions = {
                        from: mailFrom,
                        to: recipient,
                        subject: `FIR Submitted — ${report.title || report._id}`,
                        text: `Your FIR (${report._id}) has been submitted. Attached is the PDF copy.`,
                        attachments: [
                            { filename: `FIR-${report._id}.pdf`, content: pdfBuffer },
                        ],
                    };

                    transporter.sendMail(mailOptions).then((info) => {
                        console.log('FIR email sent:', info.messageId);
                    }).catch((err) => console.error('Failed to send FIR email', err));
                } else if (process.env.SENDGRID_API_KEY) {
                    // Fallback to SendGrid if configured
                    try {
                        sgMail.setApiKey(process.env.SENDGRID_API_KEY);
                        const sgMsg = {
                            to: recipient,
                            from: process.env.MAIL_FROM || process.env.SMTP_USER || 'no-reply@example.com',
                            subject: `FIR Submitted — ${report.title || report._id}`,
                            text: `Your FIR (${report._id}) has been submitted. Attached is the PDF copy.`,
                            attachments: [
                                {
                                    content: pdfBuffer.toString('base64'),
                                    filename: `FIR-${report._id}.pdf`,
                                    type: 'application/pdf',
                                    disposition: 'attachment',
                                },
                            ],
                        };
                        await sgMail.send(sgMsg);
                        console.log('FIR email sent via SendGrid');
                    } catch (err) {
                        console.error('SendGrid send failed', err);
                    }
                } else {
                    if (!recipient) console.log('No recipient email available for FIR', firId);
                    if (!smtpHost) console.log('SMTP not configured, skipping email send');
                }
            } catch (err) {
                console.error('Error generating PDF or sending email on finalize', err);
            }

            return report;
        } catch (error) {
            console.error('Error finalizing FIR report:', error);
            throw new Error('Failed to finalize FIR report');
        }
    }
}

export default new FIRService();
