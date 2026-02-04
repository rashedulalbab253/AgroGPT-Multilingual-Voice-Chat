import React from 'react';
import { MessageSquare, Settings, Languages, Leaf, Hammer } from 'lucide-react';

const LANGUAGES_LIST = [
    "English", "Hindi", "Gujarati", "Bengali", "Kannada", "Punjabi"
];

const Sidebar = ({ activeTab, setActiveTab, language, setLanguage, apiKey, setApiKey }) => {
    return (
        <div className="w-20 md:w-64 h-full bg-slate-900 border-r border-slate-700 flex flex-col transition-all duration-300">
            {/* Logo Area */}
            <div className="p-6 flex items-center justify-center md:justify-start gap-3 border-b border-slate-700">
                <div className="w-10 h-10 bg-agro-500 rounded-xl flex items-center justify-center shadow-lg shadow-agro-500/20">
                    <Leaf className="text-white" size={24} />
                </div>
                <h1 className="font-bold text-xl text-white hidden md:block tracking-wide">Agro<span className="text-agro-500">GPT</span></h1>
            </div>

            {/* Nav Items */}
            <nav className="flex-1 p-4 space-y-2">
                <NavItem
                    icon={<MessageSquare size={20} />}
                    label="Expert Chat"
                    isActive={activeTab === 'chat'}
                    onClick={() => setActiveTab('chat')}
                />
                <NavItem
                    icon={<Hammer size={20} />}
                    label="Quick Tools"
                    isActive={activeTab === 'tools'}
                    onClick={() => setActiveTab('tools')}
                />
            </nav>

            {/* Settings Area */}
            <div className="p-4 border-t border-slate-700 space-y-4">
                {/* Language Selector */}
                <div className="hidden md:block">
                    <label className="text-xs font-semibold text-gray-500 uppercase mb-2 block flex items-center gap-2">
                        <Languages size={14} /> Language
                    </label>
                    <select
                        value={language}
                        onChange={(e) => setLanguage(e.target.value)}
                        className="w-full bg-slate-800 text-sm text-gray-200 rounded-lg p-2 border border-slate-600 focus:border-agro-500 outline-none"
                    >
                        {LANGUAGES_LIST.map(lang => (
                            <option key={lang} value={lang}>{lang}</option>
                        ))}
                    </select>
                </div>

                {/* API Key Input */}
                <div className="hidden md:block">
                    <label className="text-xs font-semibold text-gray-500 uppercase mb-2 block flex items-center gap-2">
                        <Settings size={14} /> Master Key
                    </label>
                    <input
                        type="password"
                        value={apiKey}
                        onChange={(e) => setApiKey(e.target.value)}
                        placeholder="Enter Key..."
                        className="w-full bg-slate-800 text-sm text-gray-200 rounded-lg p-2 border border-slate-600 focus:border-agro-500 outline-none"
                    />
                </div>
            </div>
        </div>
    );
};

const NavItem = ({ icon, label, isActive, onClick }) => (
    <button
        onClick={onClick}
        className={`w-full flex items-center gap-3 p-3 rounded-xl transition-all duration-200 ${isActive
                ? 'bg-agro-600 text-white shadow-lg shadow-agro-600/20'
                : 'text-gray-400 hover:bg-slate-800 hover:text-gray-200'
            }`}
    >
        {icon}
        <span className="hidden md:block font-medium">{label}</span>
    </button>
);

export default Sidebar;
