import React, { forwardRef } from 'react';
import { Send } from 'lucide-react';

const ChatInput = forwardRef(({ value, onChange, onSend, onKeyPress, disabled, placeholder }, ref) => {
  return (
    <div className="flex items-center space-x-2">
      <div className="flex-1 relative">
        <textarea
          ref={ref}
          value={value}
          onChange={(e) => onChange(e.target.value)}
          onKeyPress={onKeyPress}
          disabled={disabled}
          placeholder={placeholder}
          className="w-full px-4 py-3 border border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-gray-800 text-white resize-none placeholder-gray-400"
          rows={1}
          style={{ minHeight: '48px', maxHeight: '120px' }}
        />
      </div>
      
      <button
        onClick={() => onSend(value)}
        disabled={disabled || !value.trim()}
        className="p-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
      >
        <Send className="w-5 h-5" />
      </button>
    </div>
  );
});

ChatInput.displayName = 'ChatInput';

export default ChatInput; 