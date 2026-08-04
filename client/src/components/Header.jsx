export default function Header() {
  return (
    <header className="bg-gradient-to-r from-slate-900 via-blue-900/20 to-slate-900 border-b border-blue-500/20 backdrop-blur-xl relative overflow-hidden">
      {/* Animated background effect */}
      <div className="absolute inset-0 bg-gradient-to-r from-blue-600/5 via-cyan-600/5 to-blue-600/5 animate-pulse"></div>
      
      <div className="max-w-6xl mx-auto px-4 py-6 relative z-10">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div className="flex items-center gap-4">
            <div className="relative">
              <div className="absolute inset-0 bg-gradient-to-r from-blue-600 to-cyan-600 rounded-xl blur-lg opacity-50 animate-pulse"></div>
              <div className="relative w-12 h-12 bg-gradient-to-r from-blue-600 via-cyan-600 to-blue-600 rounded-xl flex items-center justify-center shadow-lg shadow-blue-500/30">
                <svg className="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
            </div>
            <div>
              <h1 className="text-2xl font-bold bg-gradient-to-r from-white via-blue-200 to-cyan-200 bg-clip-text text-transparent">
                YouTube RAG Assistant
              </h1>
              <p className="text-slate-400 text-sm mt-1 flex items-center gap-2">
                <span className="w-1.5 h-1.5 bg-blue-500 rounded-full animate-pulse"></span>
                Chat with any YouTube video using AI
              </p>
            </div>
          </div>
          <div className="flex items-center gap-3 bg-slate-800/50 backdrop-blur-sm px-4 py-2 rounded-full border border-blue-500/20">
            <div className="w-2.5 h-2.5 bg-emerald-500 rounded-full animate-pulse shadow-lg shadow-emerald-500/50"></div>
            <span className="text-sm text-emerald-400 font-medium">Ready</span>
          </div>
        </div>
      </div>
    </header>
  );
}
