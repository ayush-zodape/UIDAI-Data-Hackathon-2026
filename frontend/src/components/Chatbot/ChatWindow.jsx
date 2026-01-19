import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, Loader } from 'lucide-react';
import { askQuestion } from '../../services/api';
import useDataStore from '../../store/useDataStore';

const ChatWindow = () => {
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const { chatHistory, addChatMessage } = useDataStore();
  const messagesEndRef = useRef(null);
  
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };
  
  useEffect(() => {
    scrollToBottom();
  }, [chatHistory]);
  
  const handleSend = async () => {
    if (!input.trim() || loading) return;
    
    const userMessage = { role: 'user', content: input };
    addChatMessage(userMessage);
    setInput('');
    setLoading(true);
    
    try {
      const response = await askQuestion(input);
      addChatMessage({
        role: 'assistant',
        content: response.response,
        suggestions: response.suggested_questions
      });
    } catch (error) {
      addChatMessage({
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        isError: true
      });
    } finally {
      setLoading(false);
    }
  };
  
  const handleSuggestionClick = (suggestion) => {
    setInput(suggestion);
  };
  
  return (
    <div className="bg-white rounded-xl shadow-lg h-[600px] flex flex-col">
      {/* Header */}
      <div className="bg-uidai-blue text-white p-4 rounded-t-xl flex items-center">
        <Bot className="mr-2" size={24} />
        <div>
          <h3 className="font-bold">BLI Assistant</h3>
          <p className="text-sm opacity-80">Ask questions about your data</p>
        </div>
      </div>
      
      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {chatHistory.length === 0 && (
          <div className="text-center text-gray-500 mt-8">
            <Bot size={48} className="mx-auto mb-4 text-gray-300" />
            <p>Ask me anything about your Aadhaar data!</p>
            <p className="text-sm">Try: "Which district has the highest BLI?"</p>
          </div>
        )}
        
        {chatHistory.map((msg, idx) => (
          <div
            key={idx}
            className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-[80%] p-4 rounded-lg ${
                msg.role === 'user'
                  ? 'bg-uidai-blue text-white rounded-br-none'
                  : msg.isError
                  ? 'bg-red-50 text-red-600 rounded-bl-none'
                  : 'bg-gray-100 text-gray-800 rounded-bl-none'
              }`}
            >
              <div className="flex items-start space-x-2">
                {msg.role === 'assistant' && <Bot size={16} className="mt-1" />}
                {msg.role === 'user' && <User size={16} className="mt-1" />}
                <p className="whitespace-pre-wrap">{msg.content}</p>
              </div>
              
              {msg.suggestions && (
                <div className="mt-3 pt-3 border-t border-gray-200">
                  <p className="text-xs text-gray-500 mb-2">Suggested questions:</p>
                  <div className="flex flex-wrap gap-2">
                    {msg.suggestions.map((s, i) => (
                      <button
                        key={i}
                        onClick={() => handleSuggestionClick(s)}
                        className="text-xs bg-white px-2 py-1 rounded border hover:bg-gray-50"
                      >
                        {s}
                      </button>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        ))}
        
        {loading && (
          <div className="flex justify-start">
            <div className="bg-gray-100 p-4 rounded-lg rounded-bl-none">
              <Loader className="animate-spin" size={20} />
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>
      
      {/* Input */}
      <div className="p-4 border-t">
        <div className="flex space-x-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSend()}
            placeholder="Ask about your data..."
            className="flex-1 border rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-uidai-blue"
          />
          <button
            onClick={handleSend}
            disabled={loading || !input.trim()}
            className="bg-uidai-blue text-white px-4 py-2 rounded-lg hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed"
          >
            <Send size={20} />
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatWindow;
