import mongoose from 'mongoose';

const evidenceChecklistSchema = new mongoose.Schema({
    crimeCategory: {
        type: String,
        enum: [
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
        ],
        required: true,
        unique: true,
    },
    items: [
        {
            name: String,
            description: String,
            importance: {
                type: String,
                enum: ['critical', 'important', 'helpful'],
                default: 'important',
            },
        },
    ],
    procedureSteps: [String],
    emergencyContacts: [
        {
            name: String,
            number: String,
            description: String,
        },
    ],
});

const EvidenceChecklist = mongoose.model('EvidenceChecklist', evidenceChecklistSchema);
export default EvidenceChecklist;
