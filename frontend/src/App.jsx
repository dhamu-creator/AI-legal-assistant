import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import './i18n/config';

// Pages
import Home from './pages/Home';
import Chatbot from './pages/Chatbot';
import FIRGenerator from './pages/FIRGenerator';
import EmergencyHelp from './pages/EmergencyHelp';
import MyFIRs from './pages/MyFIRs';

// Components
import { ChatProvider } from './context/ChatContext';
import { AuthProvider } from './context/AuthContext';
import Auth from './pages/Auth';

export default function App() {
    const { i18n } = useTranslation();

    const changeLanguage = (lang) => {
        i18n.changeLanguage(lang);
    };

    return (
        <AuthProvider>
            <ChatProvider>
                <Router>
                {/* Navigation Bar */}
                <nav className="bg-indigo-700 text-white shadow-lg">
                    <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
                        <Link to="/" className="text-2xl font-bold">
                            ⚖️ Legal AI
                        </Link>

                        <div className="flex items-center gap-6">
                            <Link to="/" className="hover:text-indigo-200 transition">
                                Home
                            </Link>
                            <Link to="/chatbot" className="hover:text-indigo-200 transition">
                                Chatbot
                            </Link>
                            <Link to="/fir-generator" className="hover:text-indigo-200 transition">
                                FIR Generator
                            </Link>
                            <Link to="/my-firs" className="hover:text-indigo-200 transition">
                                My FIRs
                            </Link>
                            <Link to="/emergency" className="hover:text-indigo-200 transition">
                                Emergency Help
                            </Link>
                            <Link to="/auth" className="hover:text-indigo-200 transition">
                                Login
                            </Link>

                            {/* Language Selector */}
                            <select
                                onChange={(e) => changeLanguage(e.target.value)}
                                className="bg-indigo-600 text-white px-3 py-1 rounded border border-indigo-500"
                            >
                                <option value="en">English</option>
                                <option value="ta">Tamil</option>
                                <option value="hi">Hindi</option>
                            </select>
                        </div>
                    </div>
                </nav>

                {/* Routes */}
                <Routes>
                    <Route path="/" element={<Home />} />
                    <Route path="/chatbot" element={<Chatbot />} />
                    <Route path="/fir-generator" element={<FIRGenerator />} />
                    <Route path="/my-firs" element={<MyFIRs />} />
                    <Route path="/auth" element={<Auth />} />
                    <Route path="/emergency" element={<EmergencyHelp />} />
                </Routes>

                {/* Footer */}
                <footer className="bg-gray-800 text-white py-8 mt-12">
                    <div className="max-w-7xl mx-auto px-4 text-center">
                        <p className="mb-2">⚖️ AI Legal Assistant</p>
                        <p className="text-sm text-gray-400 mb-4">
                            Providing legal guidance and support to Indian citizens
                        </p>
                        <p className="text-xs text-gray-500">
                            © 2024 AI Legal Assistant. This is an AI-powered platform for legal information only.
                            Always consult a lawyer for legal advice.
                        </p>
                    </div>
                </footer>
            </Router>
            </ChatProvider>
        </AuthProvider>
    );
}
