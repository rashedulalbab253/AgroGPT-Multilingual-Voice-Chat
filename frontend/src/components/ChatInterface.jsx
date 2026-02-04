import React, { useRef, useEffect, useState } from 'react';
import { Send, Sprout, Loader2, Bot, User, Mic, Square } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { sendMessage, getHistory, transcribeAudio } from '../hooks/useAPI';

const SYSTEM_INIT = { role: "system", content: "Init" }; // Placeholder, verified by backend

const ChatInterface = ({ language, apiKey, sessionId }) => {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);
    const [isRecording, setIsRecording] = useState(false);
    const mediaRecorderRef = useRef(null);
    const audioChunksRef = useRef([]);
    const scrollRef = useRef(null);

    useEffect(() => {
        if (apiKey && sessionId) {
            setLoading(true);
            getHistory(sessionId, apiKey)
                .then(data => {
                    if (data && data.length > 0) {
                        setMessages(data);
                    }
                })
                .catch(err => console.error("Could not fetch history", err))
                .finally(() => setLoading(false));
        }
    }, [sessionId, apiKey]);

    useEffect(() => {
        if (scrollRef.current) {
            scrollRef.current.scrollIntoView({ behavior: 'smooth' });
        }
    }, [messages, loading]);

    const startRecording = async () => {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorderRef.current = new MediaRecorder(stream);
            audioChunksRef.current = [];

            mediaRecorderRef.current.ondataavailable = (event) => {
                audioChunksRef.current.push(event.data);
            };

            mediaRecorderRef.current.onstop = async () => {
                const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' });
                setLoading(true);
                try {
                    const data = await transcribeAudio(audioBlob, language, apiKey);
                    if (data.transcript) {
                        setInput(data.transcript);
                    }
                } catch (err) {
                    console.error("Transcription error", err);
                    alert("Could not recognize voice. Please try again.");
                } finally {
                    setLoading(false);
                }
            };

            mediaRecorderRef.current.start();
            setIsRecording(true);
        } catch (err) {
            console.error("Mic access denied", err);
            alert("Microphone access is required for voice input.");
        }
    };

    const stopRecording = () => {
        if (mediaRecorderRef.current && isRecording) {
            mediaRecorderRef.current.stop();
            setIsRecording(false);
            mediaRecorderRef.current.stream.getTracks().forEach(track => track.stop());
        }
    };

    const handleSend = async (e) => {
        if (e) e.preventDefault();
        if (!input.trim()) return;
        if (!apiKey) {
            alert("Please enter your API Key in the sidebar settings first.");
            return;
        }

        const userMsg = { role: 'user', content: input };
        setMessages(prev => [...prev, userMsg]);
        setInput('');
        setLoading(true);

        try {
            const history = [...messages, userMsg];
            const data = await sendMessage(history, language, apiKey, sessionId);

            const botMsg = { role: 'assistant', content: data.reply };
            setMessages(prev => [...prev, botMsg]);
        } catch (error) {
            setMessages(prev => [...prev, { role: 'assistant', content: "⚠️ Error: Could not connect to the AgroGPT server. Check your API Key and connection." }]);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex flex-col h-full glass-panel rounded-2xl overflow-hidden">
            {/* Header */}
            <div className="p-4 border-b border-white border-opacity-10 flex items-center gap-3 bg-black bg-opacity-20">
                <div className="p-2 bg-agro-500 rounded-lg">
                    <Sprout size={24} className="text-white" />
                </div>
                <div>
                    <h2 className="font-bold text-lg text-white">AgroGPT Assistant</h2>
                    <div className="flex items-center gap-2">
                        <span className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></span>
                        <span className="text-xs text-gray-400">Online | Language: <span className="text-agro-400">{language}</span></span>
                    </div>
                </div>
            </div>

            {/* Messages Area */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
                {messages.length === 0 && (
                    <div className="h-full flex flex-col items-center justify-center text-gray-500 opacity-60">
                        <Sprout size={64} className="mb-4 text-agro-600" />
                        <p>Ask anything about farming in {language}...</p>
                    </div>
                )}

                <AnimatePresence>
                    {messages.map((msg, idx) => (
                        <motion.div
                            key={idx}
                            initial={{ opacity: 0, y: 10 }}
                            animate={{ opacity: 1, y: 0 }}
                            className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                        >
                            <div className={`max-w-[80%] rounded-2xl p-4 flex gap-3 ${msg.role === 'user'
                                ? 'bg-agro-600 text-white rounded-tr-sm'
                                : 'bg-slate-700 text-gray-100 rounded-tl-sm border border-slate-600'
                                }`}>
                                <div className="mt-1 flex-shrink-0">
                                    {msg.role === 'user' ? <User size={18} /> : <Bot size={18} className="text-agro-400" />}
                                </div>
                                <div className="whitespace-pre-wrap leading-relaxed border-l-2 border-transparent pl-1">
                                    {msg.content}
                                </div>
                            </div>
                        </motion.div>
                    ))}
                </AnimatePresence>

                {loading && (
                    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="flex justify-start">
                        <div className="bg-slate-700 rounded-2xl rounded-tl-sm p-4 flex items-center gap-3">
                            <Loader2 className="animate-spin text-agro-400" size={20} />
                            <span className="text-gray-400 text-sm">AgroGPT is thinking...</span>
                        </div>
                    </motion.div>
                )}
                <div ref={scrollRef} />
            </div>

            {/* Input Area */}
            <form onSubmit={handleSend} className="p-4 bg-black bg-opacity-20 border-t border-white border-opacity-10">
                <div className="flex gap-2">
                    <button
                        type="button"
                        onClick={isRecording ? stopRecording : startRecording}
                        className={`p-3 rounded-xl transition-all duration-200 ${isRecording ? 'bg-red-500 animate-pulse' : 'bg-slate-700 hover:bg-slate-600 text-gray-300'}`}
                    >
                        {isRecording ? <Square size={20} /> : <Mic size={20} />}
                    </button>
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        placeholder={isRecording ? "Listening..." : `Type or speak in ${language}...`}
                        className="flex-1 glass-input rounded-xl px-4 py-3"
                        disabled={loading || isRecording}
                    />
                    <button
                        type="submit"
                        disabled={loading || isRecording || !input.trim()}
                        className="bg-agro-600 hover:bg-agro-500 disabled:opacity-50 disabled:cursor-not-allowed text-white rounded-xl px-6 flex items-center justify-center transition-all duration-200"
                    >
                        <Send size={20} />
                    </button>
                </div>
            </form>
        </div>
    );
};

export default ChatInterface;
