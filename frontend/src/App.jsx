import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import './i18n/config';

// Pages
import Home from './pages/Home';
import Chatbot from './pages/Chatbot';
import FIRGenerator from './pages/FIRGenerator';
import EmergencyHelp from './pages/EmergencyHelp';
import MyFIRs from './pages/MyFIRs';
import AdminDashboard from './pages/AdminDashboard';
import Auth from './pages/Auth';

// Contexts
import { ChatProvider } from './context/ChatContext';
import { AuthProvider } from './context/AuthContext';
import { useAuth } from './context/AuthContext';

// Icons
import {
    HomeIcon,
    ChatBubbleLeftEllipsisIcon,
    DocumentTextIcon,
    FolderOpenIcon,
    ExclamationTriangleIcon,
    Cog6ToothIcon,
    UserCircleIcon,
    Bars3Icon,
    XMarkIcon,
    LanguageIcon,
} from '@heroicons/react/24/outline';

function NavLink({ to, children, icon: Icon, className = '' }) {
    const location = useLocation();
    const isActive = location.pathname === to;
    return (
        <Link
            to={to}
            className={`nav-link flex items-center gap-1.5 ${isActive ? 'nav-link-active' : ''} ${className}`}
        >
            {Icon && <Icon className="w-4 h-4" />}
            {children}
        </Link>
    );
}

