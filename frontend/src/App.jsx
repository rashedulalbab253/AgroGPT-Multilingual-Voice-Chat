import React, { useState } from 'react';
import ChatInterface from './components/ChatInterface';
import Sidebar from './components/Sidebar';

const App = () => {
    const [activeTab, setActiveTab] = useState('chat');
    const [language, setLanguage] = useState('English');
    const [apiKey, setApiKey] = useState(() => localStorage.getItem('agrogpt_apikey') || '');
    const [sessionId] = useState(() => {
        const saved = localStorage.getItem('agrogpt_session_id');
        if (saved) return saved;
        const newId = `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
        localStorage.setItem('agrogpt_session_id', newId);
        return newId;
    });

    const handleApiKeyChange = (val) => {
        setApiKey(val);
        localStorage.setItem('agrogpt_apikey', val);
    };

    return (
        <div className="flex h-screen w-full bg-gradient-to-br from-gray-900 via-gray-800 to-agro-900 text-white font-sans overflow-hidden">
            {/* Sidebar Navigation */}
            <Sidebar
                activeTab={activeTab}
                setActiveTab={setActiveTab}
                language={language}
                setLanguage={setLanguage}
                apiKey={apiKey}
                setApiKey={handleApiKeyChange}
            />

            {/* Main Content Area */}
            <main className="flex-1 flex flex-col h-full relative">
                {/* Background Gradients */}
                <div className="absolute top-0 left-0 w-full h-full overflow-hidden pointer-events-none z-0">
                    <div className="absolute top-[-10%] right-[-5%] w-96 h-96 bg-agro-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob"></div>
                    <div className="absolute bottom-[-10%] left-[-5%] w-96 h-96 bg-blue-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob animation-delay-2000"></div>
                </div>

                <div className="relative z-10 flex-1 flex flex-col h-full p-4 md:p-6">
                    {activeTab === 'chat' && (
                        <ChatInterface language={language} apiKey={apiKey} sessionId={sessionId} />
                    )}
                    {activeTab === 'tools' && (
                        <div className="flex items-center justify-center h-full text-gray-400">
                            <div className="glass-panel p-8 rounded-2xl text-center">
                                <h2 className="text-2xl font-bold mb-2">Detailed Tools Panel</h2>
                                <p>Use the Chat commands for quick diagnostics.</p>
                            </div>
                        </div>
                    )}
                </div>
            </main>
        </div>
    );
};

export default App;
