import express from 'express';
import ChatController from '../controllers/ChatController.js';
import { validateChatMessage, validateLanguage } from '../middleware/validation.js';
import { chatLimiter } from '../middleware/rateLimit.js';

const router = express.Router();

/**
 * Chat Routes
 */

// Create new chat session
router.post('/session', ChatController.createSession);

// Send message to chat
router.post('/message', chatLimiter, validateChatMessage, validateLanguage, ChatController.sendMessage);

// Get chat history
router.get('/history/:sessionId', ChatController.getHistory);

// Get all user chat sessions
router.get('/sessions/:userId', ChatController.getUserSessions);

// Delete chat session
router.delete('/session/:sessionId', ChatController.deleteSession);

export default router;
