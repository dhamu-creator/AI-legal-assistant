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
                // refresh list
                await fetchFIRs();
                setEditing(false);
                // update selected
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

    return (
        <div className="max-w-5xl mx-auto px-4 py-8">
            <h2 className="text-2xl font-semibold mb-4">My FIRs</h2>

            <div className="grid md:grid-cols-3 gap-6">
                <div className="md:col-span-1">
                    <div className="bg-white rounded shadow p-4">
                        <h3 className="font-medium mb-2">FIRs</h3>
                        {loading ? (
                            <p>Loading...</p>
                        ) : firs.length === 0 ? (
                            <p className="text-sm text-gray-500">No FIRs yet.</p>
                        ) : (
                            <ul>
                                {firs.map((f) => (
                                    <li key={f._id || f.id} className="py-2 border-b last:border-b-0">
                                        <button
                                            onClick={() => viewFIR(f)}
                                            className="text-left w-full"
                                        >
                                            <div className="font-semibold">{f.title || f.crimeCategory || 'Untitled'}</div>
                                            <div className="text-xs text-gray-500">{new Date(f.createdAt || f.date || Date.now()).toLocaleString()}</div>
                                        </button>
                                    </li>
                                ))}
                            </ul>
                        )}
                    </div>
                </div>

                <div className="md:col-span-2">
                    <div className="bg-white rounded shadow p-6 min-h-[240px]">
                        {!selected ? (
                            <p className="text-gray-500">Select an FIR to view details</p>
                        ) : (
                            <div>
                                <div className="flex items-start justify-between">
                                    <div>
                                        <h3 className="text-xl font-semibold">{selected.title || selected.crimeCategory}</h3>
                                        <p className="text-sm text-gray-500">Status: {selected.status || 'draft'}</p>
                                    </div>
                                    <div className="flex gap-2">
                                        <button
                                            onClick={() => startEdit()}
                                            className="px-3 py-1 bg-indigo-600 text-white rounded"
                                        >
                                            Edit
                                        </button>
                                        <button
                                            onClick={() => removeFIR(selected)}
                                            className="px-3 py-1 bg-red-500 text-white rounded"
                                        >
                                            Delete
                                        </button>
                                    </div>
                                </div>

                                <div className="mt-4">
                                    {editing ? (
                                        <div className="space-y-3">
                                            <label className="block">
                                                <div className="text-sm text-gray-600">Title</div>
                                                <input
                                                    value={form.title || ''}
                                                    onChange={(e) => setForm({ ...form, title: e.target.value })}
                                                    className="w-full border rounded px-3 py-2"
                                                />
                                            </label>

                                            <label className="block">
                                                <div className="text-sm text-gray-600">Complainant Name</div>
                                                <input
                                                    value={form.complainantName || ''}
                                                    onChange={(e) => setForm({ ...form, complainantName: e.target.value })}
                                                    className="w-full border rounded px-3 py-2"
                                                />
                                            </label>

                                            <label className="block">
                                                <div className="text-sm text-gray-600">Incident Date</div>
                                                <input
                                                    type="date"
                                                    value={form.incidentDate ? form.incidentDate.split('T')[0] : ''}
                                                    onChange={(e) => setForm({ ...form, incidentDate: e.target.value })}
                                                    className="w-full border rounded px-3 py-2"
                                                />
                                            </label>

                                            <label className="block">
                                                <div className="text-sm text-gray-600">Details</div>
                                                <textarea
                                                    value={form.details || form.description || ''}
                                                    onChange={(e) => setForm({ ...form, details: e.target.value })}
                                                    rows={6}
                                                    className="w-full border rounded px-3 py-2"
                                                />
                                            </label>

                                            <div className="flex gap-2">
                                                <button onClick={saveEdit} className="px-4 py-2 bg-green-600 text-white rounded">Save</button>
                                                <button onClick={() => setEditing(false)} className="px-4 py-2 bg-gray-200 rounded">Cancel</button>
                                            </div>
                                        </div>
                                    ) : (
                                        <div className="prose">
                                            <p><strong>Complainant:</strong> {selected.complainantName || '—'}</p>
                                            <p><strong>Incident Date:</strong> {selected.incidentDate ? new Date(selected.incidentDate).toLocaleString() : '—'}</p>
                                            <div className="mt-3">
                                                <h4 className="font-medium">Details</h4>
                                                <p className="whitespace-pre-wrap">{selected.details || selected.description || selected.firText || '—'}</p>
                                            </div>

                                            <div className="mt-4 flex gap-2">
                                                <a
                                                    href={`${API_BASE_URL.replace(/\/$/, '')}/fir/pdf/${selected._id || selected.id}?language=${(selected.language || 'en')}`}
                                                    target="_blank"
                                                    rel="noreferrer"
                                                    className="px-3 py-1 bg-indigo-600 text-white rounded"
                                                >
                                                    Download PDF
                                                </a>
                                                <button
                                                    onClick={async () => {
                                                        if (!confirm('Finalize and submit this FIR?')) return;
                                                        try {
                                                            await firAPI.finalizeFIR(selected._id || selected.id);
                                                            await fetchFIRs();
                                                            // refresh selected
                                                            const refreshed = await firAPI.getFIR(selected._id || selected.id);
                                                            setSelected(refreshed.data.data || refreshed.data);
                                                            alert('FIR finalized and submitted.');
                                                        } catch (e) {
                                                            console.error('finalize', e);
                                                            alert('Failed to finalize FIR');
                                                        }
                                                    }}
                                                    className="px-3 py-1 bg-yellow-500 text-white rounded"
                                                >
                                                    Finalize
                                                </button>
                                            </div>
                                        </div>
                                    )}
                                </div>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
}
