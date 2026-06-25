import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { motion } from 'framer-motion';
import {
    ChatBubbleLeftEllipsisIcon,
    DocumentTextIcon,
    ShieldCheckIcon,
    BookOpenIcon,
    ArrowRightIcon,
    SparklesIcon,
    CheckCircleIcon,
    ExclamationTriangleIcon,
} from '@heroicons/react/24/outline';

const fadeUp = {
    hidden: { opacity: 0, y: 40 },
    visible: (i = 0) => ({
        opacity: 1,
        y: 0,
        transition: { duration: 0.65, delay: i * 0.12, ease: [0.22, 1, 0.36, 1] },
    }),
};

const trustedBy = ['IPC 2023', 'BNS', 'CrPC', 'IT Act', 'POCSO', 'RTI Act'];

export default function Home() {
    const navigate = useNavigate();
    const { t } = useTranslation();

    const stats = [
        { value: '50,000+', label: t('home.stat1'), icon: '📋' },
        { value: '12,000+', label: t('home.stat2'), icon: '📄' },
        { value: '99.2%',   label: t('home.stat3'), icon: '🎯' },
        { value: '6',       label: t('home.stat4'), icon: '🌐' },
    ];

    const features = [
        {
            icon: ChatBubbleLeftEllipsisIcon,
            title: t('home.featureChatbotTitle'),
            description: t('home.featureChatbotDesc'),
            path: '/chatbot',
            color: '#6366f1',
            tag: 'AI Powered',
        },
        {
            icon: DocumentTextIcon,
            title: t('home.featureFirTitle'),
            description: t('home.featureFirDesc'),
            path: '/fir-generator',
            color: '#d97706',
            tag: 'Auto-Generate',
        },
        {
            icon: ShieldCheckIcon,
            title: t('home.featureGuidanceTitle'),
            description: t('home.featureGuidanceDesc'),
            path: '/chatbot',
            color: '#10b981',
            tag: 'Step-by-Step',
        },
        {
            icon: BookOpenIcon,
            title: t('home.featureKnowledgeTitle'),
            description: t('home.featureKnowledgeDesc'),
            path: '/chatbot',
            color: '#8b5cf6',
            tag: 'IPC + BNS',
        },
    ];

    const howItWorks = [
        { step: '01', title: t('home.step1Title'), desc: t('home.step1Desc') },
        { step: '02', title: t('home.step2Title'), desc: t('home.step2Desc') },
        { step: '03', title: t('home.step3Title'), desc: t('home.step3Desc') },
    ];

    const badges = [
        t('home.badge1'),
        t('home.badge2'),
        t('home.badge3'),
        t('home.badge4'),
    ];

    return (
        <div className="hero-mesh grid-overlay">

            {/* ── HERO SECTION ─────────────────────────────── */}
            <section className="relative overflow-hidden pt-24 pb-32 px-4">
                {/* Ambient orbs */}
                <div className="orb orb-indigo" style={{ width: 600, height: 600, top: -200, left: -150, opacity: 0.5 }} />
                <div className="orb orb-gold" style={{ width: 400, height: 400, bottom: -100, right: -100, opacity: 0.6 }} />

                <div className="max-w-5xl mx-auto text-center relative z-10">
                    {/* Label */}
                    <motion.div variants={fadeUp} initial="hidden" animate="visible" custom={0}>
                        <span className="section-tag">
                            <SparklesIcon className="w-3.5 h-3.5" />
                            {t('home.heroTag')}
                        </span>
                    </motion.div>

                    {/* Headline */}
                    <motion.h1
                        variants={fadeUp} initial="hidden" animate="visible" custom={1}
                        className="text-5xl sm:text-6xl md:text-7xl font-black leading-tight mb-6"
                        style={{ fontFamily: "'Inter', sans-serif", letterSpacing: '-0.03em', color: '#f1f5f9' }}
                    >
                        {t('home.title')}
                    </motion.h1>

                    {/* Subtitle */}
                    <motion.p
                        variants={fadeUp} initial="hidden" animate="visible" custom={2}
                        className="text-lg sm:text-xl mb-10 max-w-2xl mx-auto"
                        style={{ color: '#64748b', lineHeight: '1.75' }}
                    >
                        {t('home.heroSubtitle')}
                    </motion.p>

                    {/* CTA Buttons */}
                    <motion.div
                        variants={fadeUp} initial="hidden" animate="visible" custom={3}
                        className="flex flex-wrap items-center justify-center gap-4 mb-16"
                    >
                        <button
                            onClick={() => navigate('/chatbot')}
                            className="btn-primary text-base px-8 py-3.5"
                        >
                            <span className="flex items-center gap-2 relative z-10">
                                <ChatBubbleLeftEllipsisIcon className="w-5 h-5" />
                                {t('home.ctaChat')}
                                <ArrowRightIcon className="w-4 h-4" />
                            </span>
                        </button>
                        <button
                            onClick={() => navigate('/fir-generator')}
                            className="btn-outline text-base px-8 py-3.5"
                        >
                            <DocumentTextIcon className="w-5 h-5" />
                            {t('home.ctaFir')}
                        </button>
                    </motion.div>

                    {/* Trust row */}
                    <motion.div
                        variants={fadeUp} initial="hidden" animate="visible" custom={4}
                        className="flex flex-wrap items-center justify-center gap-2"
                    >
                        <span className="text-xs font-medium" style={{ color: '#334155' }}>{t('home.trustLabel')}:</span>
                        {trustedBy.map((item) => (
                            <span key={item} className="badge badge-indigo">{item}</span>
                        ))}
                    </motion.div>
                </div>
            </section>

            {/* ── STATS STRIP ──────────────────────────────── */}
            <section className="py-12 px-4" style={{ borderTop: '1px solid rgba(255,255,255,0.04)', borderBottom: '1px solid rgba(255,255,255,0.04)' }}>
                <div className="max-w-5xl mx-auto grid grid-cols-2 md:grid-cols-4 gap-4">
                    {stats.map((stat, i) => (
                        <motion.div
                            key={i}
                            variants={fadeUp} initial="hidden" whileInView="visible" viewport={{ once: true }} custom={i}
                            className="stat-card"
                        >
                            <div className="text-3xl mb-2">{stat.icon}</div>
                            <div className="text-3xl font-black mb-1 gradient-text">{stat.value}</div>
                            <div className="text-xs font-medium" style={{ color: '#64748b' }}>{stat.label}</div>
                        </motion.div>
                    ))}
                </div>
            </section>

            {/* ── DISCLAIMER ───────────────────────────────── */}
            <div className="max-w-5xl mx-auto px-4 py-6">
                <div className="flex items-start gap-3 rounded-xl px-5 py-4"
                    style={{ background: 'rgba(234,179,8,0.06)', border: '1px solid rgba(234,179,8,0.15)' }}>
                    <ExclamationTriangleIcon className="w-5 h-5 mt-0.5 flex-shrink-0" style={{ color: '#ca8a04' }} />
                    <p className="text-sm" style={{ color: '#a16207' }}>
                        <strong style={{ color: '#ca8a04' }}>{t('home.disclaimerLabel')}:</strong>{' '}
                        {t('home.disclaimer')}
                    </p>
                </div>
            </div>

            {/* ── FEATURES GRID ────────────────────────────── */}
            <section className="py-24 px-4">
                <div className="max-w-6xl mx-auto">
                    <motion.div
                        variants={fadeUp} initial="hidden" whileInView="visible" viewport={{ once: true }}
                        className="text-center mb-16"
                    >
                        <span className="section-tag">{t('home.whatWeOffer')}</span>
                        <h2 className="text-4xl md:text-5xl font-black" style={{ color: '#f1f5f9', letterSpacing: '-0.02em' }}>
                            {t('home.featuresTitle')}
                        </h2>
                    </motion.div>

                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
                        {features.map((f, i) => (
                            <motion.div
                                key={i}
                                variants={fadeUp} initial="hidden" whileInView="visible" viewport={{ once: true }} custom={i}
                                onClick={() => navigate(f.path)}
                                className="glass-card rounded-2xl p-6 cursor-pointer group"
                            >
                                {/* Icon */}
                                <div
                                    className="w-12 h-12 rounded-xl flex items-center justify-center mb-5"
                                    style={{ background: `${f.color}18`, border: `1px solid ${f.color}30` }}
                                >
                                    <f.icon className="w-6 h-6" style={{ color: f.color }} />
                                </div>

                                {/* Tag */}
                                <span className="badge mb-3" style={{
                                    background: `${f.color}15`,
                                    color: f.color,
                                    border: `1px solid ${f.color}25`,
                                    fontSize: '0.65rem',
                                }}>
                                    {f.tag}
                                </span>

                                <h3 className="text-lg font-bold mb-2" style={{ color: '#f1f5f9' }}>{f.title}</h3>
                                <p className="text-sm leading-relaxed mb-4" style={{ color: '#64748b' }}>{f.description}</p>

                                <div className="flex items-center gap-1 text-sm font-semibold group-hover:gap-2 transition-all"
                                    style={{ color: f.color }}>
                                    {t('home.exploreLabel')} <ArrowRightIcon className="w-4 h-4" />
                                </div>
                            </motion.div>
                        ))}
                    </div>
                </div>
            </section>

            {/* ── HOW IT WORKS ─────────────────────────────── */}
            <section className="py-24 px-4" style={{ background: 'rgba(99,102,241,0.03)', borderTop: '1px solid rgba(99,102,241,0.06)', borderBottom: '1px solid rgba(99,102,241,0.06)' }}>
                <div className="max-w-5xl mx-auto">
                    <motion.div
                        variants={fadeUp} initial="hidden" whileInView="visible" viewport={{ once: true }}
                        className="text-center mb-16"
                    >
                        <span className="section-tag">{t('home.howItWorksTag')}</span>
                        <h2 className="text-4xl md:text-5xl font-black" style={{ color: '#f1f5f9', letterSpacing: '-0.02em' }}>
                            {t('home.howItWorksTitle')}
                        </h2>
                    </motion.div>

                    <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                        {howItWorks.map((item, i) => (
                            <motion.div
                                key={i}
                                variants={fadeUp} initial="hidden" whileInView="visible" viewport={{ once: true }} custom={i}
                                className="relative"
                            >
                                <div className="glass-card rounded-2xl p-7">
                                    <div className="text-5xl font-black mb-4" style={{ color: 'rgba(99,102,241,0.15)', lineHeight: 1 }}>
                                        {item.step}
                                    </div>
                                    <h3 className="text-xl font-bold mb-3" style={{ color: '#f1f5f9' }}>{item.title}</h3>
                                    <p className="text-sm leading-relaxed" style={{ color: '#64748b' }}>{item.desc}</p>
                                </div>
                                {i < 2 && (
                                    <div className="hidden md:block absolute top-1/2 -right-4 text-slate-700 z-10">
                                        <ArrowRightIcon className="w-6 h-6" />
                                    </div>
                                )}
                            </motion.div>
                        ))}
                    </div>
                </div>
            </section>

            {/* ── CTA SECTION ──────────────────────────────── */}
            <section className="py-28 px-4">
                <div className="max-w-4xl mx-auto">
                    <motion.div
                        variants={fadeUp} initial="hidden" whileInView="visible" viewport={{ once: true }}
                        className="rounded-3xl overflow-hidden relative"
                        style={{
                            background: 'linear-gradient(135deg, rgba(79,70,229,0.25) 0%, rgba(217,119,6,0.15) 100%)',
                            border: '1px solid rgba(99,102,241,0.2)',
                            padding: '4rem 3rem',
                            textAlign: 'center',
                        }}
                    >
                        {/* Glow */}
                        <div className="orb orb-indigo" style={{ width: 300, height: 300, top: -100, right: -100, opacity: 0.4 }} />

                        <span className="section-tag relative z-10">{t('home.ctaTag')}</span>
                        <h2 className="text-4xl md:text-5xl font-black mb-5 relative z-10" style={{ color: '#f1f5f9', letterSpacing: '-0.02em' }}>
                            {t('home.needHelp')}
                        </h2>
                        <p className="text-lg mb-8 relative z-10" style={{ color: '#64748b', maxWidth: '28rem', margin: '0 auto 2.5rem' }}>
                            {t('home.needHelpSub')}
                        </p>

                        <div className="flex flex-wrap gap-4 justify-center relative z-10">
                            <button onClick={() => navigate('/chatbot')} className="btn-primary px-10 py-4 text-base">
                                <span className="flex items-center gap-2 relative z-10">
                                    <SparklesIcon className="w-5 h-5" />
                                    {t('home.getStarted')}
                                </span>
                            </button>
                            <button onClick={() => navigate('/emergency')} className="btn-outline px-10 py-4 text-base"
                                style={{ borderColor: 'rgba(239,68,68,0.3)', color: '#fca5a5' }}>
                                <ExclamationTriangleIcon className="w-5 h-5" />
                                {t('home.emergencyBtn')}
                            </button>
                        </div>

                        {/* Checklist */}
                        <div className="flex flex-wrap justify-center gap-5 mt-10 relative z-10">
                            {badges.map((item) => (
                                <div key={item} className="flex items-center gap-1.5 text-sm" style={{ color: '#475569' }}>
                                    <CheckCircleIcon className="w-4 h-4" style={{ color: '#22c55e' }} />
                                    {item}
                                </div>
                            ))}
                        </div>
                    </motion.div>
                </div>
            </section>
        </div>
    );
}
