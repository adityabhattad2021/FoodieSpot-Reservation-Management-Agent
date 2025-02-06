import  { useState } from 'react';
import { Send, ChefHat, LogIn } from 'lucide-react';
import { Link } from 'react-router-dom';
import { ChatMessage } from '../types';
import axios from 'axios';

export function ChatPage() {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      role: "assistant",
      content: "Hello! I'm your FoodieSpot assistant. I can help you find the perfect restaurant and make reservations. How can I assist you today?"
    }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage: ChatMessage = {
      role: 'user',
      content: input
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await axios.post('http://localhost:8001/chat', {
        message: input
      });

      setMessages(prev => [...prev, {
        role: 'assistant',
        content: response.data.message
      }]);
    } catch (error) {
      console.error('Error sending message:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-50">
      <div className="bg-white shadow-lg">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <Link className="flex items-center space-x-3 cursor-pointer" to="/" >
              <ChefHat className="h-8 w-8 text-blue-600" />
              <h1 className="text-2xl font-bold text-gray-900">FoodieSpot</h1>
            </Link>
            <Link
              to="/login"
              className="flex items-center space-x-2 text-gray-600 hover:text-blue-600 transition-colors"
            >
              <LogIn className="h-5 w-5" />
              <span>Staff Login</span>
            </Link>
          </div>
        </div>
      </div>

      <div className="max-w-4xl mx-auto p-4 h-[calc(100vh-80px)] flex flex-col">
        <div className="flex-1 overflow-y-auto p-4 space-y-4 rounded-t-xl bg-slate-300 backdrop-blur-sm shadow-sm">
          {messages.map((message, index) => (
            <div
              key={index}
              className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[80%] rounded-2xl p-4 ${
                  message.role === 'user'
                    ? 'bg-blue-600 text-white shadow-blue-200'
                    : 'bg-white text-gray-900 shadow-sm'
                } shadow-lg`}
              >
                {message.content}
              </div>
            </div>
          ))}
          {isLoading && (
            <div className="flex justify-start">
              <div className="bg-slate-300 rounded-2xl p-4 shadow-sm animate-pulse">
                <div className="flex space-x-2">
                  <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce" />
                  <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce delay-100" />
                  <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce delay-200" />
                </div>
              </div>
            </div>
          )}
        </div>

        <div className="bg-white p-4 rounded-b-xl shadow-lg">
          <div className="flex gap-2">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSend()}
              placeholder="Ask about restaurants, cuisines, or make a reservation..."
              className="flex-1 border-2 border-gray-200 rounded-xl px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
            />
            <button
              onClick={handleSend}
              disabled={isLoading}
              className="bg-blue-600 text-white rounded-xl px-6 py-2 hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 transition-all"
            >
              <Send className="w-5 h-5" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}