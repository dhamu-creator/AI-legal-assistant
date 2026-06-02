import axios from 'axios';
import dotenv from 'dotenv';

dotenv.config();

class AIService {
    constructor() {
        this.pythonBackendURL = process.env.PYTHON_BACKEND_URL || 'http://localhost:8000';

        // If TEST_MODE is enabled, do not initialize external Gemini client
        this.testMode = process.env.TEST_MODE === 'true' || false;
        if (!this.testMode) {
            if (!process.env.GEMINI_API_KEY) {
                console.warn('GEMINI_API_KEY not set — enabling TEST_MODE');
                this.testMode = true;
            } else {
                // Try dynamic import; if it fails, fall back to test mode
                import('@google/generative-ai')
                    .then((mod) => {
                        try {
                            const GoogleGenerativeAI = mod.GoogleGenerativeAI;
                            this.geminiClient = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);
                            this.model = this.geminiClient.getGenerativeModel({ model: 'gemini-1.5-flash' });
                        } catch (e) {
                            console.warn('Failed to initialize generative client, enabling TEST_MODE', e.message);
                            this.testMode = true;
                        }
                    })
                    .catch((err) => {
                        console.warn('Generative AI package not available — enabling TEST_MODE', err.message);
                        this.testMode = true;
                    });
            }
        }
    }


    /**
     * Analyze incident and detect crime category
     */
    async analyzeCrimeCategory(incidentDescription, language = 'en') {
        try {
            if (this.testMode) {
                // Simple deterministic mock based on keywords
                const text = incidentDescription.toLowerCase();
                let category = 'Theft';
                if (text.includes('hack') || text.includes('bank') || text.includes('online')) category = 'CyberFraud';
                if (text.includes('domestic') || text.includes('husband') || text.includes('wife')) category = 'DomesticViolence';
                if (text.includes('assault') || text.includes('beat')) category = 'PhysicalAssault';
                return {
                    category,
                    ipcSections: ['379'],
                    bnsSections: [],
                    confidence: 0.8,
                    explanation: 'Mocked response for tests',
                };
            }
            const prompt = `
You are an expert legal AI assistant for Indian law.

Analyze this incident: "${incidentDescription}"

Identify the primary crime category from these options:
- Theft
- Robbery
- CyberFraud
- Harassment
- DomesticViolence
- Blackmail
- OnlineScams
- IdentityTheft
- FinancialFraud
- PhysicalAssault

Also identify relevant IPC sections (like 379, 380, 420, etc.) and BNS sections.

Return ONLY valid JSON:
{
  "category": "CrimeCategory",
  "ipcSections": ["section1", "section2"],
  "bnsSections": ["section1", "section2"],
  "confidence": 0.9,
  "explanation": "Brief explanation"
}
`;

            const result = await this.model.generateContent(prompt);
            const responseText = result.response.text();
            
            // Parse JSON from response
            const jsonMatch = responseText.match(/\{[\s\S]*\}/);
            if (!jsonMatch) {
                throw new Error('Invalid response format');
            }

            return JSON.parse(jsonMatch[0]);
        } catch (error) {
            console.error('Error in analyzeCrimeCategory:', error);
            throw new Error('Failed to analyze crime category');
        }
    }

    /**
     * Generate legal guidance for the incident
     */
    async generateLegalGuidance(incidentDetails, crimeCategory, language = 'en') {
        try {
            if (this.testMode) {
                return `Mock guidance for ${crimeCategory}: This is a test-only response. Contact local police and preserve evidence.`;
            }
            const prompt = `
You are an expert legal AI assistant for Indian law. Provide clear, simple legal guidance in ${this.getLanguageName(language)}.

Incident: ${incidentDetails}
Crime Category: ${crimeCategory}

Provide guidance covering:
1. What this crime means legally
2. Rights of the victim
3. Steps to file a complaint/FIR
4. Police procedure
5. Legal remedies available
6. Important documents needed
7. Timeline for resolution
8. Emergency contacts if needed

Format your response in clear sections.
DISCLAIMER: This is for information only. Consult a lawyer for specific advice.
`;

            const result = await this.model.generateContent(prompt);
            return result.response.text();
        } catch (error) {
            console.error('Error in generateLegalGuidance:', error);
            throw new Error('Failed to generate legal guidance');
        }
    }

    /**
     * Generate FIR/Complaint draft
     */
    async generateFIRDraft(firData, language = 'en') {
        try {
            if (this.testMode) {
                return `FIR Draft (mock): Complainant: ${firData.complainantDetails?.name || 'N/A'}. Incident: ${firData.incidentDetails || 'N/A'}`;
            }
            const { complainantDetails, incidentDetails, incidentDate, incidentLocation, suspectDetails, evidence } = firData;

            const prompt = `
Generate a professional FIR (First Information Report) draft in ${this.getLanguageName(language)} with this information:

Complainant: ${complainantDetails.name}, Phone: ${complainantDetails.phone}, Address: ${complainantDetails.address}

Incident Details: ${incidentDetails}
Date: ${incidentDate}
Location: ${incidentLocation}

Suspect: ${suspectDetails?.name || 'Unknown'}, Description: ${suspectDetails?.description || 'Not provided'}

Evidence: ${evidence?.join(', ') || 'To be collected'}

Format as a professional FIR that can be submitted to police.
Include all required sections.
Keep language simple but formal.
`;

            const result = await this.model.generateContent(prompt);
            return result.response.text();
        } catch (error) {
            console.error('Error in generateFIRDraft:', error);
            throw new Error('Failed to generate FIR draft');
        }
    }

    /**
     * Get evidence checklist for crime category
     */
    async getEvidenceChecklist(crimeCategory, language = 'en') {
        try {
            if (this.testMode) {
                return {
                    items: [
                        { name: 'Mock Evidence', description: 'Test evidence', importance: 'important' },
                    ],
                    procedureSteps: ['Mock step 1', 'Mock step 2'],
                    emergencyContacts: [{ name: 'Police', number: '100' }],
                };
            }
            const prompt = `
For a ${crimeCategory} case in India, provide a detailed evidence checklist in ${this.getLanguageName(language)}.

Include:
1. Critical evidence items
2. Important supporting documents
3. Procedural steps to collect evidence
4. Emergency contacts
5. Important legal references

Format as JSON:
{
  "items": [
    {"name": "Evidence name", "description": "Why it's needed", "importance": "critical|important|helpful"}
  ],
  "procedureSteps": ["Step 1", "Step 2", ...],
  "emergencyContacts": [{"name": "Agency name", "number": "Phone number"}]
}
`;

            const result = await this.model.generateContent(prompt);
            const jsonMatch = result.response.text().match(/\{[\s\S]*\}/);
            if (!jsonMatch) {
                throw new Error('Invalid response format');
            }
            return JSON.parse(jsonMatch[0]);
        } catch (error) {
            console.error('Error in getEvidenceChecklist:', error);
            throw new Error('Failed to get evidence checklist');
        }
    }

    /**
     * Call Python RAG backend for document retrieval
     */
    async queryRAGPipeline(query, language = 'en') {
        try {
            const response = await axios.post(`${this.pythonBackendURL}/api/rag/query`, {
                query,
                language,
            });
            return response.data;
        } catch (error) {
            console.error('Error connecting to Python RAG backend:', error);
            throw new Error('Failed to retrieve legal documents');
        }
    }

    /**
     * Translate text using Gemini
     */
    async translateText(text, targetLanguage) {
        try {
            if (targetLanguage === 'en') return text;
            if (this.testMode) return `[${targetLanguage} translation] ${text}`;

            const prompt = `Translate this legal text to ${this.getLanguageName(targetLanguage)}. Preserve all legal terms and formatting.

Text: ${text}

Provide ONLY the translation, no explanations.`;

            const result = await this.model.generateContent(prompt);
            return result.response.text();
        } catch (error) {
            console.error('Error in translateText:', error);
            throw new Error('Failed to translate text');
        }
    }

    /**
     * Helper function to get language name
     */
    getLanguageName(code) {
        const languages = {
            en: 'English',
            ta: 'Tamil',
            hi: 'Hindi',
            te: 'Telugu',
            ml: 'Malayalam',
            ka: 'Kannada',
        };
        return languages[code] || 'English';
    }
}

export default new AIService();
