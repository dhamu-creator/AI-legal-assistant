import React from 'react';
import { ChevronRightIcon, ShieldCheckIcon, ChatBubbleLeftEllipsisIcon, DocumentTextIcon, BookOpenIcon } from '@heroicons/react/24/outline';
import { motion } from 'framer-motion';

export default function Home() {
    const features = [
        {
            icon: ChatBubbleLeftEllipsisIcon,
            title: 'AI Legal Chatbot',
            description: 'Talk to our AI assistant about your legal issues in your native language',
        },
        {
            icon: DocumentTextIcon,
            title: 'FIR Generator',
            description: 'Generate professional FIR and complaint documents automatically',
        },
        {
            icon: ShieldCheckIcon,
            title: 'Legal Guidance',
            description: 'Get step-by-step legal procedures and guidance for your case',
        },
        {
            icon: BookOpenIcon,
            title: 'Legal Knowledge',
            description: 'Access IPC, BNS, and other legal sections relevant to your case',
        },
    ];

    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
            {/* Hero Section */}
            <section className="pt-20 pb-32 px-4 sm:px-6 lg:px-8">
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.8 }}
                    className="max-w-4xl mx-auto text-center"
                >
                    <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-6">
                        AI Legal Assistant for Indian Citizens
                    </h1>
                    <p className="text-xl text-gray-600 mb-8 leading-relaxed">
                        Get instant legal guidance, understand your rights, and generate professional legal documents—
                        all powered by AI and the latest Indian legal references.
                    </p>
                    <motion.button
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                        className="inline-flex items-center px-8 py-3 bg-indigo-600 text-white font-semibold rounded-lg hover:bg-indigo-700 transition"
                    >
                        Start Chatting Now <ChevronRightIcon className="w-5 h-5 ml-2" />
                    </motion.button>
                </motion.div>
            </section>

            {/* Disclaimer */}
            <section className="py-8 px-4 bg-yellow-50 border-l-4 border-yellow-400 mb-12">
                <div className="max-w-4xl mx-auto">
                    <p className="text-sm text-yellow-800">
                        <span className="font-semibold">⚠️ Disclaimer:</span> This AI assistant provides legal information
                        only. It is not a substitute for a licensed advocate. Always consult a legal professional before
                        taking action.
                    </p>
                </div>
            </section>

            {/* Features Section */}
            <section className="py-20 px-4 sm:px-6 lg:px-8">
                <div className="max-w-6xl mx-auto">
                    <h2 className="text-4xl font-bold text-center text-gray-900 mb-16">Features</h2>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
                        {features.map((feature, index) => (
                            <motion.div
                                key={index}
                                initial={{ opacity: 0, y: 20 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ duration: 0.6, delay: index * 0.1 }}
                                className="bg-white rounded-lg shadow-lg p-6 hover:shadow-xl transition"
                            >
                                <feature.icon className="w-12 h-12 text-indigo-600 mb-4" />
                                <h3 className="text-xl font-semibold text-gray-900 mb-2">{feature.title}</h3>
                                <p className="text-gray-600">{feature.description}</p>
                            </motion.div>
                        ))}
                    </div>
                </div>
            </section>

            {/* CTA Section */}
            <section className="py-20 px-4 bg-indigo-600 text-white">
                <div className="max-w-4xl mx-auto text-center">
                    <h2 className="text-4xl font-bold mb-6">Need Legal Help?</h2>
                    <p className="text-lg mb-8 opacity-90">
                        Our AI is available 24/7 to help you understand legal issues and take the right steps.
                    </p>
                    <motion.button
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                        className="px-8 py-3 bg-white text-indigo-600 font-semibold rounded-lg hover:bg-gray-100 transition"
                    >
                        Get Started Now
                    </motion.button>
                </div>
            </section>
        </div>
    );
}
