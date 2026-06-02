import mongoose from 'mongoose';

const messageSchema = new mongoose.Schema(
    {
        role: {
            type: String,
            enum: ['user', 'assistant'],
            required: true,
        },
        content: {
            type: String,
            required: true,
        },
        language: {
            type: String,
            enum: ['en', 'ta', 'hi', 'te', 'ml', 'ka'],
            default: 'en',
        },
        detectedCrimeCategory: String,
        relevantIPCSection: String,
        relevantBNSSection: String,
        sourceDocuments: [String],
    },
    { timestamps: true }
);

const chatSessionSchema = new mongoose.Schema(
    {
        userId: {
            type: mongoose.Schema.Types.ObjectId,
            ref: 'User',
            required: true,
        },
        title: {
            type: String,
            default: 'New Chat',
        },
        messages: [messageSchema],
        language: {
            type: String,
            enum: ['en', 'ta', 'hi', 'te', 'ml', 'ka'],
            default: 'en',
        },
        crimeCategory: String,
        ipcSections: [String],
        bnsSections: [String],
        isResolved: {
            type: Boolean,
            default: false,
        },
    },
    { timestamps: true }
);

const ChatSession = mongoose.model('ChatSession', chatSessionSchema);
export default ChatSession;
