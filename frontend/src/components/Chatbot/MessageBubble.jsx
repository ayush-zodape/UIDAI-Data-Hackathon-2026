import React from 'react';
import { Bot, User } from 'lucide-react';

const MessageBubble = ({ message, isUser }) => {
  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}>
      <div
        className={`max-w-[80%] p-4 rounded-lg ${
          isUser
            ? 'bg-uidai-blue text-white rounded-br-none'
            : 'bg-gray-100 text-gray-800 rounded-bl-none'
        }`}
      >
        <div className="flex items-start space-x-2">
          {!isUser && <Bot size={16} className="mt-1 text-gray-500" />}
          {isUser && <User size={16} className="mt-1" />}
          <p className="whitespace-pre-wrap">{message}</p>
        </div>
      </div>
    </div>
  );
};

export default MessageBubble;
