import mongoose from 'mongoose';

const legalDocumentSchema = new mongoose.Schema(
    {
        title: {
            type: String,
            required: true,
        },
        type: {
            type: String,
            enum: ['IPC', 'BNS', 'BNSS', 'BSA', 'CyberLaw', 'ConsumerLaw', 'Judgment'],
            required: true,
        },
        content: {
            type: String,
            required: true,
        },
        sectionNumber: String,
        explanation: {
            en: String,
            ta: String,
            hi: String,
            te: String,
            ml: String,
            ka: String,
        },
        punishment: String,
        rights: [String],
        relatedSections: [String],
        keyWords: [String],
        embedding: [Number], // For vector search
        source: String,
        year: Number,
    },
    { timestamps: true }
);

// Add index for efficient searching
legalDocumentSchema.index({ keyWords: 1, type: 1 });
legalDocumentSchema.index({ sectionNumber: 1 });

const LegalDocument = mongoose.model('LegalDocument', legalDocumentSchema);
export default LegalDocument;
