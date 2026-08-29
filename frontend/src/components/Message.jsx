import { User, Bot } from 'lucide-react'
import ReactMarkdown from 'react-markdown'

export default function Message({ role, content }) {
  const isUser = role === 'user'
  
  return (
    <div className={`flex gap-4 ${isUser ? 'flex-row-reverse' : ''}`}>
      <div className={`w-10 h-10 rounded-full flex items-center justify-center shrink-0 ${isUser ? 'bg-blue-600' : 'bg-indigo-600'}`}>
        {isUser ? <User className="w-5 h-5 text-white" /> : <Bot className="w-5 h-5 text-white" />}
      </div>
      
      <div className={`max-w-[75%] rounded-2xl px-5 py-3 ${
        isUser 
          ? 'bg-blue-600 text-white rounded-tr-sm' 
          : 'bg-slate-700 text-slate-100 rounded-tl-sm'
      }`}>
        <div className="prose prose-invert max-w-none prose-p:leading-relaxed prose-pre:bg-slate-800 prose-pre:border prose-pre:border-slate-600">
          <ReactMarkdown>{content}</ReactMarkdown>
        </div>
      </div>
    </div>
  )
}
