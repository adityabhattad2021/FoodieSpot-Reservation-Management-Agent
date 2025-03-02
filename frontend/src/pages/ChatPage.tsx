import { useState, useRef, useEffect } from 'react';
import { Send, Trash, Star, MapPin, Pizza, Coffee, Smile, RefreshCw } from 'lucide-react';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
import { ChatMessage } from '../types';
import { Header } from '../components/Header';
import { useAuth } from '../context/AuthContext';

const api = axios.create({
  baseURL: import.meta.env.VITE_CHAT_URL, 
  timeout: 20000,
});

export function ChatPage() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [timedOut, setTimedOut] = useState(false);
  const { user } = useAuth();
  const chatEndRef = useRef<HTMLDivElement>(null);

  console.log("API Base URL:", import.meta.env.VITE_CHAT_URL);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  useEffect(() => {
    let storedSessionId = localStorage.getItem("sessionId");
    if (!storedSessionId) {
      fetchMessages("new");
    }else{
      fetchMessages(storedSessionId);
    }
  }, []);

  const fetchMessages = async (sid: string) => {
    try {
      const response = await api.get(`/conversation/${sid}`);
      if (!response.data || !response.data.history) {
        throw new Error("Invalid response structure");
      }

      setMessages(response.data.history);
      setSessionId(response.data.session_id);
      if(sid === "new"){
        localStorage.setItem("sessionId", response.data.session_id);
      }
    } catch (error) {
      console.error('Error fetching messages:', error);
    }
  };

  const handleDeleteSession = async () => {
    if (!sessionId) return;
    try {
      await api.delete(`/session/${sessionId}`);
      setSessionId(null);
      localStorage.removeItem("sessionId");
      fetchMessages("new");
    } catch (error) {
      console.error('Error clearing session:', error);
    }
  };

  const handleSend = async () => {
    if (!input.trim() || !sessionId) return;

    const userMessage: ChatMessage = {
      role: 'user',
      content: input,
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);
    setTimedOut(false);

    try {
      const response = await api.post('/chat/', {
        message: input,
        session_id: sessionId,
        user_id: user?.user_id // Assuming user object has an id property
      });
      
      if(response.data.detail === "Invalid session ID"){
        alert("Invalid session ID, starting a new session");
        fetchMessages("new");
        return;
      }
      
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: response.data.response
      }]);
      
    } catch (error: any) {
      console.error('Error sending message:', error);
      
      const isTimeoutError = error.code === 'ECONNABORTED' || 
                           (error.message && error.message.includes('timeout'));
      
      if (isTimeoutError) {
        setTimedOut(true);
        setMessages(prev => [...prev, {
          role: 'assistant',
          content: 'The response is taking longer than expected. Your message was sent successfully, but the reply hasn\'t arrived yet. Click the refresh button to check for a response.'
        }]);
      } else {
        setMessages(prev => [...prev, {
          role: 'assistant',
          content: 'Sorry, there was an error processing your request.'
        }]);
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleCheckResponse = async () => {
    if (!sessionId || !timedOut) return;
    
    setIsLoading(true);
    
    try {
      const response = await api.get(`/conversation/${sessionId}`);
      if (!response.data || !response.data.history) {
        throw new Error("Invalid response structure");
      }
      
      setMessages(response.data.history);
      
      setTimedOut(false);
    } catch (error) {
      console.error('Error checking for response:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e:any) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const funSuggestions = [
    { text: 'I feel like pizza tonight!', icon: <Pizza className="w-4 h-4 text-orange-500" /> },
    { text: 'Best romantic date spots?', icon: <Star className="w-4 h-4 text-orange-500" /> },
    { text: 'Recommend a chinese place', icon: <Coffee className="w-4 h-4 text-orange-500" /> },
    { text: 'Hidden gems in Indiranagar?', icon: <MapPin className="w-4 h-4 text-orange-500" /> },
    { text: 'Where to take a big family?', icon: <Smile className="w-4 h-4 text-orange-500" /> },
    { text: 'What\'s the best traditional restaurant?', icon: <Coffee className="w-4 h-4 text-orange-500" /> },
  ];

  const FormattedMessage = ({ content, isUser }: { content: string, isUser: boolean }) => {
    if (isUser) {
      return <span className="whitespace-pre-wrap prose prose-sm text-white">{content}</span>;
    }
    
    return (
      <div className="markdown-content prose prose-sm max-w-none text-gray-900">
        <ReactMarkdown>
          {content}
        </ReactMarkdown>
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-50 to-red-50">
      <Header/>
      <div className="max-w-4xl mx-auto p-4 h-[calc(100vh-80px)] flex flex-col">
        <div className="mb-4 flex flex-col gap-2">
          <div className="flex gap-2 overflow-x-auto pb-2 no-scrollbar">
            {funSuggestions.map((suggestion) => (
              <button
                key={suggestion.text}
                onClick={() => setInput(suggestion.text)}
                className="flex items-center space-x-2 bg-white/80 px-4 py-2 rounded-lg shadow-sm hover:shadow-md hover:bg-white transition-all whitespace-nowrap text-sm"
              >
                {suggestion.icon}
                <span>{suggestion.text}</span>
              </button>
            ))}
          </div>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4 rounded-t-xl bg-white/80 backdrop-blur-sm shadow-sm">
          {messages.map((message, index) => (
            <div
              key={index}
              className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
               <div
                className={`max-w-[80%] rounded-2xl p-2 px-4 ${
                  message.role === 'user'
                    ? 'bg-orange-600 text-white'
                    : 'bg-gray-100'
                } shadow-sm`}
              >
                <FormattedMessage 
                  content={message.content} 
                  isUser={message.role === 'user'} 
                />
              </div>
            </div>
          ))}
          <div ref={chatEndRef} />
          {isLoading && (
            <div className="flex justify-start">
              <div className="bg-gray-100 rounded-2xl p-4 shadow-sm">
                <div className="flex space-x-2">
                  <div className="w-2 h-2 bg-orange-600 rounded-full animate-bounce" />
                  <div className="w-2 h-2 bg-orange-600 rounded-full animate-bounce delay-100" />
                  <div className="w-2 h-2 bg-orange-600 rounded-full animate-bounce delay-200" />
                </div>
              </div>
            </div>
          )}
          {timedOut && !isLoading && (
            <div className="flex justify-center my-2">
              <button 
                onClick={handleCheckResponse}
                className="flex items-center gap-2 bg-orange-600 text-white px-4 py-2 rounded-lg shadow-sm hover:bg-orange-700 transition-all"
              >
                <RefreshCw className="w-4 h-4" />
                <span>Check for response</span>
              </button>
            </div>
          )}
        </div>

        {/* Input Area */}
        <div className="bg-white p-4 rounded-b-xl shadow-lg">
          <div className="flex gap-2">
            <div className="flex-1 relative">
              <textarea
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKeyPress}
                placeholder="Ask about restaurants, cuisines, or make a reservation..."
                rows={1}
                className="w-full border-2 border-gray-200 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all resize-none"
              />
              <div className="absolute right-3 bottom-2 text-xs text-gray-400">
                Press Enter to send
              </div>
            </div>
            <div className="flex flex-col gap-2">
              <button
                onClick={handleSend}
                disabled={isLoading || !input.trim()}
                className="bg-orange-600 text-white rounded-xl px-4 py-3 hover:bg-orange-700 disabled:opacity-50 disabled:cursor-not-allowed shadow-sm hover:shadow-md transition-all"
              >
                <Send className="w-5 h-5" />
              </button>
              <button
                onClick={handleDeleteSession}
                disabled={isLoading}
                className="bg-gray-200 text-gray-600 rounded-xl px-4 py-3 hover:bg-gray-300 disabled:opacity-50 disabled:cursor-not-allowed shadow-sm hover:shadow-md transition-all"
              >
                <Trash className="w-5 h-5" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}