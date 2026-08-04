import { useState } from 'react';
import Header from './components/Header';
import VideoInput from './components/VideoInput';
import ChatWindow from './components/ChatWindow';
import ChatInput from './components/ChatInput';
import { api } from './services/api';

function App() {
  const [videoId, setVideoId] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [isChatLoading, setIsChatLoading] = useState(false);
  const [messages, setMessages] = useState([]);
  const [error, setError] = useState(null);

  const handleProcessVideo = async (url) => {
    setIsProcessing(true);
    setError(null);

    try {
      const response = await api.processVideo(url);
      if (response.success) {
        setVideoId(response.video_id);
        setMessages([
          {
            id: Date.now(),
            role: 'assistant',
            content: `Video processed successfully! You can now ask questions about this video.`,
            timestamp: Date.now(),
          },
        ]);
      }
    } catch (err) {
      setError(err.message || 'Failed to process video');
    } finally {
      setIsProcessing(false);
    }
  };

  const handleSendMessage = async (question) => {
    if (!videoId) return;

    const userMessage = {
      id: Date.now(),
      role: 'user',
      content: question,
      timestamp: Date.now(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsChatLoading(true);
    setError(null);

    try {
      const response = await api.askQuestion(question);
      const assistantMessage = {
        id: Date.now() + 1,
        role: 'assistant',
        content: response.answer,
        timestamp: Date.now(),
      };
      setMessages((prev) => [...prev, assistantMessage]);
    } catch (err) {
      setError(err.message || 'Failed to get answer');
      const errorMessage = {
        id: Date.now() + 1,
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: Date.now(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsChatLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 flex flex-col relative overflow-hidden">
      {/* Animated background orbs */}
      <div className="fixed top-0 left-0 w-full h-full pointer-events-none overflow-hidden">
        <div className="absolute top-20 left-10 w-96 h-96 bg-blue-600/5 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute top-40 right-20 w-80 h-80 bg-cyan-600/5 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '1s' }}></div>
        <div className="absolute bottom-20 left-1/3 w-96 h-96 bg-indigo-600/5 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '2s' }}></div>
        <div className="absolute bottom-40 right-1/4 w-80 h-80 bg-blue-600/5 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '3s' }}></div>
      </div>
      
      <div className="relative z-10 flex flex-col min-h-screen">
        <Header />
        <VideoInput
          onProcessVideo={handleProcessVideo}
          isProcessing={isProcessing}
          videoId={videoId}
        />
        {error && (
          <div className="mx-4 mb-4 bg-red-900/30 backdrop-blur-xl border border-red-500/30 text-red-400 px-6 py-4 rounded-xl shadow-lg shadow-red-500/10 flex items-center gap-3">
            <svg className="w-5 h-5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
            </svg>
            <span className="text-sm">{error}</span>
          </div>
        )}
        <ChatWindow messages={messages} isLoading={isChatLoading} />
        <ChatInput
          onSend={handleSendMessage}
          disabled={!videoId}
          isLoading={isChatLoading}
        />
      </div>
    </div>
  );
}

export default App;
