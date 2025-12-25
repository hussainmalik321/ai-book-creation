import React, { useState, useEffect, useRef } from 'react';
import './ChatInterface.css';

const ChatInterface = ({ bookContent, showHeader = true }) => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const [selectedText, setSelectedText] = useState('');
  const messagesEndRef = useRef(null);

  // Initialize session
  useEffect(() => {
    const initSession = async () => {
      try {
        const response = await fetch('http://localhost:8001/api/chat/session', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({})  // Empty body as per the API
        });
        const data = await response.json();
        setSessionId(data.session_id);
      } catch (error) {
        console.error('Failed to initialize session:', error);
        // Fallback to generating a local session ID if API fails
        const fallbackSessionId = 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
        setSessionId(fallbackSessionId);
      }
    };

    initSession();
  }, []);

  // Auto-scroll to bottom of messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    const userMessage = {
      id: Date.now(),
      text: inputValue,
      sender: 'user',
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      const requestBody = {
        query_text: inputValue,
        query_type: selectedText ? "SELECTION_QA" : "GLOBAL_QA",
        selected_text: selectedText || null,
        session_id: sessionId,
      };

      const response = await fetch('http://localhost:8001/api/chat/query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
      });

      if (response.ok) {
        const data = await response.json();
        const botMessage = {
          id: Date.now() + 1,
          text: data.response_text,
          sender: 'bot',
          sources: data.source_chunks || [],
          timestamp: new Date(),
        };

        setMessages(prev => [...prev, botMessage]);
        // Clear selected text after using it for a query
        if (selectedText) {
          setSelectedText('');
        }
      } else {
        // Try to get error details from response
        let errorMessageText = 'Sorry, I encountered an error. Please try again.';
        try {
          const errorData = await response.json();
          if (errorData.detail) {
            errorMessageText = typeof errorData.detail === 'string' ? errorData.detail : (errorData.detail.message || errorMessageText);
          }
        } catch (e) {
          // If we can't parse the error, use the default message
        }

        const errorMessage = {
          id: Date.now() + 1,
          text: errorMessageText,
          sender: 'bot',
          timestamp: new Date(),
        };
        setMessages(prev => [...prev, errorMessage]);
      }
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = {
        id: Date.now() + 1,
        text: 'Sorry, I encountered an error. Please try again.',
        sender: 'bot',
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  // Add event listener for text selection
  useEffect(() => {
    const handleSelection = () => {
      setTimeout(() => {
        const selectedText = window.getSelection().toString().trim();
        if (selectedText && selectedText.length > 10) { // Only consider meaningful selections
          setSelectedText(selectedText);
        }
      }, 0);
    };

    document.addEventListener('mouseup', handleSelection);
    return () => {
      document.removeEventListener('mouseup', handleSelection);
    };
  }, []);

  return (
    <div className="chat-interface">
      {showHeader && (
        <div className="chat-header">
          <h3>AI Book Assistant</h3>
          {selectedText && (
            <div className="selected-text-preview">
              <p><strong>Selected:</strong> {selectedText.substring(0, 60)}{selectedText.length > 60 ? '...' : ''}</p>
              <button
                className="clear-selection-btn"
                onClick={() => setSelectedText('')}
              >
                Clear Selection
              </button>
            </div>
          )}
        </div>
      )}

      <div className="chat-messages">
        {messages.length === 0 && (
          <div className="welcome-message">
            <p>🤖 <strong>AI Book Assistant</strong> is ready to help! Ask me questions about this book's content or select text to ask specific questions about it.</p>
          </div>
        )}
        {messages.map((message) => (
          <div
            key={message.id}
            className={`message ${message.sender}-message`}
          >
            <div className="message-content">
              {message.sender === 'user' ? '👤 ' : '🤖 '}
              {message.text}
              {message.sources && message.sources.length > 0 && (
                <div className="sources">
                  <details>
                    <summary>Sources</summary>
                    {message.sources.map((source, idx) => (
                      <div key={idx} className="source-item">
                        <strong>{source.title}:</strong> {source.text.substring(0, 100)}...
                      </div>
                    ))}
                  </details>
                </div>
              )}
            </div>
            <div className="message-timestamp">
              {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="message bot-message">
            <div className="message-content">
              <div className="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <form className="chat-input-form" onSubmit={handleSubmit}>
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder={selectedText
            ? "Ask about the selected text..."
            : "Ask a question about the book..."
          }
          disabled={isLoading}
        />
        <button type="submit" disabled={isLoading || !inputValue.trim()}>
          {isLoading ? 'Sending...' : 'Send'}
        </button>
      </form>
    </div>
  );
};

export default ChatInterface;