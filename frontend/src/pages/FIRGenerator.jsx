import React, { useState } from 'react';
import { DocumentTextIcon, ArrowDownTrayIcon } from '@heroicons/react/24/outline';
import { motion } from 'framer-motion';
import axios from 'axios';
import { firAPI } from '../services/api';
import { useChat } from '../context/ChatContext';

const crimeCategoryOptions = [
    'Theft',
    'Robbery',
    'CyberFraud',
    'Harassment',
    'DomesticViolence',
    'Blackmail',
    'OnlineScams',
    'IdentityTheft',
    'FinancialFraud',
    'PhysicalAssault',
];

export default function FIRGenerator() {
    const [step, setStep] = useState(1);
    const [language, setLanguage] = useState('en');
    const [loading, setLoading] = useState(false);
    const [firDraft, setFirDraft] = useState('');
    const [formData, setFormData] = useState({
        title: '',
        incidentDetails: '',
        incidentDate: '',
        incidentLocation: '',
        crimeCategory: '',
        complainantDetails: {
            name: '',
            phone: '',
            address: '',
            email: '',
        },
        suspectDetails: {
            name: '',
            description: '',
            address: '',
        },
        witnessDetails: [],
        evidence: [],
    });

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData((prev) => ({
            ...prev,
            [name]: value,
        }));
    };

    const handleComplainantChange = (e) => {
        const { name, value } = e.target;
        setFormData((prev) => ({
            ...prev,
            complainantDetails: {
                ...prev.complainantDetails,
                [name]: value,
            },
        }));
    };

    const handleSuspectChange = (e) => {
        const { name, value } = e.target;
        setFormData((prev) => ({
            ...prev,
            suspectDetails: {
                ...prev.suspectDetails,
                [name]: value,
            },
        }));
    };

    const { userId } = useChat();

    const generateFIR = async () => {
        if (!formData.incidentDetails || !formData.crimeCategory || !formData.complainantDetails.name) {
            alert('Please fill in all required fields');
            return;
        }

        setLoading(true);
        try {
            const response = await firAPI.generateDraft(userId || 'demo-user', formData, language);
            setFirDraft(response.data.data.firDraft);
            setStep(4);
        } catch (error) {
            console.error('Error generating FIR:', error);
            alert('Failed to generate FIR. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    const downloadPDF = () => {
        const element = document.createElement('a');
        const file = new Blob([firDraft], { type: 'text/plain' });
        element.href = URL.createObjectURL(file);
        element.download = `FIR_${new Date().getTime()}.txt`;
        document.body.appendChild(element);
        element.click();
        document.body.removeChild(element);
    };

    const submitDraft = async () => {
        setLoading(true);
        try {
            const payload = {
                title: formData.title || `FIR - ${new Date().toLocaleDateString()}`,
                incidentDetails: formData.incidentDetails,
                incidentDate: formData.incidentDate || new Date().toISOString(),
                incidentLocation: formData.incidentLocation,
                crimeCategory: formData.crimeCategory || 'Theft',
                complainantDetails: formData.complainantDetails,
                suspectDetails: formData.suspectDetails,
                witnessDetails: formData.witnessDetails,
                evidence: formData.evidence,
                firDraft,
            };

            // Use the logged-in user id from context (falls back to demo-user)
            const res = await firAPI.createFIR(userId || 'demo-user', payload);
            if (res?.data?.success) {
                alert('FIR draft submitted and saved (status: draft).');
                setStep(1);
                setFormData({
                    title: '',
                    incidentDetails: '',
                    incidentDate: '',
                    incidentLocation: '',
                    crimeCategory: '',
                    complainantDetails: { name: '', phone: '', address: '', email: '' },
                    suspectDetails: { name: '', description: '', address: '' },
                    witnessDetails: [],
                    evidence: [],
                });
                setFirDraft('');
            } else {
                alert('Failed to save FIR draft.');
            }
        } catch (err) {
            console.error('Submit FIR failed', err);
            alert('Submission failed. Check console for details.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-gray-50 py-12 px-4">
            <div className="max-w-4xl mx-auto">
                {/* Header */}
                <div className="mb-8">
                    <h1 className="text-4xl font-bold text-gray-900 mb-2 flex items-center gap-2">
                        <DocumentTextIcon className="w-8 h-8 text-indigo-600" />
                        FIR/Complaint Generator
                    </h1>
                    <p className="text-gray-600">Generate a professional FIR (First Information Report) or complaint</p>
                </div>

                {/* Language Selector */}
                <div className="mb-6">
                    <label className="block text-sm font-medium text-gray-700 mb-2">Select Language</label>
                    <select
                        value={language}
                        onChange={(e) => setLanguage(e.target.value)}
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
                    >
                        <option value="en">English</option>
                        <option value="ta">Tamil</option>
                        <option value="hi">Hindi</option>
                        <option value="te">Telugu</option>
                        <option value="ml">Malayalam</option>
                        <option value="ka">Kannada</option>
                    </select>
                </div>

                {/* Steps */}
                {step === 1 && (
                    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-6">
                        <div className="bg-white rounded-lg shadow p-6">
                            <h2 className="text-2xl font-bold text-gray-900 mb-4">Incident Details</h2>
                            <div className="space-y-4">
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-1">FIR Title *</label>
                                    <input
                                        type="text"
                                        name="title"
                                        value={formData.title}
                                        onChange={handleInputChange}
                                        placeholder="e.g., Phone Theft Complaint"
                                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
                                    />
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-1">Crime Category *</label>
                                    <select
                                        name="crimeCategory"
                                        value={formData.crimeCategory}
                                        onChange={handleInputChange}
                                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
                                    >
                                        <option value="">Select a crime category</option>
                                        {crimeCategoryOptions.map((cat) => (
                                            <option key={cat} value={cat}>
                                                {cat}
                                            </option>
                                        ))}
                                    </select>
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-1">Incident Details *</label>
                                    <textarea
                                        name="incidentDetails"
                                        value={formData.incidentDetails}
                                        onChange={handleInputChange}
                                        placeholder="Describe what happened in detail..."
                                        rows="5"
                                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
                                    />
                                </div>
                                <div className="grid grid-cols-2 gap-4">
                                    <div>
                                        <label className="block text-sm font-medium text-gray-700 mb-1">Incident Date</label>
                                        <input
                                            type="date"
                                            name="incidentDate"
                                            value={formData.incidentDate}
                                            onChange={handleInputChange}
                                            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
                                        />
                                    </div>
                                    <div>
                                        <label className="block text-sm font-medium text-gray-700 mb-1">Location</label>
                                        <input
                                            type="text"
                                            name="incidentLocation"
                                            value={formData.incidentLocation}
                                            onChange={handleInputChange}
                                            placeholder="Where did it happen?"
                                            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
                                        />
                                    </div>
                                </div>
                                <div className="flex gap-3">
                                    <motion.button
                                        whileHover={{ scale: 1.05 }}
                                        whileTap={{ scale: 0.95 }}
                                        onClick={() => setStep(2)}
                                        className="px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition"
                                    >
                                        Next
                                    </motion.button>
                                </div>
                            </div>
                        </div>
                    </motion.div>
                )}

                {step === 2 && (
                    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-6">
                        <div className="bg-white rounded-lg shadow p-6">
                            <h2 className="text-2xl font-bold text-gray-900 mb-4">Your Details</h2>
                            <div className="space-y-4">
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-1">Full Name *</label>
                                    <input
                                        type="text"
                                        name="name"
                                        value={formData.complainantDetails.name}
                                        onChange={handleComplainantChange}
                                        placeholder="Your name"
                                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
                                    />
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-1">Phone Number *</label>
                                    <input
                                        type="tel"
                                        name="phone"
                                        value={formData.complainantDetails.phone}
                                        onChange={handleComplainantChange}
                                        placeholder="Your phone number"
                                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
                                    />
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
                                    <input
                                        type="email"
                                        name="email"
                                        value={formData.complainantDetails.email}
                                        onChange={handleComplainantChange}
                                        placeholder="Your email"
                                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
                                    />
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-1">Address</label>
                                    <textarea
                                        name="address"
                                        value={formData.complainantDetails.address}
                                        onChange={handleComplainantChange}
                                        placeholder="Your address"
                                        rows="3"
                                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
                                    />
                                </div>
                                <div className="flex gap-3">
                                    <button
                                        onClick={() => setStep(1)}
                                        className="px-6 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition"
                                    >
                                        Back
                                    </button>
                                    <motion.button
                                        whileHover={{ scale: 1.05 }}
                                        whileTap={{ scale: 0.95 }}
                                        onClick={() => setStep(3)}
                                        className="px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition"
                                    >
                                        Next
                                    </motion.button>
                                </div>
                            </div>
                        </div>
                    </motion.div>
                )}

                {step === 3 && (
                    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-6">
                        <div className="bg-white rounded-lg shadow p-6">
                            <h2 className="text-2xl font-bold text-gray-900 mb-4">Additional Details</h2>
                            <div className="space-y-4">
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-1">Suspect Name (if known)</label>
                                    <input
                                        type="text"
                                        name="name"
                                        value={formData.suspectDetails.name}
                                        onChange={handleSuspectChange}
                                        placeholder="Suspect name"
                                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
                                    />
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-1">Suspect Description</label>
                                    <textarea
                                        name="description"
                                        value={formData.suspectDetails.description}
                                        onChange={handleSuspectChange}
                                        placeholder="Physical description, clothing, etc."
                                        rows="3"
                                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
                                    />
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-1">Evidence Available</label>
                                    <textarea
                                        placeholder="List evidence: e.g., CCTV footage, witness contact, photos, etc."
                                        rows="3"
                                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
                                        onChange={(e) => {
                                            setFormData((prev) => ({
                                                ...prev,
                                                evidence: e.target.value.split('\n').filter((e) => e.trim()),
                                            }));
                                        }}
                                    />
                                </div>
                                <div className="flex gap-3">
                                    <button
                                        onClick={() => setStep(2)}
                                        className="px-6 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition"
                                    >
                                        Back
                                    </button>
                                    <motion.button
                                        whileHover={{ scale: 1.05 }}
                                        whileTap={{ scale: 0.95 }}
                                        onClick={generateFIR}
                                        disabled={loading}
                                        className="px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 disabled:bg-gray-400 transition"
                                    >
                                        {loading ? 'Generating...' : 'Generate FIR'}
                                    </motion.button>
                                </div>
                            </div>
                        </div>
                    </motion.div>
                )}

                {step === 4 && (
                    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-6">
                        <div className="bg-white rounded-lg shadow p-6">
                            <h2 className="text-2xl font-bold text-gray-900 mb-4">Your FIR Draft</h2>
                            <div className="bg-gray-50 p-6 rounded-lg mb-4 max-h-96 overflow-y-auto border border-gray-200">
                                <pre className="whitespace-pre-wrap text-sm text-gray-800 font-mono">{firDraft}</pre>
                            </div>
                            <div className="flex gap-3">
                                <motion.button
                                    whileHover={{ scale: 1.05 }}
                                    whileTap={{ scale: 0.95 }}
                                    onClick={() => setStep(1)}
                                    className="px-6 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition"
                                >
                                    Create New
                                </motion.button>
                                <motion.button
                                    whileHover={{ scale: 1.05 }}
                                    whileTap={{ scale: 0.95 }}
                                    onClick={submitDraft}
                                    disabled={loading}
                                    className="px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 disabled:bg-gray-400 transition"
                                >
                                    {loading ? 'Submitting...' : 'Submit Draft'}
                                </motion.button>
                                <motion.button
                                    whileHover={{ scale: 1.05 }}
                                    whileTap={{ scale: 0.95 }}
                                    onClick={downloadPDF}
                                    className="px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition flex items-center gap-2"
                                >
                                    <ArrowDownTrayIcon className="w-5 h-5" />
                                    Download
                                </motion.button>
                            </div>
                        </div>
                    </motion.div>
                )}

                {/* Disclaimer */}
                <div className="mt-8 bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                    <p className="text-sm text-yellow-800">
                        <span className="font-semibold">⚠️ Important:</span> This is an AI-generated draft. Please review it carefully
                        and consult with a lawyer before submitting to police.
                    </p>
                </div>
            </div>
        </div>
    );
}
