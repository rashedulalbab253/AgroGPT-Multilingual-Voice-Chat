import axios from 'axios';

// Create an Axios instance
const api = axios.create({
    baseURL: import.meta.env.VITE_BACKEND_URL || 'https://rashed-agrogpt-backend-3zpk.onrender.com/api/v1',
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
        // Determine proper file extension from blob MIME type
        const mimeType = audioBlob.type || 'audio/webm';
        let extension = 'webm';
        if (mimeType.includes('wav')) extension = 'wav';
        else if (mimeType.includes('mp4') || mimeType.includes('m4a')) extension = 'mp4';
        else if (mimeType.includes('ogg')) extension = 'ogg';

        const formData = new FormData();
        formData.append('file', audioBlob, `recording.${extension}`);
        formData.append('language_name', languageName);

        // IMPORTANT: We must NOT set Content-Type here.
        // Axios needs to auto-generate the multipart/form-data boundary.
        // Setting it to undefined with the instance's default 'application/json' 
        // can interfere. We use a fresh headers object with only the API key.
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
