import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

// English translations
const enTranslations = {
    translation: {
        home: {
            title: 'AI Legal Assistant for Indian Citizens',
            subtitle: 'Get instant legal guidance, understand your rights, and generate professional legal documents.',
            disclaimer: 'This AI assistant provides legal information only. It is not a substitute for a licensed advocate.',
            getStarted: 'Get Started Now',
        },
        chatbot: {
            title: 'AI Legal Assistant',
            placeholder: 'Describe your legal issue...',
            send: 'Send',
            welcome: 'Welcome to AI Legal Assistant',
            examples: 'Examples:',
            example1: 'My phone was stolen in a bus stand',
            example2: 'I received a threatening call from an unknown number',
            example3: 'How do I file a police complaint?',
        },
        fir: {
            title: 'FIR/Complaint Generator',
            subtitle: 'Generate a professional FIR (First Information Report) or complaint',
            incidentDetails: 'Incident Details',
            yourDetails: 'Your Details',
            additionalDetails: 'Additional Details',
            crimeCategory: 'Crime Category',
            selectCategory: 'Select a crime category',
        },
    },
};

// Tamil translations
const taTranslations = {
    translation: {
        home: {
            title: 'இந்திய குடிமக்களுக்கான AI சட்ட உதவி',
            subtitle: 'உடனடி சட்ட வழிகாட்டுதல் பெறவும், உங்கள் உரிமைகளைப் புரிந்து கொள்ளவும்.',
            disclaimer: 'இந்த AI உதவி சட்ட தகவல் மட்டுமே வழங்குகிறது. இது ஒரு தகுதிவாய்ந்த வழக்கறிஞருக்கு அபராதம் அல்ல.',
            getStarted: 'இப்போது தொடங்கவும்',
        },
        chatbot: {
            title: 'AI சட்ட உதவி',
            placeholder: 'உங்கள் சட்ட சிக்கலை விவரிக்கவும்...',
            send: 'அனுப்பு',
        },
    },
};

// Hindi translations
const hiTranslations = {
    translation: {
        home: {
            title: 'भारतीय नागरिकों के लिए AI कानूनी सहायता',
            subtitle: 'तत्काल कानूनी मार्गदर्शन प्राप्त करें और अपने अधिकारों को समझें।',
            disclaimer: 'यह AI केवल कानूनी जानकारी प्रदान करता है। यह एक योग्य वकील का विकल्प नहीं है।',
            getStarted: 'अभी शुरू करें',
        },
        chatbot: {
            title: 'AI कानूनी सहायता',
            placeholder: 'अपनी कानूनी समस्या का वर्णन करें...',
            send: 'भेजें',
        },
    },
};

i18n.use(initReactI18next).init({
    resources: {
        en: enTranslations,
        ta: taTranslations,
        hi: hiTranslations,
    },
    lng: 'en',
    interpolation: {
        escapeValue: false,
    },
});

export default i18n;
