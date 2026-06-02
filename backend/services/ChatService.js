import ChatSession from '../models/ChatSession.js';
import AIService from './AIService.js';
import LanguageDetectionService from './LanguageDetectionService.js';

class ChatService {
    /**
     * Create a new chat session
     */
    async createChatSession(userId, language = 'en') {
        try {
            const session = new ChatSession({
                userId,
                language,
                title: `Chat - ${new Date().toLocaleDateString()}`,
            });
            await session.save();
            return session;
        } catch (error) {
            console.error('Error creating chat session:', error);
            throw new Error('Failed to create chat session');
        }
    }

    /**
     * Add message to chat and get response
     */
    async sendMessage(sessionId, userMessage, language = 'en') {
        try {
            // Detect language if not provided
            if (!language || language === 'auto') {
                language = await LanguageDetectionService.detectLanguage(userMessage);
            }

            // Get chat session
            const session = await ChatSession.findById(sessionId);
            if (!session) {
                throw new Error('Chat session not found');
            }

            // Add user message to session
            session.messages.push({
                role: 'user',
                content: userMessage,
                language,
            });

            // Translate to English for AI processing if needed
            let processMessage = userMessage;
            if (language !== 'en') {
                processMessage = await AIService.translateText(userMessage, 'en');
            }

            // Analyze for crime category
            let crimeAnalysis = null;
            try {
                crimeAnalysis = await AIService.analyzeCrimeCategory(processMessage, 'en');
                if (crimeAnalysis) {
                    session.crimeCategory = crimeAnalysis.category;
                    session.ipcSections = crimeAnalysis.ipcSections;
                    session.bnsSections = crimeAnalysis.bnsSections;
                }
            } catch (error) {
                console.log('Could not analyze crime category:', error.message);
            }

            // Generate AI response
            let aiResponse = await AIService.generateLegalGuidance(processMessage, session.crimeCategory || 'General', 'en');

            // Translate response back to user language if needed
            if (language !== 'en') {
                aiResponse = await AIService.translateText(aiResponse, language);
            }

            // Add assistant message to session
            session.messages.push({
                role: 'assistant',
                content: aiResponse,
                language,
                detectedCrimeCategory: crimeAnalysis?.category,
                relevantIPCSection: crimeAnalysis?.ipcSections?.[0],
                relevantBNSSection: crimeAnalysis?.bnsSections?.[0],
            });

            await session.save();

            return {
                sessionId: session._id,
                userMessage,
                assistantResponse: aiResponse,
                crimeCategory: session.crimeCategory,
                ipcSections: session.ipcSections,
                bnsSections: session.bnsSections,
                language,
            };
        } catch (error) {
            console.error('Error sending message:', error);
            throw new Error('Failed to send message: ' + error.message);
        }
    }

    /**
     * Get chat history
     */
    async getChatHistory(sessionId) {
        try {
            const session = await ChatSession.findById(sessionId);
            if (!session) {
                throw new Error('Chat session not found');
            }
            return session;
        } catch (error) {
            console.error('Error retrieving chat history:', error);
            throw new Error('Failed to retrieve chat history');
        }
    }

    /**
     * Get all chat sessions for a user
     */
    async getUserChatSessions(userId) {
        try {
            const sessions = await ChatSession.find({ userId }).sort({ createdAt: -1 });
            return sessions;
        } catch (error) {
            console.error('Error retrieving user sessions:', error);
            throw new Error('Failed to retrieve chat sessions');
        }
    }

    /**
     * Delete chat session
     */
    async deleteChatSession(sessionId) {
        try {
            await ChatSession.findByIdAndDelete(sessionId);
            return { success: true, message: 'Chat session deleted' };
        } catch (error) {
            console.error('Error deleting chat session:', error);
            throw new Error('Failed to delete chat session');
        }
    }
}

export default new ChatService();
