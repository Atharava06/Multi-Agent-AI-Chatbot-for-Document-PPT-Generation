import { useState } from 'react'
import ChatWindow from './components/ChatWindow'
import UploadPanel from './components/UploadPanel'
import ArtifactPanel from './components/ArtifactPanel'

function App() {
  const [sessionId] = useState(() => Math.random().toString(36).substring(7))
  const [artifacts, setArtifacts] = useState([])
  const [uploadedFiles, setUploadedFiles] = useState([])

  return (
    <div className="flex h-screen w-full bg-slate-900 text-slate-100 overflow-hidden font-sans">
      
      {/* Left Panel: Chat */}
      <div className="w-1/2 h-full flex flex-col border-r border-slate-700 bg-slate-800 shadow-2xl z-10">
        <div className="p-6 border-b border-slate-700 bg-slate-800/80 backdrop-blur">
          <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-indigo-400 bg-clip-text text-transparent">Enterprise Multi-Agent Chatbot</h1>
          <p className="text-sm text-slate-400 mt-1">Orchestrating documents, PPTs, and web research.</p>
        </div>
        <ChatWindow sessionId={sessionId} />
      </div>

      {/* Right Panel: Uploads & Artifacts */}
      <div className="w-1/2 h-full flex flex-col bg-slate-900 overflow-y-auto">
        <div className="p-8 flex flex-col gap-8">
          <UploadPanel 
            uploadedFiles={uploadedFiles} 
            setUploadedFiles={setUploadedFiles} 
          />
          <ArtifactPanel 
            sessionId={sessionId} 
            artifacts={artifacts} 
            setArtifacts={setArtifacts} 
            uploadedFiles={uploadedFiles} 
          />
        </div>
      </div>
      
    </div>
  )
}

export default App
