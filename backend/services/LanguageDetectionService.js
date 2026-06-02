/**
 * Language Detection Service
 * Detects user language using Unicode character patterns
 * No external dependencies needed - pure character analysis
 */

class LanguageDetectionService {
    /**
     * Detect language from text using Unicode patterns
     */
    async detectLanguage(text) {
        // Tamil Unicode range: 0x0B80 - 0x0BFF
        // Hindi Unicode range: 0x0900 - 0x097F
        // Telugu Unicode range: 0x0C00 - 0x0C7F
        // Malayalam Unicode range: 0x0D00 - 0x0D7F
        // Kannada Unicode range: 0x0C80 - 0x0CFF

        const tamsilRegex = /[\u0B80-\u0BFF]/g;
        const hindiRegex = /[\u0900-\u097F]/g;
        const teluguRegex = /[\u0C00-\u0C7F]/g;
        const malayalamRegex = /[\u0D00-\u0D7F]/g;
        const kannadaRegex = /[\u0C80-\u0CFF]/g;

        const tamilMatches = text.match(tamsilRegex) || [];
        const hindiMatches = text.match(hindiRegex) || [];
        const teluguMatches = text.match(teluguRegex) || [];
        const malayalamMatches = text.match(malayalamRegex) || [];
        const kannadaMatches = text.match(kannadaRegex) || [];

        const detections = {
            ta: tamilMatches.length,
            hi: hindiMatches.length,
            te: teluguMatches.length,
            ml: malayalamMatches.length,
            ka: kannadaMatches.length,
        };

        // Find language with most characters
        let maxLanguage = 'en';
        let maxCount = 0;

        for (const [lang, count] of Object.entries(detections)) {
            if (count > maxCount) {
                maxCount = count;
                maxLanguage = lang;
            }
        }

        // If significant Indian script detected, return that language
        if (maxCount > text.length * 0.1) {
            return maxLanguage;
        }

        return 'en'; // Default to English
    }

    /**
     * Get all supported languages
     */
    getSupportedLanguages() {
        return {
            en: { name: 'English', nativeName: 'English' },
            ta: { name: 'Tamil', nativeName: 'தமிழ்' },
            hi: { name: 'Hindi', nativeName: 'हिन्दी' },
            te: { name: 'Telugu', nativeName: 'తెలుగు' },
            ml: { name: 'Malayalam', nativeName: 'മലയാളം' },
            ka: { name: 'Kannada', nativeName: 'ಕನ್ನಡ' },
        };
    }

    /**
     * Get language code from name
     */
    getLanguageCode(languageName) {
        const mapping = {
            english: 'en',
            tamil: 'ta',
            hindi: 'hi',
            telugu: 'te',
            malayalam: 'ml',
            kannada: 'ka',
        };
        return mapping[languageName.toLowerCase()] || 'en';
    }
}

export default new LanguageDetectionService();
