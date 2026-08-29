import { useState } from 'react'
import axios from 'axios'
import { FileText, Download, Loader2, Play, FileDown, Edit3 } from 'lucide-react'

export default function ArtifactPanel({ sessionId, artifacts, setArtifacts, uploadedFiles }) {
  const [isGenerating, setIsGenerating] = useState(false)
  const [targetFormat, setTargetFormat] = useState('docx')
  const [selectedTemplate, setSelectedTemplate] = useState('')

  const handleGenerate = async () => {
    setIsGenerating(true)
    try {
      const res = await axios.post('http://localhost:8000/generate', {
        session_id: sessionId,
        target_format: targetFormat,
        template_filename: selectedTemplate || null
      })
      
      if (res.data.filename) {
        setArtifacts(prev => [...prev, {
          filename: res.data.filename,
          format: targetFormat,
          timestamp: new Date().toISOString()
        }])
      }
    } catch (err) {
      console.error(err)
      alert("Error generating artifact")
    } finally {
      setIsGenerating(false)
    }
  }

  const handleDownload = (filename) => {
    window.open(`http://localhost:8000/download/${filename}`, '_blank')
  }

  return (
    <div className="bg-slate-800 rounded-xl border border-slate-700 shadow-xl overflow-hidden flex-1 flex flex-col">
      <div className="p-5 border-b border-slate-700 bg-slate-800/50 flex justify-between items-center">
        <h2 className="text-lg font-semibold text-slate-100 flex items-center gap-2">
          <FileText className="w-5 h-5 text-emerald-400" />
          Generated Artifacts
        </h2>
      </div>
      
      <div className="p-6 flex-1 flex flex-col gap-6">
        {/* Controls */}
        <div className="flex gap-4 items-end bg-slate-900/50 p-4 rounded-lg border border-slate-700">
          <div className="flex-1">
            <label className="block text-xs font-medium text-slate-400 mb-2 uppercase">Format</label>
            <select 
              className="w-full bg-slate-900 border border-slate-600 rounded-md p-2 text-slate-200 focus:outline-none focus:border-blue-500"
              value={targetFormat}
              onChange={(e) => setTargetFormat(e.target.value)}
            >
              <option value="docx">Word Document (.docx)</option>
              <option value="pptx">PowerPoint (.pptx)</option>
            </select>
          </div>
          
          <div className="flex-1">
            <label className="block text-xs font-medium text-slate-400 mb-2 uppercase">Template (Optional)</label>
            <select 
              className="w-full bg-slate-900 border border-slate-600 rounded-md p-2 text-slate-200 focus:outline-none focus:border-blue-500"
              value={selectedTemplate}
              onChange={(e) => setSelectedTemplate(e.target.value)}
            >
              <option value="">None</option>
              {uploadedFiles.map((file, idx) => (
                <option key={idx} value={file}>{file}</option>
              ))}
            </select>
          </div>

          <button 
            onClick={handleGenerate}
            disabled={isGenerating}
            className="bg-emerald-600 hover:bg-emerald-500 text-white px-6 py-2 rounded-md font-medium transition-colors flex items-center gap-2 disabled:opacity-50"
          >
            {isGenerating ? <Loader2 className="w-4 h-4 animate-spin" /> : <Play className="w-4 h-4" />}
            Generate
          </button>
        </div>

        {/* Artifact List */}
        <div className="flex-1 overflow-y-auto">
          {artifacts.length === 0 ? (
            <div className="h-full flex items-center justify-center text-slate-500 text-sm">
              No artifacts generated yet.
            </div>
          ) : (
            <ul className="space-y-3">
              {artifacts.map((art, idx) => (
                <li key={idx} className="flex items-center justify-between p-4 bg-slate-900 rounded-lg border border-slate-700 hover:border-slate-500 transition-colors group">
                  <div className="flex items-center gap-3">
                    <FileText className={`w-8 h-8 ${art.format === 'docx' ? 'text-blue-400' : 'text-orange-400'}`} />
                    <div>
                      <p className="text-sm font-medium text-slate-200">{art.filename}</p>
                      <p className="text-xs text-slate-500">{new Date(art.timestamp).toLocaleTimeString()}</p>
                    </div>
                  </div>
                  <div className="flex gap-2">
                    <button 
                      onClick={() => handleDownload(art.filename)}
                      className="p-2 text-slate-400 hover:text-emerald-400 hover:bg-slate-800 rounded-md transition-colors"
                      title="Download"
                    >
                      <FileDown className="w-5 h-5" />
                    </button>
                  </div>
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
    </div>
  )
}
