import FIRService from '../services/FIRService.js';
import AIService from '../services/AIService.js';

class FIRController {
    /**
     * Create FIR report
     */
    async createFIR(req, res, next) {
        try {
            const { userId } = req.params;
            const firData = req.body;

            const fir = await FIRService.createFIRReport(userId, firData);

            res.status(201).json({
                success: true,
                data: fir,
            });
        } catch (error) {
            next(error);
        }
    }

    /**
     * Generate FIR draft from incident
     */
    async generateDraft(req, res, next) {
        try {
            const { userId } = req.params;
            const { incidentData, language } = req.body;

            const fir = await FIRService.generateFIRDraft(userId, incidentData, language || 'en');

            res.status(201).json({
                success: true,
                data: fir,
            });
        } catch (error) {
            next(error);
        }
    }

    /**
     * Get user's FIR reports
     */
    async getUserFIRs(req, res, next) {
        try {
            const { userId } = req.params;

            const reports = await FIRService.getUserFIRReports(userId);

            res.status(200).json({
                success: true,
                data: reports,
            });
        } catch (error) {
            next(error);
        }
    }

    /**
     * Get specific FIR
     */
    async getFIR(req, res, next) {
        try {
            const { firId } = req.params;

            const report = await FIRService.getFIRReport(firId);

            res.status(200).json({
                success: true,
                data: report,
            });
        } catch (error) {
            next(error);
        }
    }

    /**
     * Update FIR
     */
    async updateFIR(req, res, next) {
        try {
            const { firId } = req.params;
            const updateData = req.body;

            const report = await FIRService.updateFIRReport(firId, updateData);

            res.status(200).json({
                success: true,
                data: report,
            });
        } catch (error) {
            next(error);
        }
    }

    /**
     * Delete FIR
     */
    async deleteFIR(req, res, next) {
        try {
            const { firId } = req.params;

            await FIRService.deleteFIRReport(firId);

            res.status(200).json({
                success: true,
                message: 'FIR deleted successfully',
            });
        } catch (error) {
            next(error);
        }
    }

    /**
     * Finalize (submit) FIR
     */
    async finalizeFIR(req, res, next) {
        try {
            const { firId } = req.params;

            const report = await FIRService.finalizeFIR(firId);

            res.status(200).json({
                success: true,
                data: report,
            });
        } catch (error) {
            next(error);
        }
    }

    /**
     * Get evidence checklist for crime category
     */
    async getEvidenceChecklist(req, res, next) {
        try {
            const { crimeCategory, language } = req.body;

            const checklist = await AIService.getEvidenceChecklist(crimeCategory, language || 'en');

            res.status(200).json({
                success: true,
                data: checklist,
            });
        } catch (error) {
            next(error);
        }
    }

    /**
     * Generate PDF of FIR
     */
    async generatePDF(req, res, next) {
        try {
            const { firId } = req.params;
            const { language } = req.query;

            const pdfBuffer = await FIRService.generatePDF(firId, language || 'en');

            res.setHeader('Content-Type', 'application/pdf');
            res.setHeader('Content-Disposition', `attachment; filename="FIR-${firId}.pdf"`);
            return res.send(pdfBuffer);
        } catch (error) {
            next(error);
        }
    }
}

export default new FIRController();
