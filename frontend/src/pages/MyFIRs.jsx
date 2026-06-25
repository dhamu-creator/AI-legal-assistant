import React, { useEffect, useState } from 'react';
import { useChat } from '../context/ChatContext';
import { firAPI, API_BASE_URL } from '../services/api';

export default function MyFIRs() {
    const { userId } = useChat();
    const [firs, setFirs] = useState([]);
    const [loading, setLoading] = useState(false);
    const [selected, setSelected] = useState(null);
    const [editing, setEditing] = useState(false);
    const [form, setForm] = useState({});

    useEffect(() => {
        if (!userId) return;
        fetchFIRs();
    }, [userId]);

    const fetchFIRs = async () => {
        setLoading(true);
        try {
            const res = await firAPI.getUserFIRs(userId);
            if (res?.data) setFirs(res.data.data || res.data || []);
        } catch (e) {
            console.error('fetchFIRs', e);
        } finally {
            setLoading(false);
        }
    };

    const viewFIR = async (fir) => {
        setSelected(fir);
        setEditing(false);
        setForm(fir);
    };

    const startEdit = () => {
        setEditing(true);
        setForm(selected);
    };

    const saveEdit = async () => {
        try {
            const res = await firAPI.updateFIR(selected._id || selected.id, form);
            if (res?.data) {
                await fetchFIRs();
                setEditing(false);
                const updated = (res.data.data && res.data.data.fir) || res.data;
                setSelected(updated || form);
            }
        } catch (e) {
            console.error('saveEdit', e);
        }
    };

    const removeFIR = async (fir) => {
        if (!confirm('Delete this FIR?')) return;
        try {
            await firAPI.deleteFIR(fir._id || fir.id);
            await fetchFIRs();
            setSelected(null);
        } catch (e) {
            console.error('deleteFIR', e);
        }
    };

    const statusColor = (status) => {
        if (status === 'finalized' || status === 'submitted') return 'badge-green';
        if (status === 'draft') return 'badge-gold';
        return 'badge-indigo';
    };

    return (
        <div className="page-bg px-4 py-12">
            <div className="max-w-6xl mx-auto">
                <div className="mb-8">
                    <span className="section-tag">📁 FIR Management</span>
                    <h1 className="text-4xl font-black mb-2" style={{ color: '#f1f5f9', letterSpacing: '-0.02em' }}>
                        My FIRs
                    </h1>
                    <p style={{ color: '#64748b' }}>View, edit and manage all your filed FIRs</p>
                </div>

                <div className="grid md:grid-cols-3 gap-6">
                    <div className="md:col-span-1">
                        <div className="glass-card rounded-2xl p-5">
                            <div className="flex items-center justify-between mb-4">
                                <h3 className="font-bold text-sm" style={{ color: '#f1f5f9' }}>All FIRs</h3>
                                <span className="badge badge-indigo">{firs.length}</span>
                            </div>

                            {loading ? (
                                <div className="flex items-center gap-2 py-4">
                                    <div className="typing-dot" /><div className="typing-dot" /><div className="typing-dot" />
                                    <span className="text-sm" style={{ color: '#64748b' }}>Loading...</span>
                                </div>
                            ) : firs.length === 0 ? (
                                <div className="text-center py-8">
                                    <div className="text-3xl mb-2">📂</div>
                                    <p className="text-sm" style={{ color: '#64748b' }}>No FIRs yet.</p>
                                    <p className="text-xs mt-1" style={{ color: '#334155' }}>Generate your first FIR to get started.</p>
                                </div>
                            ) : (
                                <ul className="space-y-2">
                                    {firs.map((f) => (
                                        <li key={f._id || f.id}>
                                            <button
                                                onClick={() => viewFIR(f)}
                                                className="w-full text-left px-3 py-3 rounded-xl transition-all duration-200"
                                                style={{
                                                    background: selected?._id === f._id ? 'rgba(99,102,241,0.15)' : 'rgba(255,255,255,0.03)',
                                                    border: `1px solid ${selected?._id === f._id ? 'rgba(99,102,241,0.3)' : 'rgba(255,255,255,0.06)'}`,
                                                }}
                                                onMouseEnter={e => { if (selected?._id !== f._id) e.currentTarget.style.background = 'rgba(99,102,241,0.07)'; }}
                                                onMouseLeave={e => { if (selected?._id !== f._id) e.currentTarget.style.background = 'rgba(255,255,255,0.03)'; }}
                                            >
                                                <div className="font-semibold text-sm mb-1" style={{ color: '#e2e8f0' }}>
                                                    {f.title || f.crimeCategory || 'Untitled'}
                                                </div>
                                                <div className="flex items-center justify-between">
                                                    <span className="text-xs" style={{ color: '#475569' }}>
                                                        {new Date(f.createdAt || f.date || Date.now()).toLocaleDateString()}
                                                    </span>
                                                    <span className={`badge ${statusColor(f.status)}`} style={{ fontSize: '0.6rem', padding: '0.15rem 0.5rem' }}>
                                                        {f.status || 'draft'}
                                                    </span>
                                                </div>
                                            </button>
                                        </li>
                                    ))}
                                </ul>
                            )}
                        </div>
                    </div>

                    <div className="md:col-span-2">
                        <div className="glass-card rounded-2xl p-7 min-h-[300px]">
                            {!selected ? (
                                <div className="flex flex-col items-center justify-center h-48 text-center">
                                    <div className="text-4xl mb-3 animate-float">📄</div>
                                    <p className="text-base font-semibold" style={{ color: '#475569' }}>Select an FIR to view details</p>
                                    <p className="text-sm mt-1" style={{ color: '#334155' }}>Click any FIR from the list on the left</p>
                                </div>
                            ) : (
                                <div>
                                    <div className="flex items-start justify-between mb-6">
                                        <div>
                                            <h3 className="text-xl font-black mb-1" style={{ color: '#f1f5f9' }}>
                                                {selected.title || selected.crimeCategory}
                                            </h3>
                                            <div className="flex items-center gap-2">
                                                <span className={`badge ${statusColor(selected.status)}`}>
                                                    {selected.status || 'draft'}
                                                </span>
                                                <span className="text-xs" style={{ color: '#475569' }}>
                                                    {selected.crimeCategory && `• ${selected.crimeCategory}`}
                                                </span>
                                            </div>
                                        </div>
                                        <div className="flex gap-2">
                                            <button onClick={startEdit} className="btn-outline px-4 py-2 text-sm">✏️ Edit</button>
                                            <button onClick={() => removeFIR(selected)}
                                                className="px-4 py-2 rounded-xl text-sm font-semibold transition"
                                                style={{ background: 'rgba(239,68,68,0.1)', color: '#fca5a5', border: '1px solid rgba(239,68,68,0.2)' }}
                                                onMouseEnter={e => e.currentTarget.style.background = 'rgba(239,68,68,0.2)'}
                                                onMouseLeave={e => e.currentTarget.style.background = 'rgba(239,68,68,0.1)'}>
                                                🗑️ Delete
                                            </button>
                                        </div>
                                    </div>

                                    {editing ? (
                                        <div className="space-y-4">
                                            <div>
                                                <label className="label-dark">Title</label>
                                                <input value={form.title || ''} onChange={(e) => setForm({ ...form, title: e.target.value })} className="input-dark" />
                                            </div>
                                            <div>
                                                <label className="label-dark">Complainant Name</label>
                                                <input value={form.complainantName || ''} onChange={(e) => setForm({ ...form, complainantName: e.target.value })} className="input-dark" />
                                            </div>
                                            <div>
                                                <label className="label-dark">Incident Date</label>
                                                <input type="date" value={form.incidentDate ? form.incidentDate.split('T')[0] : ''} onChange={(e) => setForm({ ...form, incidentDate: e.target.value })} className="input-dark" />
                                            </div>
                                            <div>
                                                <label className="label-dark">Details</label>
                                                <textarea value={form.details || form.description || ''} onChange={(e) => setForm({ ...form, details: e.target.value })} rows={5} className="input-dark resize-none" />
                                            </div>
                                            <div className="flex gap-3 pt-2">
                                                <button onClick={saveEdit} className="btn-primary px-6 py-2.5 text-sm">
                                                    <span className="relative z-10">💾 Save Changes</span>
                                                </button>
                                                <button onClick={() => setEditing(false)} className="btn-outline px-6 py-2.5 text-sm">Cancel</button>
                                            </div>
                                        </div>
                                    ) : (
                                        <div>
                                            <div className="grid grid-cols-2 gap-4 mb-5">
                                                <div className="p-3 rounded-xl" style={{ background: 'rgba(255,255,255,0.03)', border: '1px solid rgba(255,255,255,0.06)' }}>
                                                    <p className="text-xs font-semibold uppercase tracking-wider mb-1" style={{ color: '#475569' }}>Complainant</p>
                                                    <p className="text-sm font-medium" style={{ color: '#cbd5e1' }}>{selected.complainantName || selected.complainantDetails?.name || '—'}</p>
                                                </div>
                                                <div className="p-3 rounded-xl" style={{ background: 'rgba(255,255,255,0.03)', border: '1px solid rgba(255,255,255,0.06)' }}>
                                                    <p className="text-xs font-semibold uppercase tracking-wider mb-1" style={{ color: '#475569' }}>Incident Date</p>
                                                    <p className="text-sm font-medium" style={{ color: '#cbd5e1' }}>{selected.incidentDate ? new Date(selected.incidentDate).toLocaleDateString() : '—'}</p>
                                                </div>
                                            </div>
                                            <div>
                                                <p className="text-xs font-semibold uppercase tracking-wider mb-2" style={{ color: '#475569' }}>Details</p>
                                                <div className="rounded-xl p-4" style={{ background: 'rgba(0,0,0,0.2)', border: '1px solid rgba(255,255,255,0.04)' }}>
                                                    <p className="text-sm whitespace-pre-wrap" style={{ color: '#94a3b8', lineHeight: '1.7' }}>
                                                        {selected.details || selected.description || selected.firText || selected.firDraft || '—'}
                                                    </p>
                                                </div>
                                            </div>
                                            <div className="flex flex-wrap gap-3 mt-6">
                                                <a href={`${API_BASE_URL.replace(/\/$/, '')}/fir/pdf/${selected._id || selected.id}?language=${(selected.language || 'en')}`}
                                                    target="_blank" rel="noreferrer" className="btn-primary px-5 py-2.5 text-sm">
                                                    <span className="relative z-10">⬇️ Download PDF</span>
                                                </a>
                                                {(selected.status === 'draft') && (
                                                    <button onClick={async () => {
                                                        if (!confirm('Finalize and submit this FIR?')) return;
                                                        try {
                                                            await firAPI.finalizeFIR(selected._id || selected.id);
                                                            await fetchFIRs();
                                                            const refreshed = await firAPI.getFIR(selected._id || selected.id);
                                                            setSelected(refreshed.data.data || refreshed.data);
                                                        } catch (e) { console.error('finalize', e); }
                                                    }} className="btn-gold px-5 py-2.5 text-sm">
                                                        ✅ Finalize FIR
                                                    </button>
                                                )}
                                            </div>
                                        </div>
                                    )}
                                </div>
                            )}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
