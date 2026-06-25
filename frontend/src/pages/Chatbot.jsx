import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
    PaperAirplaneIcon,
    SparklesIcon,
    LanguageIcon,
    UserCircleIcon,
    TrashIcon,
    ArrowPathIcon,
    ShieldCheckIcon,
    DocumentTextIcon,
} from '@heroicons/react/24/outline';
import { useTranslation } from 'react-i18next';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import SpecializedWidget from '../components/SpecializedWidget';

const suggestedQuestions = [
    'What should I do if police refuse to file my FIR?',
    'What are my rights during arrest?',
    'How to file a cyber crime complaint?',
    'What is Section 498A IPC?',
    'How to apply for anticipatory bail?',
];

export default function Chatbot() {
    const { user } = useAuth();
    const userId = user?.id || '000000000000000000000000';
    const { t, i18n } = useTranslation();
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);
    const [language, setLanguage] = useState(i18n.language || 'en');
    const [sessionId, setSessionId] = useState(null);
    const messagesEndRef = useRef(null);
    const inputRef = useRef(null);

    useEffect(() => { setLanguage(i18n.language || 'en'); }, [i18n.language]);
    useEffect(() => { messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' }); }, [messages]);
    useEffect(() => { createSession(); }, []);

    const createSession = async () => {
        try {
            const res = await axios.post('/api/chat/session', { userId, language: i18n.language || 'en' });
            setSessionId(res.data.data._id);
        } catch (err) {
            console.error('Session error:', err);
        }
    };

    const clearChat = async () => {
        setMessages([]);
        await createSession();
    };

    const sendMessage = async (text) => {
        // Handle case where text is an event (though handleSubmit shouldn't pass it)
        const isEvent = text && typeof text === 'object' && text.nativeEvent;
        const msgText = isEvent ? input : (text || input);
        
        if (!msgText.trim() || loading) return;

        let currentSessionId = sessionId;
        
        // If session failed to create initially (e.g. backend was down), try creating it now
        if (!currentSessionId) {
            try {
                const res = await axios.post('/api/chat/session', { userId, language: i18n.language || 'en' });
                currentSessionId = res.data.data._id;
                setSessionId(currentSessionId);
            } catch (err) {
                console.error('Session error:', err);
                setMessages(prev => [...prev, {
                    role: 'assistant',
                    content: 'Cannot connect to the server. Please check your connection or reload the page.',
                    isError: true,
                }]);
                return;
            }
        }

        setInput('');
        setMessages(prev => [...prev, { role: 'user', content: msgText }]);
        setLoading(true);

        try {
            const res = await axios.post('/api/chat/message', { sessionId: currentSessionId, message: msgText, language });
            const { assistantResponse, crimeCategory, ipcSections, agentData, legal, evidence, severity, timeline, judgements, api_integration, language: detectedLang } = res.data.data;
            if (detectedLang && detectedLang !== language) {
                setLanguage(detectedLang);
                i18n.changeLanguage(detectedLang);
            }
            setMessages(prev => [...prev, { 
                role: 'assistant', 
                content: assistantResponse, 
                crimeCategory, 
                ipcSections, 
                agentData,
                legal,
                evidence,
                severity,
                timeline,
                judgements,
                api_integration
            }]);
        } catch (err) {
            setMessages(prev => [...prev, {
                role: 'assistant',
                content: 'I encountered an error. Please check your connection and try again.',
                isError: true,
            }]);
        } finally {
            setLoading(false);
            setTimeout(() => inputRef.current?.focus(), 100);
        }
    };

    const handleSubmit = (e) => { e.preventDefault(); sendMessage(); };

    const languages = [
        { code: 'en', name: 'English' },
        { code: 'ta', name: 'தமிழ்' },
        { code: 'hi', name: 'हिंदी' },
        { code: 'te', name: 'తెలుగు' },
        { code: 'ml', name: 'മലയാളം' },
        { code: 'ka', name: 'ಕನ್ನಡ' },
    ];

    return (
        <div className="flex flex-col" style={{ height: 'calc(100vh - 64px)', background: '#020817' }}>

            {/* ── Header ── */}
            <div className="flex-shrink-0 px-4 py-3 flex items-center justify-between"
                style={{ background: 'rgba(2,8,23,0.9)', borderBottom: '1px solid rgba(255,255,255,0.06)' }}>
                <div className="flex items-center gap-3">
                    <div className="w-9 h-9 rounded-xl flex items-center justify-center animate-pulse-glow"
                        style={{ background: 'linear-gradient(135deg,#6366f1,#4f46e5)' }}>
                        <SparklesIcon className="w-5 h-5 text-white" />
                    </div>
                    <div>
                        <h1 className="text-sm font-bold" style={{ color: '#f1f5f9' }}>{t('chatbot.title')}</h1>
                        <div className="flex items-center gap-1.5">
                            <div className="w-1.5 h-1.5 rounded-full bg-green-400" />
                            <span className="text-xs" style={{ color: '#64748b' }}>AI Online · Powered by Groq</span>
                        </div>
                    </div>
                </div>

                <div className="flex items-center gap-2">
                    {/* Language */}
                    <div className="flex items-center gap-1.5 px-2 py-1 rounded-lg"
                        style={{ background: 'rgba(255,255,255,0.04)', border: '1px solid rgba(255,255,255,0.06)' }}>
                        <LanguageIcon className="w-4 h-4" style={{ color: '#64748b' }} />
                        <select
                            value={language}
                            onChange={(e) => { setLanguage(e.target.value); i18n.changeLanguage(e.target.value); }}
                            className="select-dark text-xs py-0 border-none bg-transparent"
                            style={{ background: 'transparent', border: 'none', padding: '0' }}
                        >
                            {languages.map((l) => (
                                <option key={l.code} value={l.code}>{l.name}</option>
                            ))}
                        </select>
                    </div>

                    {/* Clear */}
                    <button
                        onClick={clearChat}
                        className="p-2 rounded-lg transition tooltip"
                        data-tip="Clear chat"
                        style={{ color: '#64748b', background: 'rgba(255,255,255,0.04)', border: '1px solid rgba(255,255,255,0.06)' }}
                        onMouseEnter={e => e.currentTarget.style.color = '#a5b4fc'}
                        onMouseLeave={e => e.currentTarget.style.color = '#64748b'}
                    >
                        <TrashIcon className="w-4 h-4" />
                    </button>
                </div>
            </div>

            {/* ── Messages ── */}
            <div className="flex-1 overflow-y-auto px-4 py-6"
                style={{ background: 'linear-gradient(180deg,#020817 0%,#0a0f1e 100%)' }}>
                <div className="max-w-3xl mx-auto space-y-5">

                    {/* Empty State */}
                    {messages.length === 0 && (
                        <motion.div
                            initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.6 }}
                            className="text-center py-10"
                        >
                            <div className="w-20 h-20 rounded-2xl flex items-center justify-center mx-auto mb-6 animate-float"
                                style={{ background: 'linear-gradient(135deg,rgba(99,102,241,0.2),rgba(79,70,229,0.1))', border: '1px solid rgba(99,102,241,0.2)' }}>
                                <SparklesIcon className="w-10 h-10" style={{ color: '#6366f1' }} />
                            </div>
                            <h2 className="text-2xl font-black mb-2" style={{ color: '#f1f5f9' }}>{t('chatbot.welcome')}</h2>
                            <p className="text-sm mb-8 max-w-sm mx-auto" style={{ color: '#64748b', lineHeight: 1.8 }}>
                                {t('chatbot.description')}
                            </p>

                            {/* Suggested Questions */}
                            <div className="text-left max-w-lg mx-auto">
                                <p className="text-xs font-semibold uppercase tracking-widest mb-3" style={{ color: '#334155' }}>
                                    Try asking:
                                </p>
                                <div className="space-y-2">
                                    {suggestedQuestions.map((q, i) => (
                                        <motion.button
                                            key={i}
                                            initial={{ opacity: 0, x: -10 }}
                                            animate={{ opacity: 1, x: 0 }}
                                            transition={{ delay: i * 0.08 }}
                                            onClick={() => sendMessage(q)}
                                            className="w-full text-left px-4 py-3 rounded-xl text-sm transition-all duration-200 group"
                                            style={{
                                                background: 'rgba(99,102,241,0.06)',
                                                border: '1px solid rgba(99,102,241,0.1)',
                                                color: '#94a3b8',
                                            }}
                                            onMouseEnter={e => {
                                                e.currentTarget.style.background = 'rgba(99,102,241,0.12)';
                                                e.currentTarget.style.borderColor = 'rgba(99,102,241,0.25)';
                                                e.currentTarget.style.color = '#c7d2fe';
                                            }}
                                            onMouseLeave={e => {
                                                e.currentTarget.style.background = 'rgba(99,102,241,0.06)';
                                                e.currentTarget.style.borderColor = 'rgba(99,102,241,0.1)';
                                                e.currentTarget.style.color = '#94a3b8';
                                            }}
                                        >
                                            <span className="mr-2" style={{ color: '#4f46e5' }}>→</span>
                                            {q}
                                        </motion.button>
                                    ))}
                                </div>
                            </div>
                        </motion.div>
                    )}

                    {/* Messages */}
                    <AnimatePresence>
                        {messages.map((msg, i) => (
                            <motion.div
                                key={i}
                                initial={{ opacity: 0, y: 12 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ duration: 0.35 }}
                                className={`flex gap-3 ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                            >
                                {/* AI Avatar */}
                                {msg.role === 'assistant' && (
                                    <div className="w-8 h-8 rounded-lg flex-shrink-0 flex items-center justify-center mt-0.5"
                                        style={{ background: 'linear-gradient(135deg,#6366f1,#4f46e5)' }}>
                                        <SparklesIcon className="w-4 h-4 text-white" />
                                    </div>
                                )}

                                <div className={msg.role === 'user' ? 'bubble-user' : 'bubble-ai'}>
                                    <div className="text-sm leading-relaxed markdown-content">
                                        <ReactMarkdown remarkPlugins={[remarkGfm]}>
                                            {msg.content}
                                        </ReactMarkdown>
                                    </div>

                                    {/* IPC Sections */}
                                    {msg.crimeCategory && (
                                        <div className="mt-3 pt-3" style={{ borderTop: '1px solid rgba(255,255,255,0.08)' }}>
                                            <div className="flex flex-wrap gap-2">
                                                <span className="badge badge-gold text-xs">
                                                    ⚖ {msg.crimeCategory}
                                                </span>
                                                {msg.ipcSections?.map((s, j) => (
                                                    <span key={j} className="badge badge-indigo text-xs">{s}</span>
                                                ))}
                                            </div>
                                        </div>
                                    )}

                                    {/* Specialized Widgets */}
                                    {msg.crimeCategory && (
                                        <div className="mt-4">
                                            <SpecializedWidget msg={msg} />
                                        </div>
                                    )}
                                </div>

                                {/* User Avatar */}
                                {msg.role === 'user' && (
                                    <div className="w-8 h-8 rounded-lg flex-shrink-0 flex items-center justify-center mt-0.5"
                                        style={{ background: 'rgba(255,255,255,0.06)', border: '1px solid rgba(255,255,255,0.08)' }}>
                                        <UserCircleIcon className="w-4 h-4" style={{ color: '#64748b' }} />
                                    </div>
                                )}
                            </motion.div>
                        ))}
                    </AnimatePresence>

                    {/* Typing Indicator */}
                    {loading && (
                        <motion.div
                            initial={{ opacity: 0 }} animate={{ opacity: 1 }}
                            className="flex gap-3 justify-start"
                        >
                            <div className="w-8 h-8 rounded-lg flex-shrink-0 flex items-center justify-center"
                                style={{ background: 'linear-gradient(135deg,#6366f1,#4f46e5)' }}>
                                <SparklesIcon className="w-4 h-4 text-white" />
                            </div>
                            <div className="bubble-ai flex items-center gap-1.5">
                                <div className="typing-dot" />
                                <div className="typing-dot" />
                                <div className="typing-dot" />
                                <span className="text-xs ml-1" style={{ color: '#64748b' }}>Analyzing your query...</span>
                            </div>
                        </motion.div>
                    )}

                    <div ref={messagesEndRef} />
                </div>
            </div>

            {/* ── Input Bar ── */}
            <div className="flex-shrink-0 px-4 py-4"
                style={{ background: 'rgba(2,8,23,0.95)', borderTop: '1px solid rgba(255,255,255,0.06)' }}>
                <div className="max-w-3xl mx-auto">
                    <form onSubmit={handleSubmit} className="flex gap-3 items-end">
                        <div className="flex-1 relative">
                            <textarea
                                ref={inputRef}
                                value={input}
                                onChange={(e) => setInput(e.target.value)}
                                onKeyDown={(e) => {
                                    if (e.key === 'Enter' && !e.shiftKey) {
                                        e.preventDefault();
                                        handleSubmit(e);
                                    }
                                }}
                                placeholder={t('chatbot.placeholder')}
                                disabled={loading}
                                rows={1}
                                className="input-dark resize-none py-3.5 pr-12"
                                style={{ minHeight: '52px', maxHeight: '140px', lineHeight: '1.5' }}
                                onInput={(e) => {
                                    e.target.style.height = 'auto';
                                    e.target.style.height = Math.min(e.target.scrollHeight, 140) + 'px';
                                }}
                            />
                        </div>

                        <button
                            type="submit"
                            disabled={loading || !input.trim()}
                            className="flex-shrink-0 w-12 h-12 rounded-xl flex items-center justify-center transition-all duration-200"
                            style={{
                                background: loading || !input.trim()
                                    ? 'rgba(255,255,255,0.05)'
                                    : 'linear-gradient(135deg,#6366f1,#4f46e5)',
                                border: '1px solid rgba(255,255,255,0.06)',
                                boxShadow: !loading && input.trim() ? '0 4px 15px rgba(99,102,241,0.35)' : 'none',
                            }}
                        >
                            <PaperAirplaneIcon className="w-5 h-5"
                                style={{ color: loading || !input.trim() ? '#334155' : 'white' }} />
                        </button>
                    </form>

                    <div className="flex items-center justify-between mt-2 px-1">
                        <p className="text-xs" style={{ color: '#1e293b' }}>
                            <ShieldCheckIcon className="w-3 h-3 inline mr-1" />
                            {t('chatbot.disclaimer')}
                        </p>
                        <p className="text-xs" style={{ color: '#1e293b' }}>Enter to send · Shift+Enter for new line</p>
                    </div>
                </div>
            </div>
        </div>
    );
}
