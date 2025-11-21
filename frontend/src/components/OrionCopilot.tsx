"use client";

import { useState } from "react";
import { MessageSquare, X, Send, Sparkles } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

export default function OrionCopilot() {
    const [isOpen, setIsOpen] = useState(false);
    const [messages, setMessages] = useState([
        { role: "assistant", content: "Olá! Sou Orion, sua IA de comando. Como posso ajudar a otimizar suas operações hoje?" }
    ]);
    const [inputValue, setInputValue] = useState("");

    const toggleChat = () => setIsOpen(!isOpen);

    const sendMessage = () => {
        if (!inputValue.trim()) return;

        setMessages([...messages, { role: "user", content: inputValue }]);
        setInputValue("");

        // Simulate AI response
        setTimeout(() => {
            setMessages(prev => [...prev, { role: "assistant", content: "Processando sua solicitação nos servidores quânticos..." }]);
        }, 1000);
    };

    return (
        <div className="fixed bottom-6 right-6 z-[100] flex flex-col items-end">
            <AnimatePresence>
                {isOpen && (
                    <motion.div
                        initial={{ opacity: 0, y: 20, scale: 0.9 }}
                        animate={{ opacity: 1, y: 0, scale: 1 }}
                        exit={{ opacity: 0, y: 20, scale: 0.9 }}
                        className="mb-4 w-[90vw] md:w-96 h-[500px] glass-panel rounded-2xl flex flex-col overflow-hidden border border-[var(--color-quantum-purple)] shadow-[0_0_30px_rgba(108,52,131,0.3)]"
                    >
                        {/* Header */}
                        <div className="p-4 bg-gradient-to-r from-[var(--color-void-black)] to-[var(--color-quantum-purple)] flex items-center justify-between border-b border-[var(--color-glass-border)]">
                            <div className="flex items-center gap-2">
                                <Sparkles className="w-5 h-5 text-[var(--color-photon-gold)]" />
                                <h3 className="font-orbitron text-lg text-white tracking-wider">ORION v1.0</h3>
                            </div>
                            <button onClick={toggleChat} className="text-gray-400 hover:text-white transition-colors">
                                <X className="w-5 h-5" />
                            </button>
                        </div>

                        {/* Messages */}
                        <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-black/40">
                            {messages.map((msg, idx) => (
                                <div key={idx} className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}>
                                    <div className={`max-w-[80%] p-3 rounded-xl text-sm ${msg.role === "user"
                                            ? "bg-[var(--color-quantum-purple)] text-white rounded-br-none"
                                            : "bg-[var(--color-glass-border)] text-gray-200 rounded-bl-none border border-white/10"
                                        }`}>
                                        {msg.content}
                                    </div>
                                </div>
                            ))}
                        </div>

                        {/* Input */}
                        <div className="p-4 bg-black/60 border-t border-[var(--color-glass-border)]">
                            <div className="flex gap-2">
                                <input
                                    type="text"
                                    value={inputValue}
                                    onChange={(e) => setInputValue(e.target.value)}
                                    onKeyPress={(e) => e.key === "Enter" && sendMessage()}
                                    placeholder="Digite um comando..."
                                    className="flex-1 bg-transparent border border-[var(--color-glass-border)] rounded-lg px-4 py-2 text-white focus:outline-none focus:border-[var(--color-neon-blue)] transition-colors"
                                />
                                <button
                                    onClick={sendMessage}
                                    className="p-2 bg-[var(--color-quantum-purple)] rounded-lg hover:bg-purple-700 transition-colors text-white"
                                >
                                    <Send className="w-5 h-5" />
                                </button>
                            </div>
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>

            <motion.button
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.9 }}
                onClick={toggleChat}
                className="w-14 h-14 rounded-full bg-gradient-to-br from-[var(--color-quantum-purple)] to-[var(--color-void-black)] border border-[var(--color-photon-gold)] shadow-[0_0_20px_rgba(244,208,63,0.4)] flex items-center justify-center text-white z-50"
            >
                {isOpen ? <X className="w-6 h-6" /> : <MessageSquare className="w-6 h-6" />}
            </motion.button>
        </div>
    );
}
