export default function ChatMessage({ message }) {
  const isUser = message.role === 'user';
  const time = new Date(message.timestamp).toLocaleTimeString([], { 
    hour: '2-digit', 
    minute: '2-digit' 
  });

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} animate-fade-in`}>
      <div className={`max-w-[85%] sm:max-w-[75%] ${isUser ? 'order-2' : 'order-1'}`}>
        <div className="relative">
          {/* Glow effect for user messages */}
          {isUser && (
            <div className="absolute inset-0 bg-gradient-to-r from-purple-600 to-pink-600 rounded-2xl blur-lg opacity-30"></div>
          )}
          
          <div
            className={`relative rounded-2xl px-5 py-4 ${
              isUser
                ? 'bg-gradient-to-r from-purple-600 via-pink-600 to-purple-600 bg-[length:200%_100%] text-white shadow-xl shadow-purple-500/20'
                : 'bg-gradient-to-br from-slate-800/80 to-slate-900/80 backdrop-blur-xl text-slate-100 border border-purple-500/20 shadow-lg'
            }`}
          >
            <p className="text-sm leading-relaxed whitespace-pre-wrap">{message.content}</p>
          </div>
        </div>
        
        <div className={`flex items-center gap-2 mt-2 text-xs ${isUser ? 'justify-end' : 'justify-start'}`}>
          <span className="text-slate-500">{time}</span>
          {isUser && (
            <div className="flex items-center gap-1 text-purple-400">
              <svg className="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
              </svg>
              <span className="text-purple-400/70">Sent</span>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
