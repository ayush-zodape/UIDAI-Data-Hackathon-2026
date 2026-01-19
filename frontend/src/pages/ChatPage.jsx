import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import useDataStore from '../store/useDataStore';
import ChatWindow from '../components/Chatbot/ChatWindow';

const ChatPage = () => {
  const navigate = useNavigate();
  const { isDataLoaded } = useDataStore();
  
  useEffect(() => {
    if (!isDataLoaded) {
      navigate('/upload');
    }
  }, [isDataLoaded, navigate]);
  
  if (!isDataLoaded) return null;
  
  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold text-gray-800 mb-2">AI Assistant</h1>
      <p className="text-gray-600 mb-6">
        Ask questions about your uploaded data in natural language.
      </p>
      
      <ChatWindow />
      
      {/* Sample Questions */}
      <div className="mt-6 bg-white rounded-xl shadow-lg p-6">
        <h2 className="text-lg font-bold text-gray-800 mb-4">Try These Questions</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {[
            "Which district has the highest BLI?",
            "What is the overall BLI?",
            "How many districts are at critical risk?",
            "What does BLI mean?",
            "Which state has the worst performance?",
            "What interventions do you recommend?"
          ].map((question, idx) => (
            <div
              key={idx}
              className="p-3 bg-gray-50 rounded-lg text-sm text-gray-700 cursor-pointer hover:bg-gray-100"
            >
              {question}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default ChatPage;
