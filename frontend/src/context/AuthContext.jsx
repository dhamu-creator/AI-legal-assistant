import React, { createContext, useContext, useState, useEffect } from 'react';
import { apiClient } from '../services/api';

const AuthContext = createContext();

export function AuthProvider({ children }) {
    const [token, setToken] = useState(() => localStorage.getItem('token') || null);
    const [user, setUser] = useState(() => {
        try {
            const raw = localStorage.getItem('user');
            return raw ? JSON.parse(raw) : null;
        } catch (e) {
            return null;
        }
    });

    // Keep localStorage in sync with state
    useEffect(() => {
        if (token) {
            localStorage.setItem('token', token);
        } else {
            localStorage.removeItem('token');
        }
    }, [token]);

    useEffect(() => {
        if (user) {
            localStorage.setItem('user', JSON.stringify(user));
        } else {
            localStorage.removeItem('user');
        }
    }, [user]);

    const login = async (email, password) => {
        const res = await apiClient.post('/auth/login', { email, password });
        if (res.data?.success) {
            const { token: newToken, user: newUser } = res.data.data;
            setToken(newToken);
            setUser({ id: newUser.id, name: newUser.name, email: newUser.email, role: newUser.role });
        }
        return res.data;
    };

    const register = async (name, email, password, role = 'user') => {
        const res = await apiClient.post('/auth/register', { name, email, password, role });
        if (res.data?.success) {
            const { token: newToken, user: newUser } = res.data.data;
            setToken(newToken);
            setUser({ id: newUser.id, name: newUser.name, email: newUser.email, role: newUser.role || role });
        }
        return res.data;
    };

    const logout = () => {
        setToken(null);
        setUser(null);
    };

    return (
        <AuthContext.Provider value={{ token, user, login, register, logout, setUser, setToken }}>
            {children}
        </AuthContext.Provider>
    );
}

export function useAuth() {
    const ctx = useContext(AuthContext);
    if (!ctx) throw new Error('useAuth must be used within AuthProvider');
    return ctx;
}

export default AuthContext;