function Navbar() {
    const { t, i18n } = useTranslation();
    const { user } = useAuth();
    const [scrolled, setScrolled] = useState(false);
    const [mobileOpen, setMobileOpen] = useState(false);

    useEffect(() => {
        const onScroll = () => setScrolled(window.scrollY > 20);
        window.addEventListener('scroll', onScroll);
        return () => window.removeEventListener('scroll', onScroll);
    }, []);

    const navItems = [
        { to: '/', label: t('nav.home'), icon: HomeIcon },
        { to: '/chatbot', label: t('nav.chatbot'), icon: ChatBubbleLeftEllipsisIcon },
        { to: '/fir-generator', label: t('nav.firGenerator'), icon: DocumentTextIcon },
        { to: '/my-firs', label: t('nav.myFirs'), icon: FolderOpenIcon },
        { to: '/emergency', label: t('nav.emergencyHelp'), icon: ExclamationTriangleIcon, className: 'nav-emergency' },
    ];

    // Show Admin link for admin users OR always include it (accessible via URL)
    if (user?.role === 'admin' || user?.role === 'Admin') {
        navItems.push({ to: '/admin', label: t('nav.admin'), icon: Cog6ToothIcon });
    }

    return (
        <nav className="navbar" style={{ transition: 'box-shadow 0.3s', boxShadow: scrolled ? '0 8px 32px rgba(0,0,0,0.4)' : 'none' }}>
            <div className="max-w-7xl mx-auto px-4 sm:px-6">
                <div className="flex items-center justify-between h-16">
                    {/* Logo */}
                    <Link to="/" className="flex items-center gap-2.5 group">
                        <div className="w-8 h-8 rounded-lg flex items-center justify-center" style={{ background: 'linear-gradient(135deg, #6366f1, #4f46e5)' }}>
                            <span className="text-white font-black text-sm">⚖</span>
                        </div>
                        <div>
                            <span className="text-white font-black text-lg tracking-tight">Lex</span>
                            <span className="font-black text-lg tracking-tight" style={{ color: '#f59e0b' }}>AI</span>
                        </div>
                        <span className="badge badge-indigo hidden sm:inline-flex" style={{ fontSize: '0.6rem' }}>BETA</span>
                    </Link>

                    {/* Desktop Nav */}
                    <div className="hidden lg:flex items-center gap-1">
                        {navItems.map((item) => (
                            <NavLink key={item.to} to={item.to} icon={item.icon} className={item.className || ''}>
                                {item.label}
                            </NavLink>
                        ))}
                    </div>

                    {/* Right Side */}
                    <div className="hidden lg:flex items-center gap-3">
                        {/* Language Selector */}
                        <div className="flex items-center gap-1.5">
                            <LanguageIcon className="w-4 h-4" style={{ color: '#64748b' }} />
                            <select
                                value={i18n.language}
                                onChange={(e) => i18n.changeLanguage(e.target.value)}
                                className="select-dark"
                            >
                                <option value="en">English</option>
                                <option value="ta">தமிழ் (Tamil)</option>
                                <option value="hi">हिंदी (Hindi)</option>
                                <option value="te">తెలుగు (Telugu)</option>
                                <option value="ml">മലയാളം (Malayalam)</option>
                                <option value="ka">ಕನ್ನಡ (Kannada)</option>
                            </select>
                        </div>

                        {/* Auth Buttons */}
                        {user ? (
                            <div className="flex items-center gap-2">
                                {user.role === 'admin' && (
                                    <Link to="/admin" className="flex items-center gap-1 px-3 py-1.5 rounded-lg text-xs font-bold transition"
                                        style={{ background: 'rgba(217,119,6,0.15)', color: '#fbbf24', border: '1px solid rgba(217,119,6,0.25)' }}>
                                        <Cog6ToothIcon className="w-3.5 h-3.5" />
                                        Admin
                                    </Link>
                                )}
                                <Link to="/auth" className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg font-semibold text-sm transition-all duration-200"
                                    style={{ background: 'rgba(99,102,241,0.15)', color: '#a5b4fc', border: '1px solid rgba(99,102,241,0.2)' }}>
                                    <UserCircleIcon className="w-4 h-4" />
                                    {user.name?.split(' ')[0]}
                                </Link>
                            </div>
                        ) : (
                            <Link to="/auth" className="flex items-center gap-1.5 px-4 py-1.5 rounded-lg font-semibold text-sm transition-all duration-200"
                                style={{ background: 'linear-gradient(135deg, #6366f1, #4f46e5)', color: 'white' }}>
                                <UserCircleIcon className="w-4 h-4" />
                                {t('nav.login')}
                            </Link>
                        )}
                    </div>

                    {/* Mobile toggle */}
                    <button
                        className="lg:hidden p-2 rounded-lg text-slate-400 hover:text-white hover:bg-white/5 transition"
                        onClick={() => setMobileOpen(!mobileOpen)}
                    >
                        {mobileOpen ? <XMarkIcon className="w-5 h-5" /> : <Bars3Icon className="w-5 h-5" />}
                    </button>
                </div>
            </div>

            {/* Mobile Menu */}
            {mobileOpen && (
                <div className="lg:hidden border-t" style={{ borderColor: 'rgba(255,255,255,0.06)', background: 'rgba(2,8,23,0.95)' }}>
                    <div className="px-4 py-3 space-y-1">
                        {navItems.map((item) => (
                            <Link
                                key={item.to}
                                to={item.to}
                                onClick={() => setMobileOpen(false)}
                                className={`flex items-center gap-2.5 px-3 py-2.5 rounded-lg text-sm font-medium transition ${item.className || 'text-slate-300 hover:text-white hover:bg-white/5'}`}
                            >
                                {item.icon && <item.icon className="w-4 h-4" />}
                                {item.label}
                            </Link>
                        ))}
                        <div className="pt-2 border-t" style={{ borderColor: 'rgba(255,255,255,0.06)' }}>
                            <div className="flex items-center gap-2 px-3 py-2">
                                <LanguageIcon className="w-4 h-4 text-slate-500" />
                                <select
                                    value={i18n.language}
                                    onChange={(e) => i18n.changeLanguage(e.target.value)}
                                    className="select-dark flex-1"
                                >
                                    <option value="en">English</option>
                                    <option value="ta">தமிழ் (Tamil)</option>
                                    <option value="hi">हिंदी (Hindi)</option>
                                    <option value="te">తెలుగు (Telugu)</option>
                                    <option value="ml">മലയാളം (Malayalam)</option>
                                    <option value="ka">ಕನ್ನಡ (Kannada)</option>
                                </select>
                            </div>
                            <Link
                                to="/auth"
                                onClick={() => setMobileOpen(false)}
                                className="flex items-center gap-2 px-3 py-2.5 rounded-lg text-sm font-semibold mt-1"
                                style={{ background: 'rgba(99,102,241,0.15)', color: '#a5b4fc' }}
                            >
                                <UserCircleIcon className="w-4 h-4" />
                                {user ? user.name?.split(' ')[0] : t('nav.login')}
                            </Link>
                        </div>
                    </div>
                </div>
            )}
        </nav>
    );
}

