import React, { useState, useEffect } from 'react';
import { DocumentTextIcon, ArrowDownTrayIcon } from '@heroicons/react/24/outline';
import { motion } from 'framer-motion';
import { useTranslation } from 'react-i18next';
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
    const { t, i18n } = useTranslation();
    const [step, setStep] = useState(1);
    const [language, setLanguage] = useState(i18n.language || 'en');
    const [loading, setLoading] = useState(false);
    const [firDraft, setFirDraft] = useState('');

    useEffect(() => {
        setLanguage(i18n.language || 'en');
    }, [i18n.language]);
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
            const response = await firAPI.generateDraft(userId || '000000000000000000000000', formData, language);
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

            // Use the logged-in user id from context (falls back to 000000000000000000000000)
            const res = await firAPI.createFIR(userId || '000000000000000000000000', payload);
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

    const stepLabels = [t('fir.incidentDetails'), t('fir.yourDetails'), t('fir.additionalDetails'), t('fir.draftTitle')];

    return (
        <div className="page-bg py-12 px-4">
            <div className="max-w-4xl mx-auto">
                {/* Header */}
                <div className="mb-8">
                    <span className="section-tag"><DocumentTextIcon className="w-3.5 h-3.5" />FIR Generator</span>
                    <h1 className="text-4xl font-black mb-2" style={{ color: '#f1f5f9', letterSpacing: '-0.02em' }}>
                        {t('fir.title')}
                    </h1>
                    <p style={{ color: '#64748b' }}>{t('fir.subtitle')}</p>
                </div>

                {/* Step Progress */}
                <div className="flex items-center gap-2 mb-8 overflow-x-auto pb-2">
                    {stepLabels.map((label, i) => (
                        <React.Fragment key={i}>
                            <div className="flex items-center gap-2 flex-shrink-0">
                                <div className="w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold"
                                    style={{
                                        background: step > i + 1 ? 'linear-gradient(135deg,#22c55e,#16a34a)' : step === i + 1 ? 'linear-gradient(135deg,#6366f1,#4f46e5)' : 'rgba(255,255,255,0.06)',
                                        color: step >= i + 1 ? 'white' : '#475569',
                                    }}>
                                    {step > i + 1 ? '✓' : i + 1}
                                </div>
                                <span className="text-xs font-medium hidden sm:block" style={{ color: step === i + 1 ? '#a5b4fc' : '#475569' }}>{label}</span>
                            </div>
                            {i < stepLabels.length - 1 && (
                                <div className="flex-1 h-px min-w-[1rem]" style={{ background: step > i + 1 ? '#22c55e' : 'rgba(255,255,255,0.06)' }} />
                            )}
                        </React.Fragment>
                    ))}
                </div>

                {/* Language Selector */}
                <div className="mb-6">
                    <label className="label-dark">{t('fir.selectLanguage')}</label>
                    <select
                        value={language}
                        onChange={(e) => { setLanguage(e.target.value); i18n.changeLanguage(e.target.value); }}
                        className="select-dark w-full py-2.5 px-4"
                    >
                        <option value="en">English</option>
                        <option value="ta">தமிழ் (Tamil)</option>
                        <option value="hi">हिंदी (Hindi)</option>
                        <option value="te">తెలుగు (Telugu)</option>
                        <option value="ml">മലയാളം (Malayalam)</option>
                        <option value="ka">ಕನ್ನಡ (Kannada)</option>
                    </select>
                </div>

                {/* Steps */}
                {step === 1 && (
                    <motion.div initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} className="space-y-5">
                        <div className="glass-card rounded-2xl p-7">
                            <h2 className="text-xl font-black mb-5" style={{ color: '#f1f5f9' }}>{t('fir.incidentDetails')}</h2>
                            <div className="space-y-4">
                                <div>
                                    <label className="label-dark">{t('fir.titleLabel')}</label>
                                    <input type="text" name="title" value={formData.title} onChange={handleInputChange}
                                        placeholder={t('fir.titlePlaceholder')} className="input-dark" />
                                </div>
                                <div>
                                    <label className="label-dark">{t('fir.crimeCategory')}</label>
                                    <select name="crimeCategory" value={formData.crimeCategory} onChange={handleInputChange} className="select-dark w-full py-3 px-4">
                                        <option value="">{t('fir.selectCategory')}</option>
                                        {crimeCategoryOptions.map(cat => <option key={cat} value={cat}>{cat}</option>)}
                                    </select>
                                </div>
                                <div>
                                    <label className="label-dark">{t('fir.detailsLabel')}</label>
                                    <textarea name="incidentDetails" value={formData.incidentDetails} onChange={handleInputChange}
                                        placeholder={t('fir.detailsPlaceholder')} rows="5" className="input-dark resize-none" />
                                </div>
                                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                                    <div>
                                        <label className="label-dark">{t('fir.dateLabel')}</label>
                                        <input type="date" name="incidentDate" value={formData.incidentDate} onChange={handleInputChange} className="input-dark" />
                                    </div>
                                    <div>
                                        <label className="label-dark">{t('fir.locationLabel')}</label>
                                        <input type="text" name="incidentLocation" value={formData.incidentLocation} onChange={handleInputChange}
                                            placeholder={t('fir.locationPlaceholder')} className="input-dark" />
                                    </div>
                                </div>
                                <div className="flex gap-3 pt-2">
                                    <button onClick={() => setStep(2)} className="btn-primary px-8 py-3">
                                        <span className="relative z-10">{t('fir.buttonNext')} →</span>
                                    </button>
                                </div>
                            </div>
                        </div>
                    </motion.div>
                )}

                {step === 2 && (
                    <motion.div initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} className="space-y-5">
                        <div className="glass-card rounded-2xl p-7">
                            <h2 className="text-xl font-black mb-5" style={{ color: '#f1f5f9' }}>{t('fir.yourDetails')}</h2>
                            <div className="space-y-4">
                                <div>
                                    <label className="label-dark">{t('fir.fullNameLabel')}</label>
                                    <input type="text" name="name" value={formData.complainantDetails.name} onChange={handleComplainantChange}
                                        placeholder={t('fir.fullNamePlaceholder')} className="input-dark" />
                                </div>
                                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                                    <div>
                                        <label className="label-dark">{t('fir.phoneLabel')}</label>
                                        <input type="tel" name="phone" value={formData.complainantDetails.phone} onChange={handleComplainantChange}
                                            placeholder={t('fir.phonePlaceholder')} className="input-dark" />
                                    </div>
                                    <div>
                                        <label className="label-dark">{t('fir.emailLabel')}</label>
                                        <input type="email" name="email" value={formData.complainantDetails.email} onChange={handleComplainantChange}
                                            placeholder={t('fir.emailPlaceholder')} className="input-dark" />
                                    </div>
                                </div>
                                <div>
                                    <label className="label-dark">{t('fir.addressLabel')}</label>
                                    <textarea name="address" value={formData.complainantDetails.address} onChange={handleComplainantChange}
                                        placeholder={t('fir.addressPlaceholder')} rows="3" className="input-dark resize-none" />
                                </div>
                                <div className="flex gap-3 pt-2">
                                    <button onClick={() => setStep(1)} className="btn-outline px-8 py-3">{t('fir.buttonBack')}</button>
                                    <button onClick={() => setStep(3)} className="btn-primary px-8 py-3">
                                        <span className="relative z-10">{t('fir.buttonNext')} →</span>
                                    </button>
                                </div>
                            </div>
                        </div>
                    </motion.div>
                )}

                {step === 3 && (
                    <motion.div initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} className="space-y-5">
                        <div className="glass-card rounded-2xl p-7">
                            <h2 className="text-xl font-black mb-5" style={{ color: '#f1f5f9' }}>{t('fir.additionalDetails')}</h2>
                            <div className="space-y-4">
                                <div>
                                    <label className="label-dark">{t('fir.suspectNameLabel')}</label>
                                    <input type="text" name="name" value={formData.suspectDetails.name} onChange={handleSuspectChange}
                                        placeholder={t('fir.suspectNamePlaceholder')} className="input-dark" />
                                </div>
                                <div>
                                    <label className="label-dark">{t('fir.suspectDescLabel')}</label>
                                    <textarea name="description" value={formData.suspectDetails.description} onChange={handleSuspectChange}
                                        placeholder={t('fir.suspectDescPlaceholder')} rows="3" className="input-dark resize-none" />
                                </div>
                                <div>
                                    <label className="label-dark">{t('fir.evidenceLabel')}</label>
                                    <textarea placeholder={t('fir.evidencePlaceholder')} rows="3" className="input-dark resize-none"
                                        onChange={(e) => setFormData(prev => ({ ...prev, evidence: e.target.value.split('\n').filter(e => e.trim()) }))} />
                                </div>
                                <div className="flex gap-3 pt-2">
                                    <button onClick={() => setStep(2)} className="btn-outline px-8 py-3">{t('fir.buttonBack')}</button>
                                    <button onClick={generateFIR} disabled={loading} className="btn-primary px-8 py-3" style={{ opacity: loading ? 0.7 : 1 }}>
                                        <span className="relative z-10 flex items-center gap-2">
                                            {loading && <svg className="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"/><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/></svg>}
                                            {loading ? t('fir.buttonGenerating') : `⚡ ${t('fir.buttonGenerate')}`}
                                        </span>
                                    </button>
                                </div>
                            </div>
                        </div>
                    </motion.div>
                )}

                {step === 4 && (
                    <motion.div initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} className="space-y-5">
                        <div className="glass-card rounded-2xl p-7">
                            <div className="flex items-center gap-3 mb-5">
                                <span className="badge badge-green">✓ Draft Generated</span>
                                <h2 className="text-xl font-black" style={{ color: '#f1f5f9' }}>{t('fir.draftTitle')}</h2>
                            </div>
                            <div className="rounded-xl p-5 mb-5 max-h-96 overflow-y-auto"
                                style={{ background: 'rgba(0,0,0,0.3)', border: '1px solid rgba(255,255,255,0.06)' }}>
                                <pre className="whitespace-pre-wrap text-sm font-mono" style={{ color: '#94a3b8', lineHeight: '1.7' }}>{firDraft}</pre>
                            </div>
                            <div className="flex flex-wrap gap-3">
                                <button onClick={() => setStep(1)} className="btn-outline px-6 py-2.5 text-sm">{t('fir.buttonCreateNew')}</button>
                                <button onClick={submitDraft} disabled={loading} className="btn-primary px-6 py-2.5 text-sm" style={{ opacity: loading ? 0.7 : 1 }}>
                                    <span className="relative z-10 flex items-center gap-2">
                                        {loading ? 'Saving...' : `💾 ${t('fir.buttonSubmitDraft')}`}
                                    </span>
                                </button>
                                <button onClick={downloadPDF} className="btn-gold px-6 py-2.5 text-sm">
                                    <ArrowDownTrayIcon className="w-4 h-4" />
                                    {t('fir.buttonDownload')}
                                </button>
                            </div>
                        </div>
                    </motion.div>
                )}

                {/* Disclaimer */}
                <div className="mt-8 flex items-start gap-3 rounded-xl px-5 py-4"
                    style={{ background: 'rgba(234,179,8,0.06)', border: '1px solid rgba(234,179,8,0.15)' }}>
                    <span style={{ color: '#ca8a04' }}>⚠</span>
                    <p className="text-sm" style={{ color: '#a16207' }}>{t('fir.disclaimer')}</p>
                </div>
            </div>
        </div>
    );
}
