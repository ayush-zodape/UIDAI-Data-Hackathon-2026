import React, { useState } from 'react';
import { Send } from 'lucide-react';

const ChatInput = ({ onSend, disabled }) => {
  const [input, setInput] = useState('');
  
  const handleSubmit = () => {
    if (input.trim() && !disabled) {
      onSend(input.trim());
      setInput('');
    }
  };
  
  return (
    <div className="flex space-x-2 p-4 border-t">
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyPress={(e) => e.key === 'Enter' && handleSubmit()}
        placeholder="Ask about your data..."
        disabled={disabled}
        className="flex-1 border rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-uidai-blue disabled:bg-gray-100"
      />
      <button
        onClick={handleSubmit}
        disabled={disabled || !input.trim()}
        className="bg-uidai-blue text-white px-4 py-2 rounded-lg hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
      >
        <Send size={20} />
      </button>
    </div>
  );
};

export default ChatInput;
