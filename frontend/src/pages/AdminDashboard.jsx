import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Activity, Users, FileText, MessageSquare, AlertCircle, Cpu, TrendingUp } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';

const fadeUp = {
    hidden: { opacity: 0, y: 24 },
    visible: (i = 0) => ({ opacity: 1, y: 0, transition: { duration: 0.5, delay: i * 0.1, ease: [0.22, 1, 0.36, 1] } }),
};

function StatCard({ icon: Icon, label, value, color, index }) {
    return (
        <motion.div
            variants={fadeUp} initial="hidden" animate="visible" custom={index}
            className="glass-card rounded-2xl p-6"
        >
            <div className="flex items-start justify-between mb-4">
                <div className="w-11 h-11 rounded-xl flex items-center justify-center"
                    style={{ background: `${color}18`, border: `1px solid ${color}25` }}>
                    <Icon className="w-5 h-5" style={{ color }} />
                </div>
                <TrendingUp className="w-4 h-4" style={{ color: '#22c55e' }} />
            </div>
            <p className="text-xs font-semibold uppercase tracking-wider mb-1" style={{ color: '#64748b' }}>{label}</p>
            <p className="text-3xl font-black" style={{ color: '#f1f5f9' }}>{value}</p>
        </motion.div>
    );
}

export default function AdminDashboard() {
    const { token, user } = useAuth();
    const navigate = useNavigate();
    const [analytics, setAnalytics] = useState(null);
    const [error, setError] = useState(null);
    const [connected, setConnected] = useState(false);

    useEffect(() => {
        if (!token) {
            setError('Authorization required. Please log in as an admin.');
            return;
        }
        const eventSource = new EventSource(`/api/admin/analytics/stream?token=${token}`);
        eventSource.onmessage = (event) => {
            try {
                setAnalytics(JSON.parse(event.data));
                setConnected(true);
                setError(null);
            } catch (err) {
                console.error('Parse error', err);
            }
        };
        eventSource.onerror = (err) => {
            console.error('SSE error', err);
            setConnected(false);
            setError('Failed to connect to the live analytics stream. Access denied or server error.');
            eventSource.close();
        };
        return () => eventSource.close();
    }, [token]);

    /* ── Error State ── */
    if (error) {
        return (
            <div className="page-bg flex items-center justify-center px-4 py-20">
                <motion.div
                    initial="hidden" animate="visible" variants={fadeUp}
                    className="glass-card rounded-2xl p-10 text-center max-w-md"
                >
                    <div className="w-14 h-14 rounded-2xl flex items-center justify-center mx-auto mb-5"
                        style={{ background: 'rgba(239,68,68,0.1)', border: '1px solid rgba(239,68,68,0.2)' }}>
                        <AlertCircle className="w-7 h-7" style={{ color: '#ef4444' }} />
                    </div>
                    <h2 className="text-xl font-black mb-3" style={{ color: '#f1f5f9' }}>Access Denied</h2>
                    <p className="text-sm mb-6" style={{ color: '#64748b' }}>{error}</p>
                    <button onClick={() => navigate('/auth')} className="btn-primary w-full justify-center py-3">
                        <span className="relative z-10">Sign In as Admin</span>
                    </button>
                </motion.div>
            </div>
        );
    }

    /* ── Loading State ── */
    if (!analytics) {
        return (
            <div className="page-bg flex items-center justify-center min-h-screen px-4">
                <div className="text-center">
                    <div className="w-16 h-16 rounded-2xl flex items-center justify-center mx-auto mb-6 animate-pulse-glow"
                        style={{ background: 'linear-gradient(135deg,#6366f1,#4f46e5)' }}>
                        <Cpu className="w-8 h-8 text-white animate-spin-slow" />
                    </div>
                    <p className="text-base font-semibold" style={{ color: '#94a3b8' }}>Connecting to live stream...</p>
                    <p className="text-sm mt-1" style={{ color: '#334155' }}>Establishing SSE connection</p>
                </div>
            </div>
        );
    }

    const totalFIRs = Object.values(analytics.crime_distribution || {}).reduce((a, b) => a + b, 0);
    const maxAction = Math.max(analytics.total_actions_24h || 1, 1);
    const maxCrime = Math.max(...Object.values(analytics.crime_distribution || { _: 1 }), 1);

    return (
        <div className="page-bg px-4 py-10">
            <div className="max-w-7xl mx-auto">

                {/* ── Header ── */}
                <motion.div
                    variants={fadeUp} initial="hidden" animate="visible"
                    className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-10"
                >
                    <div>
                        <span className="section-tag">
                            <Cpu className="w-3.5 h-3.5" />
                            Admin Control Panel
                        </span>
                        <h1 className="text-3xl font-black" style={{ color: '#f1f5f9', letterSpacing: '-0.02em' }}>
                            System Analytics
                        </h1>
                        <p className="text-sm mt-1" style={{ color: '#64748b' }}>
                            Real-time monitoring · Logged in as <strong style={{ color: '#a5b4fc' }}>{user?.name}</strong>
                        </p>
                    </div>

                    {/* Live indicator */}
                    <div className="flex items-center gap-2 px-4 py-2 rounded-full"
                        style={{
                            background: connected ? 'rgba(34,197,94,0.1)' : 'rgba(234,179,8,0.1)',
                            border: `1px solid ${connected ? 'rgba(34,197,94,0.2)' : 'rgba(234,179,8,0.2)'}`,
                        }}>
                        <div className={`w-2 h-2 rounded-full ${connected ? 'bg-green-400 animate-pulse' : 'bg-yellow-400'}`} />
                        <span className="text-sm font-semibold" style={{ color: connected ? '#86efac' : '#fcd34d' }}>
                            {connected ? 'Live Stream Active' : 'Reconnecting...'}
                        </span>
                    </div>
                </motion.div>

                {/* ── KPI Cards ── */}
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5 mb-8">
                    <StatCard icon={Users} label="Active Users (24h)" value={analytics.active_users_24h || 0} color="#6366f1" index={0} />
                    <StatCard icon={Activity} label="Total Actions (24h)" value={analytics.total_actions_24h || 0} color="#d97706" index={1} />
                    <StatCard icon={FileText} label="Total FIRs" value={totalFIRs} color="#10b981" index={2} />
                    <StatCard icon={MessageSquare} label="System Status" value="Healthy" color="#22c55e" index={3} />
                </div>

                {/* ── Charts Row ── */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">

                    {/* Action Breakdown */}
                    <motion.div
                        variants={fadeUp} initial="hidden" animate="visible" custom={4}
                        className="glass-card rounded-2xl p-7"
                    >
                        <h2 className="text-lg font-black mb-6" style={{ color: '#f1f5f9' }}>
                            Action Breakdown
                            <span className="ml-2 text-xs font-medium" style={{ color: '#64748b' }}>(Last 24h)</span>
                        </h2>
                        <div className="space-y-4">
                            {Object.entries(analytics.action_breakdown || {})
                                .sort((a, b) => b[1] - a[1])
                                .map(([action, count]) => (
                                    <div key={action}>
                                        <div className="flex justify-between items-center mb-1.5">
                                            <span className="text-sm capitalize" style={{ color: '#94a3b8' }}>
                                                {action.replace(/_/g, ' ')}
                                            </span>
                                            <span className="text-sm font-bold" style={{ color: '#f1f5f9' }}>{count}</span>
                                        </div>
                                        <div className="h-1.5 rounded-full overflow-hidden" style={{ background: 'rgba(255,255,255,0.05)' }}>
                                            <motion.div
                                                initial={{ width: 0 }}
                                                animate={{ width: `${(count / maxAction) * 100}%` }}
                                                transition={{ duration: 0.8, ease: 'easeOut' }}
                                                className="h-full rounded-full"
                                                style={{ background: 'linear-gradient(90deg,#6366f1,#818cf8)' }}
                                            />
                                        </div>
                                    </div>
                                ))}
                            {Object.keys(analytics.action_breakdown || {}).length === 0 && (
                                <p className="text-sm italic" style={{ color: '#334155' }}>No recent actions recorded.</p>
                            )}
                        </div>
                    </motion.div>

                    {/* Crime Distribution */}
                    <motion.div
                        variants={fadeUp} initial="hidden" animate="visible" custom={5}
                        className="glass-card rounded-2xl p-7"
                    >
                        <h2 className="text-lg font-black mb-6" style={{ color: '#f1f5f9' }}>
                            FIR Crime Distribution
                            <span className="ml-2 badge badge-gold" style={{ fontSize: '0.65rem' }}>All Time</span>
                        </h2>
                        <div className="space-y-4">
                            {Object.entries(analytics.crime_distribution || {})
                                .sort((a, b) => b[1] - a[1])
                                .map(([category, count]) => (
                                    <div key={category}>
                                        <div className="flex justify-between items-center mb-1.5">
                                            <span className="text-sm" style={{ color: '#94a3b8' }}>{category}</span>
                                            <span className="text-sm font-bold" style={{ color: '#f1f5f9' }}>{count}</span>
                                        </div>
                                        <div className="h-1.5 rounded-full overflow-hidden" style={{ background: 'rgba(255,255,255,0.05)' }}>
                                            <motion.div
                                                initial={{ width: 0 }}
                                                animate={{ width: `${(count / maxCrime) * 100}%` }}
                                                transition={{ duration: 0.8, ease: 'easeOut' }}
                                                className="h-full rounded-full"
                                                style={{ background: 'linear-gradient(90deg,#d97706,#f59e0b)' }}
                                            />
                                        </div>
                                    </div>
                                ))}
                            {Object.keys(analytics.crime_distribution || {}).length === 0 && (
                                <p className="text-sm italic" style={{ color: '#334155' }}>No FIRs recorded yet.</p>
                            )}
                        </div>
                    </motion.div>
                </div>
            </div>
        </div>
    );
}
