import axios from 'axios';

// Vite uses import.meta.env.VITE_* (not process.env.REACT_APP_*)
// Default to '/api' so the Vite dev proxy (vite.config.js) forwards to localhost:5000
export const API_BASE_URL = import.meta.env.VITE_API_URL || '/api';

// Attach Authorization header from localStorage for all requests
axios.interceptors.request.use((config) => {
    try {
        const token = localStorage.getItem('token');
        if (token) {
            config.headers = config.headers || {};
            config.headers.Authorization = `Bearer ${token}`;
        }
    } catch (e) {
        // ignore
    }
    return config;
});

export const apiClient = axios.create({ baseURL: API_BASE_URL });

// Attach token from localStorage if present
apiClient.interceptors.request.use((config) => {
    const token = localStorage.getItem('token');
    if (token) config.headers = { ...(config.headers || {}), Authorization: `Bearer ${token}` };
    return config;
});

export const chatAPI = {
    createSession: (userId, language) => apiClient.post(`/chat/session`, { userId, language }),
    sendMessage: (sessionId, message, language) => apiClient.post(`/chat/message`, { sessionId, message, language }),
    getHistory: (sessionId) => apiClient.get(`/chat/history/${sessionId}`),
    getUserSessions: (userId) => apiClient.get(`/chat/sessions/${userId}`),
    deleteSession: (sessionId) => apiClient.delete(`/chat/session/${sessionId}`),
};

export const firAPI = {
    createFIR: (userId, firData) => apiClient.post(`/fir/create/${userId}`, firData),
    generateDraft: (userId, incidentData, language) => apiClient.post(`/fir/generate/${userId}`, { incidentData, language }),
    getUserFIRs: (userId) => apiClient.get(`/fir/user/${userId}`),
    getFIR: (firId) => apiClient.get(`/fir/${firId}`),
    updateFIR: (firId, updateData) => apiClient.put(`/fir/${firId}`, updateData),
    deleteFIR: (firId) => apiClient.delete(`/fir/${firId}`),
    finalizeFIR: (firId) => apiClient.post(`/fir/finalize/${firId}`),
    getEvidenceChecklist: (crimeCategory, language) => apiClient.post(`/fir/evidence/checklist`, { crimeCategory, language }),
    generatePDF: (firId, language) => apiClient.get(`/fir/pdf/${firId}?language=${language}`),
};

export const legalAPI = {
    getLanguages: () => apiClient.get(`/legal/languages`),
    getCrimeCategories: () => apiClient.get(`/legal/crime-categories`),
    getDisclaimer: () => apiClient.get(`/legal/disclaimer`),
    getEmergencyContacts: () => apiClient.get(`/legal/emergency-contacts`),
};
