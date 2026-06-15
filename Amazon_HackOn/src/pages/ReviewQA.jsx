import { useState, useRef, useEffect } from 'react';
import { useMutation } from '@tanstack/react-query';
import { MessageSquare, Send, AlertTriangle, ShieldCheck, HelpCircle, User, MessageCircle } from 'lucide-react';
import { apiService } from '../api/api';

const ReviewQA = () => {
  const [query, setQuery] = useState('');
  const [chatHistory, setChatHistory] = useState([
    { 
      type: 'bot', 
      text: 'Hi! I am the Amazon Review Assistant. Ask me any question about the Noise ColorFit Pro 4 in Hindi, English, or Hinglish, and I will find the answer from real customer reviews.',
      sources: null
    }
  ]);
  
  const chatEndRef = useRef(null);

  const askMutation = useMutation({
    mutationFn: apiService.askQuestion,
    onSuccess: (data) => {
      setChatHistory(prev => [...prev, { 
        type: 'bot', 
        text: data.answer,
        sources: data.source_reviews,
        language: data.language_detected,
        confidence: data.confidence
      }]);
    }
  });

  // Auto-scroll chat
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [chatHistory, askMutation.isPending]);

  const handleSend = (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    // Add user message
    setChatHistory(prev => [...prev, { type: 'user', text: query }]);
    
    // Call API
    askMutation.mutate({
      product_id: "P001", // Hardcoded for demo
      question: query
    });
    
    setQuery('');
  };

  const handleSuggestionClick = (suggestion) => {
    setQuery(suggestion);
    // Add small delay to let state update before sending
    setTimeout(() => {
      setChatHistory(prev => [...prev, { type: 'user', text: suggestion }]);
      askMutation.mutate({ product_id: "P001", question: suggestion });
      setQuery('');
    }, 50);
  };

  return (
    <div className="max-w-6xl mx-auto w-full">
      <div className="flex items-center space-x-3 mb-6">
        <MessageSquare className="text-[#007185]" size={28} />
        <h1 className="text-2xl font-bold">Multilingual Review QA Assistant</h1>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* LEFT: Product Context & Warnings */}
        <div className="lg:col-span-1 space-y-6">
          {/* Product Mock Card */}
          <div className="amazon-card shadow-sm border border-gray-200">
            <h3 className="text-xs font-bold text-gray-500 uppercase tracking-wider mb-4">Currently Viewing</h3>
            <div className="flex items-center space-x-4 mb-4">
              <div className="w-20 h-20 bg-gray-50 flex items-center justify-center border border-gray-200">
                <img src="https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400&q=80" alt="Watch" className="max-w-full max-h-full object-contain" />
              </div>
              <div>
                <h4 className="font-bold text-sm text-[#007185] hover:underline cursor-pointer line-clamp-2">Noise ColorFit Pro 4 Smartwatch</h4>
                <div className="flex items-center mt-1">
                  <span className="text-[#FFA41C] text-sm">★★★★☆</span>
                  <span className="text-xs text-[#007185] ml-2 hover:underline cursor-pointer">12,402 ratings</span>
                </div>
                <div className="text-lg font-medium mt-1">₹3,499</div>
              </div>
            </div>
          </div>

          {/* Return Prevention Alerts */}
          <div className="space-y-4">
            <h3 className="text-sm font-bold border-b border-gray-200 pb-2">Return Prevention Insights</h3>
            
            <div className="bg-amber-50 border border-amber-300 rounded p-4 text-amber-900 shadow-sm flex items-start">
              <AlertTriangle className="mr-3 mt-0.5 flex-shrink-0 text-amber-600" size={20} />
              <div>
                <h4 className="font-bold text-sm">High Return Rate Alert</h4>
                <p className="text-xs mt-1 leading-snug">This seller has a return rate of <strong>24%</strong> (higher than average). We recommend reading reviews carefully before purchasing.</p>
              </div>
            </div>
            
            <div className="bg-[#F0F8FF] border border-[#b2d5d8] rounded p-4 text-[#007185] shadow-sm flex items-start">
              <HelpCircle className="mr-3 mt-0.5 flex-shrink-0" size={20} />
              <div>
                <h4 className="font-bold text-sm text-black">Personalized Suggestion</h4>
                <p className="text-xs mt-1 text-black leading-snug">Based on your return history for electronics, many buyers found the <strong>strap size</strong> of this watch runs slightly small. Consider measuring your wrist.</p>
              </div>
            </div>
          </div>
        </div>

        {/* RIGHT: Chat Interface */}
        <div className="lg:col-span-2">
          <div className="bg-white border border-gray-300 shadow-md rounded flex flex-col h-[600px] overflow-hidden">
            
            {/* Chat Header */}
            <div className="bg-[#232F3E] text-white px-4 py-3 flex items-center justify-between shadow-sm z-10">
              <div className="flex items-center">
                <MessageSquare size={18} className="mr-2 text-amazon-yellow" />
                <span className="font-bold text-sm">Review Assistant (AI)</span>
              </div>
              <div className="text-xs text-gray-400 flex items-center">
                <ShieldCheck size={14} className="mr-1 text-green-400" /> Grounded in real reviews only
              </div>
            </div>
            
            {/* Chat Messages */}
            <div className="flex-grow overflow-y-auto p-4 space-y-4 bg-gray-50">
              {chatHistory.map((msg, idx) => (
                <div key={idx} className={`flex flex-col ${msg.type === 'user' ? 'items-end' : 'items-start'}`}>
                  
                  {/* Message Bubble */}
                  <div className={`max-w-[85%] rounded-lg p-3 ${
                    msg.type === 'user' 
                      ? 'bg-[#dcf8c6] text-black rounded-tr-none border border-[#b8e0a3] shadow-sm' 
                      : 'bg-white text-black rounded-tl-none border border-gray-200 shadow-sm'
                  }`}>
                    {msg.type === 'bot' && idx === 0 ? (
                      <div className="text-sm">{msg.text}</div>
                    ) : msg.type === 'user' ? (
                      <div className="text-sm">{msg.text}</div>
                    ) : (
                      <div className="text-sm">
                        <div className="whitespace-pre-wrap">{msg.text}</div>
                        
                        {/* Source citations */}
                        {msg.sources && msg.sources.length > 0 && (
                          <div className="mt-3 pt-3 border-t border-gray-100 bg-gray-50 -mx-3 -mb-3 p-3 rounded-b-lg">
                            <div className="text-xs font-bold text-gray-500 mb-2 flex justify-between items-center">
                              <span>Sources used:</span>
                              <span className="text-[10px] bg-blue-100 text-blue-800 px-1.5 py-0.5 rounded">
                                Lang: {msg.language?.toUpperCase() || 'EN'}
                              </span>
                            </div>
                            <div className="space-y-2">
                              {msg.sources.map((src, i) => (
                                <div key={i} className="text-xs text-gray-600 bg-white p-2 border border-gray-100 rounded">
                                  <div className="flex items-center justify-between mb-1">
                                    <div className="flex items-center font-medium text-black">
                                      <User size={10} className="mr-1 text-gray-400" /> {src.user}
                                    </div>
                                    <div className="text-[#FFA41C]">
                                      {'★'.repeat(src.rating)}{'☆'.repeat(5-src.rating)}
                                    </div>
                                  </div>
                                  <div className="line-clamp-2 italic">"{src.text}"</div>
                                </div>
                              ))}
                            </div>
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                </div>
              ))}
              
              {/* Loading Indicator */}
              {askMutation.isPending && (
                <div className="flex flex-col items-start">
                  <div className="max-w-[85%] rounded-lg rounded-tl-none p-3 bg-white border border-gray-200 shadow-sm flex items-center space-x-2">
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.4s' }}></div>
                  </div>
                </div>
              )}
              
              <div ref={chatEndRef} />
            </div>
            
            {/* Suggestions */}
            <div className="bg-white border-t border-gray-200 p-2 overflow-x-auto whitespace-nowrap">
              <div className="flex space-x-2 px-2">
                <button 
                  onClick={() => handleSuggestionClick("battery kitne din chalti hai?")}
                  className="text-xs border border-[#007185] text-[#007185] bg-[#F0F8FF] hover:bg-[#E0F0FF] rounded-full px-3 py-1.5 transition-colors"
                >
                  battery kitne din chalti hai? (Hinglish)
                </button>
                <button 
                  onClick={() => handleSuggestionClick("क्या यह वाटरप्रूफ है?")}
                  className="text-xs border border-[#007185] text-[#007185] bg-[#F0F8FF] hover:bg-[#E0F0FF] rounded-full px-3 py-1.5 transition-colors"
                >
                  क्या यह वाटरप्रूफ है? (Hindi)
                </button>
                <button 
                  onClick={() => handleSuggestionClick("Is the heart rate sensor accurate?")}
                  className="text-xs border border-[#007185] text-[#007185] bg-[#F0F8FF] hover:bg-[#E0F0FF] rounded-full px-3 py-1.5 transition-colors"
                >
                  Is the heart rate sensor accurate? (English)
                </button>
              </div>
            </div>
            
            {/* Input Box */}
            <div className="bg-gray-100 p-3 border-t border-gray-200">
              <form onSubmit={handleSend} className="relative flex items-center">
                <input
                  type="text"
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  placeholder="Ask a question in any language..."
                  className="w-full pl-4 pr-12 py-3 rounded-full border border-gray-300 focus:outline-none focus:border-[#007185] focus:ring-1 focus:ring-[#007185] shadow-inner text-sm"
                  disabled={askMutation.isPending}
                />
                <button 
                  type="submit"
                  disabled={!query.trim() || askMutation.isPending}
                  className={`absolute right-2 p-2 rounded-full ${!query.trim() || askMutation.isPending ? 'text-gray-400' : 'text-[#007185] hover:bg-gray-200'}`}
                >
                  <Send size={18} />
                </button>
              </form>
            </div>
            
          </div>
        </div>
      </div>
    </div>
  );
};

export default ReviewQA;
