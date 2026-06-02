import express from 'express';

const router = express.Router();

/**
 * Legal Information Routes
 */

// Get supported languages
router.get('/languages', (req, res) => {
    const languages = {
        en: { name: 'English', nativeName: 'English' },
        ta: { name: 'Tamil', nativeName: 'தமிழ்' },
        hi: { name: 'Hindi', nativeName: 'हिन्दी' },
        te: { name: 'Telugu', nativeName: 'తెలుగు' },
        ml: { name: 'Malayalam', nativeName: 'മലയാളം' },
        ka: { name: 'Kannada', nativeName: 'ಕನ್ನಡ' },
    };
    res.status(200).json({
        success: true,
        data: languages,
    });
});

// Get crime categories
router.get('/crime-categories', (req, res) => {
    const categories = [
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
    res.status(200).json({
        success: true,
        data: categories,
    });
});

// Get legal disclaimer
router.get('/disclaimer', (req, res) => {
    res.status(200).json({
        success: true,
        data: {
            disclaimer: `This AI assistant provides legal information and guidance only. It is not a substitute for a licensed advocate. 
            
            The information provided is for educational purposes only. Before taking any legal action, please consult with a qualified legal professional. 
            
            We are not responsible for any consequences arising from the use of this information.`,
        },
    });
});

// Get emergency contacts
router.get('/emergency-contacts', (req, res) => {
    const contacts = {
        police: '100',
        women_safety: '1091',
        cyber_crime: '1930',
        childline: '1098',
        emergency: '112',
    };
    res.status(200).json({
        success: true,
        data: contacts,
    });
});

export default router;
