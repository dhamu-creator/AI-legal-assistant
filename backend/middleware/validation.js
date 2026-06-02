// Input Validation Middleware
export const validateChatMessage = (req, res, next) => {
    const { message } = req.body;

    if (!message || typeof message !== 'string') {
        return res.status(400).json({
            success: false,
            message: 'Invalid message format',
        });
    }

    if (message.trim().length === 0 || message.length > 5000) {
        return res.status(400).json({
            success: false,
            message: 'Message must be between 1 and 5000 characters',
        });
    }

    // Sanitize input to prevent injection attacks
    req.body.message = message.trim();
    next();
};

export const validateFIRReport = (req, res, next) => {
    const { incidentDetails, crimeCategory, complainantDetails } = req.body;

    if (!incidentDetails || !crimeCategory || !complainantDetails) {
        return res.status(400).json({
            success: false,
            message: 'Missing required FIR fields',
        });
    }

    const validCategories = [
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

    if (!validCategories.includes(crimeCategory)) {
        return res.status(400).json({
            success: false,
            message: 'Invalid crime category',
        });
    }

    next();
};

export const validateLanguage = (req, res, next) => {
    const { language } = req.body;
    const validLanguages = ['en', 'ta', 'hi', 'te', 'ml', 'ka'];

    if (language && !validLanguages.includes(language)) {
        return res.status(400).json({
            success: false,
            message: 'Invalid language code',
        });
    }

    next();
};
