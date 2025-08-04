import React, { useState, useRef, useEffect } from 'react';
import { Bot } from 'lucide-react';
import { useChat } from '../../hooks/useChat';
import MessageBubble from './MessageBubble';
import ChatInput from './ChatInput';
import SourcesPanel from './SourcesPanel';
import QuickActions from './QuickActions';

const ChatInterface = () => {
  const [inputValue, setInputValue] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [showSources, setShowSources] = useState(false);
  const [selectedMessage, setSelectedMessage] = useState(null);
  const messagesEndRef = useRef(null);
  
  const { messages, sendMessage, isLoading } = useChat();

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (message) => {
    if (!message.trim()) return;
    
    setIsTyping(true);
    setInputValue('');
    
    try {
      await sendMessage(message);
    } catch (error) {
      console.error('Failed to send message:', error);
    } finally {
      setIsTyping(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage(inputValue);
    }
  };

  const handleQuickAction = (action) => {
    const actionMessages = {
      'stock_recommendation': 'Can you give me some stock recommendations?',
      'latest_news': 'What are the latest financial news?',
      'market_analysis': 'Can you analyze the current market trends?',
      'help': 'How can I use this finance assistant?'
    };
    
    const message = actionMessages[action] || 'Tell me about finance';
    handleSendMessage(message);
  };

  return (
    <div className="flex h-full bg-black">
      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col">
        {/* Messages Container */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-full text-center">
              <div className="w-16 h-16 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center mb-4">
                <Bot className="w-8 h-8 text-white" />
              </div>
              <h2 className="text-2xl font-bold text-white mb-2">
                Finance AI Assistant
              </h2>
              <p className="text-gray-400 mb-8 max-w-md">
                I'm your AI-powered financial assistant. Ask me about stocks, market analysis, 
                investment strategies, or the latest financial news.
              </p>
              
              {/* Quick Actions */}
              <div className="w-full max-w-2xl">
                <h3 className="text-lg font-semibold text-white mb-4">Quick Actions</h3>
                <QuickActions onActionClick={handleQuickAction} />
              </div>
            </div>
          ) : (
            <div className="space-y-4">
              {messages.map((message, index) => (
                <MessageBubble
                  key={index}
                  message={message}
                  onSourceClick={() => {
                    setSelectedMessage(message);
                    setShowSources(true);
                  }}
                />
              ))}
              
              {isTyping && (
                <div className="flex items-start space-x-3">
                  <div className="w-8 h-8 bg-gray-700 rounded-full flex items-center justify-center">
                    <Bot className="w-4 h-4 text-gray-300" />
                  </div>
                  <div className="flex-1">
                    <div className="bg-gray-800 rounded-lg px-4 py-2">
                      <div className="flex space-x-1">
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div className="border-t border-gray-700 p-4">
          <ChatInput
            value={inputValue}
            onChange={setInputValue}
            onSend={handleSendMessage}
            onKeyPress={handleKeyPress}
            disabled={isLoading || isTyping}
            placeholder="Ask me about stocks, markets, or financial news..."
          />
        </div>
      </div>

      {/* Sources Panel */}
      {showSources && (
        <SourcesPanel
          sources={selectedMessage?.sources || []}
          onClose={() => {
            setShowSources(false);
            setSelectedMessage(null);
          }}
        />
      )}
    </div>
  );
};

export default ChatInterface; 