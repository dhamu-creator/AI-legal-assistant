import React from 'react';
import { motion } from 'framer-motion';
import { useTranslation } from 'react-i18next';
import {
    PhoneIcon,
    ExclamationTriangleIcon,
    ShieldCheckIcon,
    CheckCircleIcon,
    ArrowRightIcon,
} from '@heroicons/react/24/outline';

const fadeUp = {
    hidden: { opacity: 0, y: 30 },
    visible: (i = 0) => ({
        opacity: 1, y: 0,
        transition: { duration: 0.55, delay: i * 0.1, ease: [0.22, 1, 0.36, 1] },
    }),
};

export default function EmergencyHelp() {
    const { t } = useTranslation();

    const emergencyContacts = [
        {
            name: t('emergency.contacts.police.name'),
            number: '100',
            description: t('emergency.contacts.police.desc'),
            icon: '🚔',
            color: '#3b82f6',
        },
        {
            name: t('emergency.contacts.women.name'),
            number: '1091',
            description: t('emergency.contacts.women.desc'),
            icon: '👩‍⚖️',
            color: '#ec4899',
        },
        {
            name: t('emergency.contacts.cyber.name'),
            number: '1930',
            description: t('emergency.contacts.cyber.desc'),
            icon: '💻',
            color: '#8b5cf6',
        },
        {
            name: t('emergency.contacts.child.name'),
            number: '1098',
            description: t('emergency.contacts.child.desc'),
            icon: '👶',
            color: '#10b981',
        },
        {
            name: t('emergency.contacts.unified.name'),
            number: '112',
            description: t('emergency.contacts.unified.desc'),
            icon: '🆘',
            color: '#ef4444',
        },
    ];

    const procedures = [
        {
            title: t('emergency.refuse.title'),
            icon: '📋',
            color: '#6366f1',
            steps: [
                t('emergency.refuse.step1'),
                t('emergency.refuse.step2'),
                t('emergency.refuse.step3'),
                t('emergency.refuse.step4'),
                t('emergency.refuse.step5'),
            ],
        },
        {
            title: t('emergency.complaint.title'),
            icon: '📝',
            color: '#d97706',
            steps: [
                t('emergency.complaint.step1'),
                t('emergency.complaint.step2'),
                t('emergency.complaint.step3'),
                t('emergency.complaint.step4'),
                t('emergency.complaint.step5'),
            ],
        },
        {
            title: t('emergency.cybercrime.title'),
            icon: '🔐',
            color: '#8b5cf6',
            steps: [
                t('emergency.cybercrime.step1'),
                t('emergency.cybercrime.step2'),
                t('emergency.cybercrime.step3'),
                t('emergency.cybercrime.step4'),
                t('emergency.cybercrime.step5'),
            ],
        },
    ];

    const notes = [
        t('emergency.notes.note1'),
        t('emergency.notes.note2'),
        t('emergency.notes.note3'),
        t('emergency.notes.note4'),
        t('emergency.notes.note5'),
        t('emergency.notes.note6'),
    ];

    return (
        <div className="page-bg px-4 py-16">
            <div className="max-w-6xl mx-auto">

                {/* ── Header ── */}
                <motion.div
                    variants={fadeUp} initial="hidden" animate="visible"
                    className="mb-14"
                >
                    <span className="section-tag">
                        <ExclamationTriangleIcon className="w-3.5 h-3.5" />
                        Emergency Legal Help
                    </span>
                    <h1 className="text-4xl md:text-5xl font-black mb-3"
                        style={{ color: '#f1f5f9', letterSpacing: '-0.02em' }}>
                        {t('emergency.title')}
                    </h1>
                    <p className="text-lg" style={{ color: '#64748b' }}>
                        {t('emergency.subtitle')}
                    </p>
                </motion.div>

                {/* ── Emergency Contacts ── */}
                <section className="mb-16">
                    <motion.h2
                        variants={fadeUp} initial="hidden" whileInView="visible" viewport={{ once: true }}
                        className="text-2xl font-black mb-6" style={{ color: '#f1f5f9' }}>
                        {t('emergency.contactsTitle')}
                    </motion.h2>

                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
                        {emergencyContacts.map((contact, i) => (
                            <motion.a
                                key={i}
                                href={`tel:${contact.number}`}
                                variants={fadeUp} initial="hidden" whileInView="visible"
                                viewport={{ once: true }} custom={i}
                                className="emergency-card"
                            >
                                {/* Icon + Number */}
                                <div className="flex items-center gap-3 mb-3">
                                    <div className="w-10 h-10 rounded-xl flex items-center justify-center text-xl"
                                        style={{ background: `${contact.color}18`, border: `1px solid ${contact.color}30` }}>
                                        {contact.icon}
                                    </div>
                                    <div>
                                        <div className="text-2xl font-black" style={{ color: contact.color, lineHeight: 1 }}>
                                            {contact.number}
                                        </div>
                                        <div className="text-xs" style={{ color: '#334155' }}>Tap to call</div>
                                    </div>
                                </div>
                                <h3 className="font-bold text-sm mb-1" style={{ color: '#e2e8f0' }}>{contact.name}</h3>
                                <p className="text-xs leading-relaxed" style={{ color: '#64748b' }}>{contact.description}</p>

                                <div className="mt-3 flex items-center gap-1 text-xs font-medium" style={{ color: contact.color }}>
                                    <PhoneIcon className="w-3.5 h-3.5" />
                                    Call Now
                                    <ArrowRightIcon className="w-3 h-3" />
                                </div>
                            </motion.a>
                        ))}
                    </div>
                </section>

                {/* ── Procedures ── */}
                <section className="mb-16">
                    <motion.h2
                        variants={fadeUp} initial="hidden" whileInView="visible" viewport={{ once: true }}
                        className="text-2xl font-black mb-6" style={{ color: '#f1f5f9' }}>
                        {t('emergency.proceduresTitle')}
                    </motion.h2>

                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                        {procedures.map((proc, i) => (
                            <motion.div
                                key={i}
                                variants={fadeUp} initial="hidden" whileInView="visible"
                                viewport={{ once: true }} custom={i}
                                className="glass-card rounded-2xl p-6"
                            >
                                {/* Header */}
                                <div className="flex items-center gap-3 mb-5">
                                    <div className="w-10 h-10 rounded-xl flex items-center justify-center text-xl"
                                        style={{ background: `${proc.color}18`, border: `1px solid ${proc.color}25` }}>
                                        {proc.icon}
                                    </div>
                                    <h3 className="font-bold text-sm" style={{ color: '#f1f5f9' }}>{proc.title}</h3>
                                </div>

                                {/* Steps */}
                                <ol className="space-y-3.5">
                                    {proc.steps.map((step, j) => (
                                        <li key={j} className="flex gap-3">
                                            <div className="step-number flex-shrink-0 w-6 h-6 text-xs"
                                                style={{
                                                    background: `linear-gradient(135deg, ${proc.color}, ${proc.color}99)`,
                                                    boxShadow: `0 4px 12px ${proc.color}30`,
                                                }}>
                                                {j + 1}
                                            </div>
                                            <span className="text-sm leading-relaxed" style={{ color: '#94a3b8' }}>{step}</span>
                                        </li>
                                    ))}
                                </ol>
                            </motion.div>
                        ))}
                    </div>
                </section>

                {/* ── Important Notes ── */}
                <motion.section
                    variants={fadeUp} initial="hidden" whileInView="visible" viewport={{ once: true }}
                    className="rounded-2xl p-7"
                    style={{
                        background: 'rgba(99,102,241,0.06)',
                        border: '1px solid rgba(99,102,241,0.15)',
                    }}
                >
                    <div className="flex items-center gap-2.5 mb-5">
                        <ShieldCheckIcon className="w-5 h-5" style={{ color: '#6366f1' }} />
                        <h3 className="text-lg font-bold" style={{ color: '#f1f5f9' }}>
                            {t('emergency.importantNotesTitle')}
                        </h3>
                    </div>

                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                        {notes.map((note, i) => (
                            <div key={i} className="flex items-start gap-2.5">
                                <CheckCircleIcon className="w-4 h-4 flex-shrink-0 mt-0.5" style={{ color: '#22c55e' }} />
                                <span className="text-sm" style={{ color: '#94a3b8', lineHeight: 1.7 }}>{note}</span>
                            </div>
                        ))}
                    </div>
                </motion.section>

            </div>
        </div>
    );
}
