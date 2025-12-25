import React, { useState } from 'react';
import ChatInterface from './ChatInterface';
import './FloatingChatButton.css';

const FloatingChatButton = () => {
  const [isOpen, setIsOpen] = useState(false);

  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  const closeChat = () => {
    setIsOpen(false);
  };

  return (
    <div className="floating-chat-container">
      {isOpen && (
        <div className="chat-modal">
          <div className="chat-modal-content">
            <div className="chat-modal-header">
              <h3>🤖 AI Book Assistant</h3>
              <button className="close-modal-button" onClick={closeChat} aria-label="Close chat">
                ×
              </button>
            </div>
            <div className="chat-modal-body">
              <ChatInterface showHeader={false} />
            </div>
          </div>
        </div>
      )}
      <button
        className="floating-chat-button"
        onClick={toggleChat}
        aria-label={isOpen ? "Close chat" : "Open chat"}
      >
        {isOpen ? '×' : '🤖'}
      </button>
    </div>
  );
};

export default FloatingChatButton;