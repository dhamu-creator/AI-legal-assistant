import express from 'express';
import FIRController from '../controllers/FIRController.js';
import { validateFIRReport, validateLanguage } from '../middleware/validation.js';
import { apiLimiter } from '../middleware/rateLimit.js';

const router = express.Router();

/**
 * FIR Routes
 * IMPORTANT: Specific routes must be declared BEFORE parameterized routes (:firId)
 * to prevent route conflicts in Express.
 */

// Get evidence checklist (specific path — must come before /:firId)
router.post('/evidence/checklist', validateLanguage, FIRController.getEvidenceChecklist);

// Create new FIR report
router.post('/create/:userId', validateFIRReport, FIRController.createFIR);

// Generate FIR draft from incident
router.post('/generate/:userId', validateLanguage, FIRController.generateDraft);

// Finalize (submit) FIR (must come before /:firId)
router.post('/finalize/:firId', FIRController.finalizeFIR);

// Get user's FIR reports (must come before /:firId)
router.get('/user/:userId', FIRController.getUserFIRs);

// Generate PDF (must come before /:firId)
router.get('/pdf/:firId', FIRController.generatePDF);

// Get specific FIR (generic param route — must be AFTER all specific routes)
router.get('/:firId', FIRController.getFIR);

// Update FIR
router.put('/:firId', FIRController.updateFIR);

// Delete FIR
router.delete('/:firId', FIRController.deleteFIR);

export default router;
