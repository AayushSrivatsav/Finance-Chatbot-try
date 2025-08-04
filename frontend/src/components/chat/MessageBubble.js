import React from 'react';
import { Bot, User, FileText } from 'lucide-react';
import { formatTimestamp } from '../../utils/dateUtils';

const MessageBubble = ({ message, onSourceClick }) => {
  const isUser = message.message_type === 'user';
  const isBot = message.message_type === 'bot';

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}>
      <div className={`flex max-w-xs lg:max-w-md ${isUser ? 'flex-row-reverse' : 'flex-row'} items-start space-x-2`}>
        <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
          isUser 
            ? 'bg-blue-600 text-white' 
            : 'bg-gray-700 text-gray-300'
        }`}>
          {isUser ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
        </div>
        
        <div className={`flex flex-col ${isUser ? 'items-end' : 'items-start'}`}>
          <div className={`px-4 py-2 rounded-lg max-w-xs lg:max-w-md ${
            isUser
              ? 'bg-blue-600 text-white'
              : 'bg-gray-800 text-white border border-gray-700'
          }`}>
            <p className="text-sm whitespace-pre-wrap">{message.content}</p>
          </div>
          
          {isBot && message.sources && message.sources.length > 0 && (
            <button
              onClick={() => onSourceClick && onSourceClick()}
              className="mt-2 flex items-center space-x-1 text-xs text-gray-400 hover:text-blue-400 transition-colors"
            >
              <FileText className="w-3 h-3" />
              <span>{message.sources.length} source(s)</span>
            </button>
          )}
          
          <span className="text-xs text-gray-500 mt-1">
            {formatTimestamp(message.timestamp)}
          </span>
        </div>
      </div>
    </div>
  );
};

export default MessageBubble; 