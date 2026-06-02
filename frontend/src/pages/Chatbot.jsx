import React, { useState, useEffect, useRef } from 'react';
import { PaperAirplaneIcon, SparklesIcon, LanguageIcon } from '@heroicons/react/24/outline';
import { motion } from 'framer-motion';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';

export default function Chatbot() {
    const { user } = useAuth();
    const userId = user?.id || 'demo-user';
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);
    const [language, setLanguage] = useState('en');
    const [sessionId, setSessionId] = useState(null);
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    useEffect(() => {
        // Create new chat session on mount
        createSession();
    }, []);

    const createSession = async () => {
        try {
            const response = await axios.post('/api/chat/session', {
                userId,
                language,
            });
            setSessionId(response.data.data._id);
        } catch (error) {
            console.error('Error creating session:', error);
        }
    };

    const sendMessage = async (e) => {
        e.preventDefault();
        if (!input.trim() || loading || !sessionId) return;

        const userMessage = input;
        setInput('');
        setMessages((prev) => [...prev, { role: 'user', content: userMessage }]);
        setLoading(true);

        try {
            const response = await axios.post('/api/chat/message', {
                sessionId,
                message: userMessage,
                language,
            });

            const { assistantResponse, crimeCategory, ipcSections } = response.data.data;

            setMessages((prev) => [
                ...prev,
                {
                    role: 'assistant',
                    content: assistantResponse,
                    crimeCategory,
                    ipcSections,
                },
            ]);
        } catch (error) {
            console.error('Error sending message:', error);
            setMessages((prev) => [
                ...prev,
                {
                    role: 'assistant',
                    content: 'Sorry, I encountered an error. Please try again.',
                },
            ]);
        } finally {
            setLoading(false);
        }
    };

    const languages = [
        { code: 'en', name: 'English' },
        { code: 'ta', name: 'Tamil' },
        { code: 'hi', name: 'Hindi' },
        { code: 'te', name: 'Telugu' },
        { code: 'ml', name: 'Malayalam' },
        { code: 'ka', name: 'Kannada' },
    ];

    return (
        <div className="h-screen flex flex-col bg-gray-50">
            {/* Header */}
            <div className="bg-indigo-600 text-white p-4 shadow-lg">
                <div className="max-w-6xl mx-auto flex items-center justify-between">
                    <div className="flex items-center gap-2">
                        <SparklesIcon className="w-6 h-6" />
                        <h1 className="text-2xl font-bold">AI Legal Assistant</h1>
                    </div>
                    <div className="flex items-center gap-2">
                        <LanguageIcon className="w-5 h-5" />
                        <select
                            value={language}
                            onChange={(e) => setLanguage(e.target.value)}
                            className="bg-indigo-500 text-white px-3 py-1 rounded border border-indigo-400"
                        >
                            {languages.map((lang) => (
                                <option key={lang.code} value={lang.code}>
                                    {lang.name}
                                </option>
                            ))}
                        </select>
                    </div>
                </div>
            </div>

            {/* Chat Area */}
            <div className="flex-1 overflow-y-auto p-4">
                <div className="max-w-4xl mx-auto space-y-4">
                    {messages.length === 0 ? (
                        <motion.div
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            className="text-center py-12"
                        >
                            <SparklesIcon className="w-16 h-16 text-indigo-400 mx-auto mb-4" />
                            <h2 className="text-2xl font-semibold text-gray-800 mb-2">Welcome to AI Legal Assistant</h2>
                            <p className="text-gray-600 mb-6">
                                Tell me about your legal issue, and I'll help you understand your rights and options.
                            </p>
                            <div className="space-y-2 text-sm text-gray-600">
                                <p className="font-semibold">Examples:</p>
                                <p>• "My phone was stolen in a bus stand"</p>
                                <p>• "I received a threatening call from an unknown number"</p>
                                <p>• "How do I file a police complaint?"</p>
                            </div>
                        </motion.div>
                    ) : (
                        messages.map((msg, index) => (
                            <motion.div
                                key={index}
                                initial={{ opacity: 0, y: 10 }}
                                animate={{ opacity: 1, y: 0 }}
                                className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                            >
                                <div
                                    className={`max-w-2xl rounded-lg p-4 ${
                                        msg.role === 'user'
                                            ? 'bg-indigo-600 text-white'
                                            : 'bg-white text-gray-800 shadow'
                                    }`}
                                >
                                    <p className="whitespace-pre-wrap">{msg.content}</p>
                                    {msg.crimeCategory && (
                                        <div className="mt-3 pt-3 border-t border-opacity-30">
                                            <p className="text-sm font-semibold">
                                                Crime Category: {msg.crimeCategory}
                                            </p>
                                            {msg.ipcSections && (
                                                <p className="text-sm">
                                                    Relevant Sections: {msg.ipcSections.join(', ')}
                                                </p>
                                            )}
                                        </div>
                                    )}
                                </div>
                            </motion.div>
                        ))
                    )}
                    {loading && (
                        <div className="flex justify-start">
                            <div className="bg-white rounded-lg p-4 shadow">
                                <div className="flex gap-2">
                                    <div className="w-2 h-2 bg-indigo-600 rounded-full animate-bounce"></div>
                                    <div className="w-2 h-2 bg-indigo-600 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                                    <div className="w-2 h-2 bg-indigo-600 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                                </div>
                            </div>
                        </div>
                    )}
                    <div ref={messagesEndRef} />
                </div>
            </div>

            {/* Input Area */}
            <div className="bg-white border-t p-4">
                <div className="max-w-4xl mx-auto">
                    <form onSubmit={sendMessage} className="flex gap-3">
                        <input
                            type="text"
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            placeholder="Describe your legal issue..."
                            className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:border-indigo-500"
                            disabled={loading}
                        />
                        <button
                            type="submit"
                            disabled={loading || !input.trim()}
                            className="px-6 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 disabled:bg-gray-400 transition flex items-center gap-2"
                        >
                            <PaperAirplaneIcon className="w-5 h-5" />
                            Send
                        </button>
                    </form>
                    <p className="text-xs text-gray-500 mt-2">
                        ⚠️ This is AI-generated legal guidance. Always consult a lawyer for specific advice.
                    </p>
                </div>
            </div>
        </div>
    );
}
