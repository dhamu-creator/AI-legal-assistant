import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import {
    EnvelopeIcon,
    LockClosedIcon,
    UserIcon,
    ShieldCheckIcon,
    SparklesIcon,
    ArrowRightOnRectangleIcon,
    UserPlusIcon,
    EyeIcon,
    EyeSlashIcon,
} from '@heroicons/react/24/outline';

const fadeUp = {
    hidden: { opacity: 0, y: 24 },
    visible: { opacity: 1, y: 0, transition: { duration: 0.5, ease: [0.22, 1, 0.36, 1] } },
};

export default function Auth() {
    const { login, register, logout, user } = useAuth();
    const navigate = useNavigate();
    const [mode, setMode] = useState('login');
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [role, setRole] = useState('user');
    const [showPass, setShowPass] = useState(false);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setSuccess('');
        setLoading(true);
        try {
            if (mode === 'login') {
                await login(email, password);
                setSuccess('Welcome back! You are now logged in.');
                setTimeout(() => navigate('/'), 1200);
            } else {
                await register(name, email, password, role);
                setSuccess('Account created successfully! Welcome to LexAI.');
                setTimeout(() => navigate('/'), 1200);
            }
        } catch (err) {
            setError(err?.response?.data?.message || 'Something went wrong. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    /* ─── If already logged in ─── */
    if (user) {
        return (
            <div className="page-bg flex items-center justify-center px-4 py-20">
                <motion.div
                    initial="hidden" animate="visible" variants={fadeUp}
                    className="glass-card rounded-3xl p-10 text-center max-w-md w-full"
                >
                    <div className="w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-5"
                        style={{ background: 'linear-gradient(135deg,#6366f1,#4f46e5)' }}>
                        <UserIcon className="w-8 h-8 text-white" />
                    </div>
                    <h2 className="text-2xl font-black mb-1" style={{ color: '#f1f5f9' }}>
                        Welcome, {user.name}
                    </h2>
                    <p className="text-sm mb-2" style={{ color: '#64748b' }}>{user.email}</p>
                    <span className={`badge mb-6 ${user.role === 'admin' ? 'badge-gold' : 'badge-indigo'}`}>
                        {user.role === 'admin' ? '⭐ Admin' : '👤 User'}
                    </span>

                    <div className="space-y-3">
                        <button
                            onClick={() => navigate('/chatbot')}
                            className="btn-primary w-full justify-center py-3"
                        >
                            <span className="flex items-center gap-2 relative z-10">
                                <SparklesIcon className="w-5 h-5" />
                                Open Legal Chatbot
                            </span>
                        </button>
                        <button
                            onClick={() => { logout(); setSuccess('Logged out successfully.'); }}
                            className="btn-outline w-full justify-center py-3"
                            style={{ borderColor: 'rgba(239,68,68,0.3)', color: '#fca5a5' }}
                        >
                            <ArrowRightOnRectangleIcon className="w-5 h-5" />
                            Sign Out
                        </button>
                    </div>
                </motion.div>
            </div>
        );
    }

    return (
        <div className="page-bg flex items-center justify-center px-4 py-16">
            <div className="w-full max-w-5xl grid grid-cols-1 lg:grid-cols-2 gap-8 items-center">

                {/* ── Left Panel (Branding) ── */}
                <motion.div
                    initial={{ opacity: 0, x: -40 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ duration: 0.7, ease: [0.22, 1, 0.36, 1] }}
                    className="hidden lg:block"
                >
                    <div className="relative">
                        <div className="orb orb-indigo" style={{ width: 350, height: 350, top: -80, left: -80, opacity: 0.4 }} />
                        <div className="orb orb-gold" style={{ width: 200, height: 200, bottom: -50, right: 0, opacity: 0.3 }} />

                        <div className="relative z-10">
                            <div className="flex items-center gap-2.5 mb-8">
                                <div className="w-10 h-10 rounded-xl flex items-center justify-center"
                                    style={{ background: 'linear-gradient(135deg,#6366f1,#4f46e5)' }}>
                                    <span className="text-white font-black">⚖</span>
                                </div>
                                <span className="text-white font-black text-2xl">
                                    Lex<span style={{ color: '#f59e0b' }}>AI</span>
                                </span>
                            </div>

                            <h1 className="text-4xl font-black mb-5" style={{ color: '#f1f5f9', lineHeight: 1.2, letterSpacing: '-0.02em' }}>
                                Your AI-Powered<br />
                                <span className="gradient-text">Legal Partner</span>
                            </h1>
                            <p className="text-base mb-8" style={{ color: '#64748b', lineHeight: 1.8 }}>
                                Join thousands of Indian citizens who use LexAI to understand their rights, generate FIRs, and get instant legal guidance.
                            </p>

                            <div className="space-y-4">
                                {[
                                    { icon: '⚡', text: 'Instant AI legal analysis in 6 languages' },
                                    { icon: '📄', text: 'Professional FIR documents, auto-generated' },
                                    { icon: '🔒', text: '100% private — your data stays secure' },
                                    { icon: '⚖️', text: 'Covers IPC, BNS 2023, CrPC, IT Act & more' },
                                ].map((item, i) => (
                                    <div key={i} className="flex items-center gap-3">
                                        <span className="text-xl">{item.icon}</span>
                                        <span className="text-sm" style={{ color: '#94a3b8' }}>{item.text}</span>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>
                </motion.div>

                {/* ── Right Panel (Form) ── */}
                <motion.div
                    initial="hidden" animate="visible" variants={fadeUp}
                    className="glass-card rounded-3xl p-8 sm:p-10 w-full"
                >
                    {/* Toggle Tabs */}
                    <div className="flex rounded-xl p-1 mb-8"
                        style={{ background: 'rgba(255,255,255,0.04)', border: '1px solid rgba(255,255,255,0.06)' }}>
                        {['login', 'register'].map((m) => (
                            <button
                                key={m}
                                onClick={() => { setMode(m); setError(''); setSuccess(''); }}
                                className="flex-1 py-2.5 rounded-lg text-sm font-semibold transition-all duration-300"
                                style={{
                                    background: mode === m ? 'linear-gradient(135deg,#6366f1,#4f46e5)' : 'transparent',
                                    color: mode === m ? 'white' : '#64748b',
                                    boxShadow: mode === m ? '0 4px 15px rgba(99,102,241,0.3)' : 'none',
                                }}
                            >
                                {m === 'login' ? (
                                    <span className="flex items-center justify-center gap-1.5">
                                        <ArrowRightOnRectangleIcon className="w-4 h-4" />
                                        Sign In
                                    </span>
                                ) : (
                                    <span className="flex items-center justify-center gap-1.5">
                                        <UserPlusIcon className="w-4 h-4" />
                                        Register
                                    </span>
                                )}
                            </button>
                        ))}
                    </div>

                    <h2 className="text-2xl font-black mb-1" style={{ color: '#f1f5f9' }}>
                        {mode === 'login' ? 'Welcome back' : 'Create account'}
                    </h2>
                    <p className="text-sm mb-7" style={{ color: '#64748b' }}>
                        {mode === 'login'
                            ? 'Sign in to access your legal dashboard'
                            : 'Join LexAI and get free legal guidance'}
                    </p>

                    {/* Alerts */}
                    <AnimatePresence>
                        {error && (
                            <motion.div
                                initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }}
                                className="rounded-xl px-4 py-3 mb-5 text-sm"
                                style={{ background: 'rgba(239,68,68,0.1)', border: '1px solid rgba(239,68,68,0.2)', color: '#fca5a5' }}
                            >
                                ⚠ {error}
                            </motion.div>
                        )}
                        {success && (
                            <motion.div
                                initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }}
                                className="rounded-xl px-4 py-3 mb-5 text-sm"
                                style={{ background: 'rgba(34,197,94,0.1)', border: '1px solid rgba(34,197,94,0.2)', color: '#86efac' }}
                            >
                                ✓ {success}
                            </motion.div>
                        )}
                    </AnimatePresence>

                    <form onSubmit={handleSubmit} className="space-y-4">
                        <AnimatePresence>
                            {mode === 'register' && (
                                <motion.div
                                    initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: 'auto' }} exit={{ opacity: 0, height: 0 }}
                                >
                                    <label className="label-dark">Full Name</label>
                                    <div className="relative">
                                        <UserIcon className="w-4 h-4 absolute left-3.5 top-1/2 -translate-y-1/2" style={{ color: '#64748b' }} />
                                        <input
                                            value={name}
                                            onChange={(e) => setName(e.target.value)}
                                            placeholder="Rajesh Kumar"
                                            required
                                            className="input-dark pl-10"
                                        />
                                    </div>
                                </motion.div>
                            )}
                        </AnimatePresence>

                        <div>
                            <label className="label-dark">Email Address</label>
                            <div className="relative">
                                <EnvelopeIcon className="w-4 h-4 absolute left-3.5 top-1/2 -translate-y-1/2" style={{ color: '#64748b' }} />
                                <input
                                    type="email"
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                    placeholder="you@example.com"
                                    required
                                    className="input-dark pl-10"
                                />
                            </div>
                        </div>

                        <div>
                            <label className="label-dark">Password</label>
                            <div className="relative">
                                <LockClosedIcon className="w-4 h-4 absolute left-3.5 top-1/2 -translate-y-1/2" style={{ color: '#64748b' }} />
                                <input
                                    type={showPass ? 'text' : 'password'}
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                    placeholder="••••••••"
                                    required
                                    className="input-dark pl-10 pr-10"
                                />
                                <button
                                    type="button"
                                    onClick={() => setShowPass(!showPass)}
                                    className="absolute right-3.5 top-1/2 -translate-y-1/2 transition"
                                    style={{ color: '#64748b' }}
                                >
                                    {showPass ? <EyeSlashIcon className="w-4 h-4" /> : <EyeIcon className="w-4 h-4" />}
                                </button>
                            </div>
                        </div>

                        <AnimatePresence>
                            {mode === 'register' && (
                                <motion.div
                                    initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: 'auto' }} exit={{ opacity: 0, height: 0 }}
                                >
                                    <label className="label-dark">Account Type</label>
                                    <div className="grid grid-cols-2 gap-3">
                                        {[{ value: 'user', label: '👤 User', desc: 'Legal guidance' }, { value: 'admin', label: '⭐ Admin', desc: 'Full access' }].map((r) => (
                                            <button
                                                key={r.value}
                                                type="button"
                                                onClick={() => setRole(r.value)}
                                                className="p-3 rounded-xl text-left transition-all duration-200"
                                                style={{
                                                    background: role === r.value ? 'rgba(99,102,241,0.15)' : 'rgba(255,255,255,0.03)',
                                                    border: `1px solid ${role === r.value ? 'rgba(99,102,241,0.4)' : 'rgba(255,255,255,0.08)'}`,
                                                    color: role === r.value ? '#a5b4fc' : '#64748b',
                                                }}
                                            >
                                                <div className="font-semibold text-sm">{r.label}</div>
                                                <div className="text-xs mt-0.5" style={{ opacity: 0.7 }}>{r.desc}</div>
                                            </button>
                                        ))}
                                    </div>
                                </motion.div>
                            )}
                        </AnimatePresence>

                        <button
                            type="submit"
                            disabled={loading}
                            className="btn-primary w-full justify-center py-3.5 mt-2 text-base"
                            style={{ opacity: loading ? 0.7 : 1 }}
                        >
                            <span className="flex items-center gap-2 relative z-10">
                                {loading ? (
                                    <>
                                        <svg className="animate-spin w-5 h-5" fill="none" viewBox="0 0 24 24">
                                            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                                            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                                        </svg>
                                        Processing...
                                    </>
                                ) : mode === 'login' ? (
                                    <><ArrowRightOnRectangleIcon className="w-5 h-5" /> Sign In</>
                                ) : (
                                    <><UserPlusIcon className="w-5 h-5" /> Create Account</>
                                )}
                            </span>
                        </button>
                    </form>

                    <div className="mt-6 flex items-center gap-3">
                        <div className="flex-1 h-px" style={{ background: 'rgba(255,255,255,0.06)' }} />
                        <ShieldCheckIcon className="w-4 h-4" style={{ color: '#334155' }} />
                        <div className="flex-1 h-px" style={{ background: 'rgba(255,255,255,0.06)' }} />
                    </div>
                    <p className="text-center text-xs mt-4" style={{ color: '#334155' }}>
                        Your data is encrypted and never shared with third parties
                    </p>
                </motion.div>
            </div>
        </div>
    );
}
