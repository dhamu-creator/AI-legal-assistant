import React, { useState, createContext, useContext, useEffect } from 'react';
import { useAuth } from './AuthContext';

const ChatContext = createContext();

export function ChatProvider({ children }) {
    const { user } = useAuth();
    const [userId, setUserId] = useState(() => {
        try {
            const raw = localStorage.getItem('user');
            const u = raw ? JSON.parse(raw) : null;
            return u?.id || '000000000000000000000000';
        } catch {
            return '000000000000000000000000';
        }
    });
    const [language, setLanguage] = useState('en');
    const [sessions, setSessions] = useState([]);
    const [currentSession, setCurrentSession] = useState(null);

    useEffect(() => {
        if (user?.id) setUserId(user.id);
        else setUserId('000000000000000000000000');
    }, [user]);

    const createSession = (title) => {
        const newSession = {
            id: Date.now(),
            title,
            messages: [],
            createdAt: new Date(),
        };
        setSessions([newSession, ...sessions]);
        setCurrentSession(newSession);
        return newSession;
    };

    const addMessage = (sessionId, message) => {
        setSessions(
            sessions.map((session) =>
                session.id === sessionId
                    ? { ...session, messages: [...session.messages, message] }
                    : session
            )
        );
    };

    const value = {
        userId,
        setUserId,
        language,
        setLanguage,
        sessions,
        currentSession,
        createSession,
        addMessage,
    };

    return <ChatContext.Provider value={value}>{children}</ChatContext.Provider>;
}

export function useChat() {
    const context = useContext(ChatContext);
    if (!context) {
        throw new Error('useChat must be used within ChatProvider');
    }
    return context;
}