function Footer() {
    return (
        <footer className="footer mt-20">
            <div className="max-w-7xl mx-auto px-6 py-12">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-10 mb-10">
                    {/* Brand */}
                    <div>
                        <div className="flex items-center gap-2 mb-4">
                            <div className="w-8 h-8 rounded-lg flex items-center justify-center" style={{ background: 'linear-gradient(135deg, #6366f1, #4f46e5)' }}>
                                <span className="text-white font-black text-sm">⚖</span>
                            </div>
                            <span className="text-white font-black text-xl">Lex<span style={{ color: '#f59e0b' }}>AI</span></span>
                        </div>
                        <p className="text-sm" style={{ color: '#64748b', lineHeight: '1.7' }}>
                            Empowering Indian citizens with AI-driven legal knowledge, FIR generation, and rights awareness.
                        </p>
                    </div>

                    {/* Quick Links */}
                    <div>
                        <h4 className="text-sm font-semibold uppercase tracking-widest mb-4" style={{ color: '#475569' }}>Quick Links</h4>
                        <div className="space-y-2">
                            {[
                                { to: '/chatbot', label: 'AI Legal Chatbot' },
                                { to: '/fir-generator', label: 'FIR Generator' },
                                { to: '/my-firs', label: 'My FIRs' },
                                { to: '/emergency', label: 'Emergency Help' },
                            ].map((link) => (
                                <Link key={link.to} to={link.to} className="block text-sm transition" style={{ color: '#64748b' }}
                                    onMouseEnter={(e) => e.target.style.color = '#a5b4fc'}
                                    onMouseLeave={(e) => e.target.style.color = '#64748b'}>
                                    → {link.label}
                                </Link>
                            ))}
                        </div>
                    </div>

                    {/* Legal */}
                    <div>
                        <h4 className="text-sm font-semibold uppercase tracking-widest mb-4" style={{ color: '#475569' }}>Legal Notice</h4>
                        <p className="text-xs" style={{ color: '#475569', lineHeight: '1.8' }}>
                            LexAI provides legal information only. This platform is <strong style={{ color: '#64748b' }}>not a substitute</strong> for licensed legal counsel. Always consult a qualified advocate for legal action.
                        </p>
                        <div className="flex gap-2 mt-4">
                            <span className="badge badge-indigo">IPC</span>
                            <span className="badge badge-gold">CrPC</span>
                            <span className="badge badge-green">BNS 2023</span>
                        </div>
                    </div>
                </div>

                <hr className="divider-gold mb-6" />

                <div className="flex flex-col sm:flex-row items-center justify-between gap-3">
                    <p className="text-xs" style={{ color: '#334155' }}>
                        © 2024 LexAI — AI Legal Assistant. All rights reserved.
                    </p>
                    <p className="text-xs" style={{ color: '#334155' }}>
                        Powered by Groq AI · Made for Indian Citizens
                    </p>
                </div>
            </div>
        </footer>
    );
}

function AppContent() {
    return (
        <Router>
            <div className="flex flex-col min-h-screen" style={{ background: '#020817' }}>
                <Navbar />
                <main className="flex-1">
                    <Routes>
                        <Route path="/" element={<Home />} />
                        <Route path="/chatbot" element={<Chatbot />} />
                        <Route path="/fir-generator" element={<FIRGenerator />} />
                        <Route path="/my-firs" element={<MyFIRs />} />
                        <Route path="/auth" element={<Auth />} />
                        <Route path="/emergency" element={<EmergencyHelp />} />
                        <Route path="/admin" element={<AdminDashboard />} />
                    </Routes>
                </main>
                <Footer />
            </div>
        </Router>
    );
}

export default function App() {
    return (
        <AuthProvider>
            <ChatProvider>
                <AppContent />
            </ChatProvider>
        </AuthProvider>
    );
}
