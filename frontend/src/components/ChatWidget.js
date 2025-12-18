import React, { useState, useEffect, useRef } from 'react';
import styles from './ChatWidget.module.css';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';

const ChatWidget = () => {
    const [isOpen, setIsOpen] = useState(false);
    const [message, setMessage] = useState('');
    const [conversation, setConversation] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const chatWindowRef = useRef(null);

    const {
        siteConfig: { customFields },
    } = useDocusaurusContext();
    const backendUrl = customFields.backendUrl;

    const toggleChat = () => {
        setIsOpen(!isOpen);
    };

    const sendMessage = async (e) => {
        e.preventDefault();
        if (!message.trim()) return;

        const userMessage = { text: message, sender: 'user' };
        setConversation((prev) => [...prev, userMessage]);
        setMessage('');
        setIsLoading(true);

        try {
            const response = await fetch(`${backendUrl}/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ query: message }),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            setConversation((prev) => [...prev, { text: data.response, sender: 'bot' }]);
        } catch (error) {
            console.error('Error sending message:', error);
            setConversation((prev) => [...prev, { text: `Error: ${error.message}`, sender: 'bot' }]);
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
        if (chatWindowRef.current) {
            chatWindowRef.current.scrollTop = chatWindowRef.current.scrollHeight;
        }
    }, [conversation]);

    return (
        <>
            {isOpen && (
                <div className={styles.chatWindow}>
                    <div className={styles.chatHeader} onClick={toggleChat}>
                        <div className={styles.headerTitle}>AI Assistant</div>
                        <button className={styles.closeButton}>×</button>
                    </div>
                    <div className={styles.chatBody} ref={chatWindowRef}>
                        {conversation.length === 0 && !isLoading && (
                            <div className={styles.welcomeMessage}>
                                Hello! I'm your AI assistant for the Docusaurus book. How can I help you today?
                            </div>
                        )}
                        {conversation.map((msg, index) => (
                            <div key={index} className={`${styles.message} ${styles[msg.sender]}`}>
                                {msg.text.split('\n').map((line, i) => (
                                    <div key={i}>{line}</div>
                                ))}
                            </div>
                        ))}
                        {isLoading && (
                            <div className={`${styles.message} ${styles.bot}`}>
                                <div className={styles.loadingDots}>
                                    <span></span>
                                    <span></span>
                                    <span></span>
                                </div>
                            </div>
                        )}
                    </div>
                    <form className={styles.chatInputForm} onSubmit={sendMessage}>
                        <input
                            type="text"
                            value={message}
                            onChange={(e) => setMessage(e.target.value)}
                            placeholder="Ask me anything about the book..."
                            disabled={isLoading}
                        />
                        <button type="submit" disabled={isLoading} aria-label="Send message">
                            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                                <line x1="22" y1="2" x2="11" y2="13"></line>
                                <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
                            </svg>
                        </button>
                    </form>
                </div>
            )}
            {!isOpen && (
                <button className={styles.chatToggleButton} onClick={toggleChat} aria-label="Open chat">
                    <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                        <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
                    </svg>
                </button>
            )}
        </>
    );
};

export default ChatWidget;