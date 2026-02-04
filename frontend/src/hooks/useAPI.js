import axios from 'axios';

// Create an Axios instance
const api = axios.create({
    baseURL: import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000/api/v1',
    headers: {
        'Content-Type': 'application/json',
    },
});

export const sendMessage = async (messages, targetLanguage, apiKey, sessionId) => {
    try {
        const response = await api.post('/chat', {
            session_id: sessionId,
            messages,
            target_language: targetLanguage
        }, {
            headers: {
                'X-API-Key': apiKey
            }
        });
        return response.data;
    } catch (error) {
        console.error("API Error", error);
        throw error;
    }
};

export const getHistory = async (sessionId, apiKey) => {
    try {
        const response = await api.get(`/history/${sessionId}`, {
            headers: {
                'X-API-Key': apiKey
            }
        });
        return response.data;
    } catch (error) {
        console.error("API Error", error);
        throw error;
    }
};

export const transcribeAudio = async (audioBlob, languageName, apiKey) => {
    try {
        const formData = new FormData();
        formData.append('file', audioBlob, 'record.webm');
        formData.append('language_name', languageName);

        const response = await api.post('/transcribe', formData, {
            headers: {
                'X-API-Key': apiKey,
                'Content-Type': 'multipart/form-data'
            }
        });
        return response.data;
    } catch (error) {
        console.error("API Error", error);
        throw error;
    }
};

export const translateText = async (text, sourceLang, targetLang, apiKey) => {
    try {
        const response = await api.post('/translate', {
            text,
            source_language: sourceLang,
            target_language: targetLang
        }, {
            headers: {
                'X-API-Key': apiKey
            }
        });
        return response.data;
    } catch (error) {
        console.error("API Error", error);
        throw error;
    }
};
