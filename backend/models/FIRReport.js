import mongoose from 'mongoose';

const firReportSchema = new mongoose.Schema(
    {
        userId: {
            type: mongoose.Schema.Types.ObjectId,
            ref: 'User',
            required: true,
        },
        title: {
            type: String,
            required: true,
        },
        incidentDetails: {
            type: String,
            required: true,
        },
        incidentDate: Date,
        incidentLocation: String,
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
        },
        ipcSections: [String],
        bnsSections: [String],
        complainantDetails: {
            name: String,
            phone: String,
            address: String,
            email: String,
        },
        suspectDetails: {
            name: String,
            description: String,
            address: String,
        },
        witnessDetails: [
            {
                name: String,
                phone: String,
                statement: String,
            },
        ],
        evidence: [String],
        firDraft: String,
        submittedAt: Date,
        status: {
            type: String,
            enum: ['draft', 'submitted', 'filed'],
            default: 'draft',
        },
        language: {
            type: String,
            enum: ['en', 'ta', 'hi', 'te', 'ml', 'ka'],
            default: 'en',
        },
    },
    { timestamps: true }
);

const FIRReport = mongoose.model('FIRReport', firReportSchema);
export default FIRReport;
