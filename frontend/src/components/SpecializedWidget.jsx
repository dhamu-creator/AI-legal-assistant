import React from 'react';
import { motion } from 'framer-motion';
import { 
    ExclamationTriangleIcon, 
    ShieldCheckIcon, 
    DocumentTextIcon,
    ExclamationCircleIcon,
    ScaleIcon,
    CheckCircleIcon,
    BookOpenIcon,
    ClockIcon,
    CheckBadgeIcon,
    ServerStackIcon,
    MagnifyingGlassIcon
} from '@heroicons/react/24/outline';

export default function SpecializedWidget({ msg }) {
    if (!msg) return null;

    const { crimeCategory, agentData, legal, timeline, evidence, api_integration, severity } = msg;

    // We'll collect all rendered widgets into an array so we can stagger their animations.
    const widgets = [];

    // --- 1. EXTERNAL API INTEGRATION (Mock CCTNS or Cyber Registry) ---
    if (api_integration) {
        if (api_integration.tracking_id) {
            widgets.push(
                <WidgetCard key="api-fir" title="e-FIR Portal Integration" subtitle="Mock CCTNS Transmission" icon={<ServerStackIcon className="w-5 h-5 text-indigo-400" />} colorClass="border-indigo-500/30 bg-slate-900/60" headerBg="bg-indigo-500/10">
                    <div className="flex items-center gap-3 bg-indigo-500/5 border border-indigo-500/20 p-3 rounded-lg">
                        <CheckBadgeIcon className="w-8 h-8 text-indigo-400 flex-shrink-0" />
                        <div>
                            <p className="text-xs text-indigo-200">FIR successfully transmitted to Mock Database.</p>
                            <p className="text-sm font-mono font-bold text-white mt-1">Tracking ID: {api_integration.tracking_id}</p>
                        </div>
                    </div>
                </WidgetCard>
            );
        } else if (api_integration.registry) {
            const entities = Object.entries(api_integration.results || {});
            if (entities.length > 0) {
                widgets.push(
                    <WidgetCard key="api-fraud" title="National Cyber Registry Scan" subtitle="Entity Risk Analysis" icon={<MagnifyingGlassIcon className="w-5 h-5 text-rose-400" />} colorClass="border-rose-500/30 bg-slate-900/60" headerBg="bg-rose-500/10">
                        <div className="space-y-3">
                            {entities.map(([entity, data], idx) => (
                                <div key={idx} className="bg-rose-500/5 border border-rose-500/20 p-3 rounded-lg flex items-center justify-between">
                                    <div className="truncate pr-4">
                                        <p className="text-xs text-rose-200/70 mb-0.5">Scanned Entity</p>
                                        <p className="text-sm font-bold text-rose-100 truncate">{entity}</p>
                                    </div>
                                    <div className="text-right">
                                        <p className="text-xs text-rose-200/70 mb-0.5">Risk Score</p>
                                        <p className={`text-sm font-black ${data.risk_score > 70 ? 'text-red-500' : data.risk_score > 40 ? 'text-amber-500' : 'text-emerald-500'}`}>
                                            {data.risk_score}/100
                                        </p>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </WidgetCard>
                );
            }
        }
    }

    // --- 2. RAG LEGAL CONTEXT ---
    if (legal && legal.retrieved_sections && legal.retrieved_sections.length > 0) {
        widgets.push(
            <WidgetCard key="rag-legal" title="Legal Knowledge Base" subtitle="Retrieved from ChromaDB" icon={<BookOpenIcon className="w-5 h-5 text-sky-400" />} colorClass="border-sky-500/30 bg-slate-900/60" headerBg="bg-sky-500/10">
                <div className="space-y-2">
                    {legal.retrieved_sections.slice(0, 3).map((sec, idx) => (
                        <div key={idx} className="p-3 bg-sky-900/10 border border-sky-500/20 rounded-lg">
                            <h5 className="text-xs font-bold text-sky-300 mb-1 flex items-center gap-2">
                                <span>§ {sec.metadata?.law || 'BNS'} Section {sec.metadata?.section || ''}</span>
                                {sec.metadata?.score && <span className="text-[10px] bg-sky-500/20 px-1.5 py-0.5 rounded text-sky-200">Relevance: {(sec.metadata.score).toFixed(2)}</span>}
                            </h5>
                            <p className="text-xs text-slate-300 line-clamp-3 leading-relaxed">{sec.content}</p>
                        </div>
                    ))}
                </div>
            </WidgetCard>
        );
    }

    // --- 3. SEVERITY / URGENCY (Agentic System override) ---
    if (severity && severity.severity) {
        const isCritical = severity.severity === 'Critical' || severity.severity === 'High';
        widgets.push(
            <WidgetCard key="severity" title="Incident Severity Analysis" subtitle="AI Risk Assessment" icon={isCritical ? <ExclamationTriangleIcon className="w-5 h-5 text-red-400" /> : <ExclamationCircleIcon className="w-5 h-5 text-amber-400" />} colorClass={isCritical ? 'border-red-500/30 bg-slate-900/60' : 'border-amber-500/30 bg-slate-900/60'} headerBg={isCritical ? 'bg-red-500/10' : 'bg-amber-500/10'}>
                <div className="flex items-center gap-4 mb-3">
                    <div className="flex-1">
                        <div className="w-full h-2 bg-slate-800 rounded-full overflow-hidden">
                            <motion.div initial={{ width: 0 }} animate={{ width: `${severity.score || 0}%` }} transition={{ duration: 1, ease: 'easeOut' }} className={`h-full rounded-full ${isCritical ? 'bg-gradient-to-r from-red-600 to-red-400' : 'bg-gradient-to-r from-amber-600 to-amber-400'}`} />
                        </div>
                    </div>
                    <span className={`text-xs font-black ${isCritical ? 'text-red-400' : 'text-amber-400'}`}>{severity.severity} RISK</span>
                </div>
                {severity.urgency && (
                    <div className={`text-xs p-2 rounded ${isCritical ? 'bg-red-500/10 text-red-200 border border-red-500/20' : 'bg-amber-500/10 text-amber-200 border border-amber-500/20'}`}>
                        <strong>Action Required:</strong> {severity.urgency}
                    </div>
                )}
            </WidgetCard>
        );
    }

    // --- 4. LEGAL TIMELINE ---
    if (timeline && timeline.timeline_steps) {
        widgets.push(
            <WidgetCard key="timeline" title="Legal Timeline" subtitle="Procedural Steps" icon={<ClockIcon className="w-5 h-5 text-emerald-400" />} colorClass="border-emerald-500/30 bg-slate-900/60" headerBg="bg-emerald-500/10">
                <div className="relative pl-3 border-l-2 border-emerald-500/20 space-y-4 my-2 ml-2">
                    {timeline.timeline_steps.map((step, idx) => (
                        <div key={idx} className="relative">
                            <div className="absolute -left-[19px] top-1 w-3 h-3 rounded-full bg-emerald-500 border-2 border-slate-900 shadow-[0_0_8px_rgba(16,185,129,0.6)]" />
                            <h5 className="text-xs font-bold text-emerald-300">{step.phase}</h5>
                            <p className="text-xs text-slate-300 mt-0.5 leading-relaxed">{step.description}</p>
                            {step.estimated_duration && (
                                <span className="inline-block mt-1 text-[10px] text-emerald-400/80 bg-emerald-500/10 px-1.5 py-0.5 rounded">ETA: {step.estimated_duration}</span>
                            )}
                        </div>
                    ))}
                </div>
            </WidgetCard>
        );
    }

    // --- 5. EVIDENCE CHECKLIST ---
    if (evidence && evidence.evidence) {
        widgets.push(
            <WidgetCard key="evidence" title="Required Evidence" subtitle="Preservation Checklist" icon={<DocumentTextIcon className="w-5 h-5 text-fuchsia-400" />} colorClass="border-fuchsia-500/30 bg-slate-900/60" headerBg="bg-fuchsia-500/10">
                <ul className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                    {evidence.evidence.map((item, idx) => (
                        <li key={idx} className="flex items-start gap-2 bg-fuchsia-500/5 border border-fuchsia-500/10 p-2 rounded">
                            <CheckCircleIcon className="w-3.5 h-3.5 text-fuchsia-400 mt-0.5 flex-shrink-0" />
                            <span className="text-xs text-slate-200">{item}</span>
                        </li>
                    ))}
                </ul>
            </WidgetCard>
        );
    }

    // If no widgets were built, fallback to old agentData rendering logic just in case
    if (widgets.length === 0 && agentData) {
        if (agentData.scam_detection) {
            widgets.push(
                <WidgetCard key="old-scam" title="Scam Detection" subtitle="Risk Analysis" icon={<ExclamationTriangleIcon className="w-5 h-5 text-amber-400" />} colorClass="border-amber-500/30 bg-slate-900/60" headerBg="bg-amber-500/10">
                    <div className="text-xs text-slate-300">Risk Level: {agentData.scam_detection.risk_level}</div>
                </WidgetCard>
            );
        }
        if (agentData.missing_person_checklist) {
            widgets.push(
                <WidgetCard key="old-missing" title="Missing Person Action Plan" subtitle="Emergency Steps" icon={<ShieldCheckIcon className="w-5 h-5 text-purple-400" />} colorClass="border-purple-500/30 bg-slate-900/60" headerBg="bg-purple-500/10">
                    <ul className="space-y-1">
                        {agentData.missing_person_checklist.emergency_steps?.map((s, i) => (
                            <li key={i} className="text-xs text-slate-300 flex items-start gap-2"><CheckCircleIcon className="w-3 h-3 text-purple-400 mt-0.5" />{s}</li>
                        ))}
                    </ul>
                </WidgetCard>
            );
        }
    }

    if (widgets.length === 0) return null;

    return (
        <div className="flex flex-col gap-3 mt-4 w-full">
            {widgets.map((widget, index) => (
                <motion.div
                    key={widget.key}
                    initial={{ opacity: 0, y: 15 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.4, delay: index * 0.1, ease: "easeOut" }}
                >
                    {widget}
                </motion.div>
            ))}
        </div>
    );
}

function WidgetCard({ title, subtitle, icon, colorClass, headerBg, children }) {
    return (
        <div className={`rounded-xl overflow-hidden backdrop-blur-md shadow-lg ${colorClass}`}>
            <div className={`px-4 py-3 flex items-center gap-3 ${headerBg}`}>
                <div className="p-1.5 rounded-lg bg-white/5 backdrop-blur-sm border border-white/10">
                    {icon}
                </div>
                <div>
                    <h4 className="text-sm font-bold text-white tracking-wide">{title}</h4>
                    {subtitle && <p className="text-[10px] uppercase tracking-wider text-slate-400 font-semibold">{subtitle}</p>}
                </div>
            </div>
            <div className="p-4">
                {children}
            </div>
        </div>
    );
}
