import React from 'react';
import { PhoneIcon, ExclamationTriangleIcon, MapPinIcon } from '@heroicons/react/24/outline';

export default function EmergencyHelp() {
    const emergencyContacts = [
        { name: 'Police Emergency', number: '100', description: 'General police emergency' },
        { name: 'Women Helpline', number: '1091', description: 'Women safety and support' },
        { name: 'Cybercrime Helpline', number: '1930', description: 'Online fraud and cyber crimes' },
        { name: 'Childline', number: '1098', description: 'Child safety and protection' },
        { name: 'Unified Emergency', number: '112', description: 'All emergencies' },
    ];

    const procedures = [
        {
            title: 'If Police Refuse to File FIR',
            steps: [
                'Ask for written refusal with reasons',
                'Contact the Station House Officer (SHO)',
                'File a complaint with District Superintendent',
                'Contact State Legal Services Authority',
                'Approach High Court if necessary',
            ],
        },
        {
            title: 'Steps to File a Police Complaint',
            steps: [
                'Visit nearest police station',
                'Speak to duty officer',
                'Provide detailed incident information',
                'Get FIR copy and acknowledgment',
                'Keep all documents safe',
            ],
        },
        {
            title: 'Cybercrime Reporting',
            steps: [
                'Visit cybercrime.gov.in portal',
                'File complaint online',
                'Provide evidence (screenshots, transaction details)',
                'Keep reference number',
                'Follow up with local police if needed',
            ],
        },
    ];

    return (
        <div className="min-h-screen bg-gray-50 py-12 px-4">
            <div className="max-w-6xl mx-auto">
                {/* Header */}
                <div className="mb-12">
                    <h1 className="text-4xl font-bold text-gray-900 mb-2 flex items-center gap-2">
                        <ExclamationTriangleIcon className="w-8 h-8 text-red-600" />
                        Emergency Help & Legal Procedures
                    </h1>
                    <p className="text-gray-600">Important contacts and step-by-step guidance for legal issues</p>
                </div>

                {/* Emergency Contacts */}
                <section className="mb-12">
                    <h2 className="text-3xl font-bold text-gray-900 mb-6">Emergency Contacts</h2>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
                        {emergencyContacts.map((contact, index) => (
                            <div key={index} className="bg-white rounded-lg shadow p-6 hover:shadow-lg transition">
                                <div className="flex items-center gap-3 mb-3">
                                    <PhoneIcon className="w-6 h-6 text-red-600" />
                                    <span className="text-2xl font-bold text-red-600">{contact.number}</span>
                                </div>
                                <h3 className="font-semibold text-gray-900 mb-1">{contact.name}</h3>
                                <p className="text-sm text-gray-600">{contact.description}</p>
                            </div>
                        ))}
                    </div>
                </section>

                {/* Procedures */}
                <section>
                    <h2 className="text-3xl font-bold text-gray-900 mb-6">Legal Procedures</h2>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        {procedures.map((procedure, index) => (
                            <div key={index} className="bg-white rounded-lg shadow p-6">
                                <h3 className="text-xl font-bold text-gray-900 mb-4">{procedure.title}</h3>
                                <ol className="space-y-3">
                                    {procedure.steps.map((step, stepIndex) => (
                                        <li key={stepIndex} className="flex gap-3">
                                            <span className="flex-shrink-0 w-6 h-6 bg-indigo-600 text-white rounded-full flex items-center justify-center text-sm font-semibold">
                                                {stepIndex + 1}
                                            </span>
                                            <span className="text-gray-700">{step}</span>
                                        </li>
                                    ))}
                                </ol>
                            </div>
                        ))}
                    </div>
                </section>

                {/* Important Notes */}
                <section className="mt-12 bg-blue-50 border border-blue-200 rounded-lg p-6">
                    <h3 className="text-xl font-bold text-blue-900 mb-4">Important Notes</h3>
                    <ul className="space-y-2 text-blue-800">
                        <li>✓ You have the right to file an FIR without being turned away</li>
                        <li>✓ Get written acknowledgment of your complaint</li>
                        <li>✓ Keep all documents and reference numbers</li>
                        <li>✓ You can request a copy of the FIR after filing</li>
                        <li>✓ Consult a lawyer for serious crimes</li>
                        <li>✓ Legal aid is available for those who cannot afford lawyers</li>
                    </ul>
                </section>
            </div>
        </div>
    );
}
