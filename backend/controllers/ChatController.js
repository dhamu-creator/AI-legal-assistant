import ChatService from '../services/ChatService.js';

class ChatController {
    /**
     * Create new chat session
     */
    async createSession(req, res, next) {
        try {
            const { userId, language } = req.body;

            if (!userId) {
                return res.status(400).json({
                    success: false,
                    message: 'User ID is required',
                });
            }

            const session = await ChatService.createChatSession(userId, language || 'en');

            res.status(201).json({
                success: true,
                data: session,
            });
        } catch (error) {
            next(error);
        }
    }

    /**
     * Send message to chat
     */
    async sendMessage(req, res, next) {
        try {
            const { sessionId, message, language } = req.body;

            if (!sessionId || !message) {
                return res.status(400).json({
                    success: false,
                    message: 'Session ID and message are required',
                });
            }

            const result = await ChatService.sendMessage(sessionId, message, language || 'en');

            res.status(200).json({
                success: true,
                data: result,
            });
        } catch (error) {
            next(error);
        }
    }

    /**
     * Get chat history
     */
    async getHistory(req, res, next) {
        try {
            const { sessionId } = req.params;

            const history = await ChatService.getChatHistory(sessionId);

            res.status(200).json({
                success: true,
                data: history,
            });
        } catch (error) {
            next(error);
        }
    }

    /**
     * Get all user chat sessions
     */
    async getUserSessions(req, res, next) {
        try {
            const { userId } = req.params;

            const sessions = await ChatService.getUserChatSessions(userId);

            res.status(200).json({
                success: true,
                data: sessions,
            });
        } catch (error) {
            next(error);
        }
    }

    /**
     * Delete chat session
     */
    async deleteSession(req, res, next) {
        try {
            const { sessionId } = req.params;

            await ChatService.deleteChatSession(sessionId);

            res.status(200).json({
                success: true,
                message: 'Chat session deleted',
            });
        } catch (error) {
            next(error);
        }
    }
}

export default new ChatController();
