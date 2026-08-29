import { useState } from 'react'
import axios from 'axios'
import { UploadCloud, File as FileIcon, Loader2 } from 'lucide-react'

export default function UploadPanel({ uploadedFiles, setUploadedFiles }) {
  const [isUploading, setIsUploading] = useState(false)

  const handleFileUpload = async (e) => {
    const files = e.target.files
    if (!files.length) return

    const formData = new FormData()
    for (let i = 0; i < files.length; i++) {
      formData.append('files', files[i])
    }

    setIsUploading(true)
    try {
      const res = await axios.post('http://localhost:8000/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
      setUploadedFiles(prev => [...prev, ...res.data.files])
    } catch (err) {
      console.error(err)
      alert("Error uploading files")
    } finally {
      setIsUploading(false)
      // reset file input
      e.target.value = null
    }
  }

  return (
    <div className="bg-slate-800 rounded-xl border border-slate-700 shadow-xl overflow-hidden">
      <div className="p-5 border-b border-slate-700 bg-slate-800/50">
        <h2 className="text-lg font-semibold text-slate-100 flex items-center gap-2">
          <UploadCloud className="w-5 h-5 text-blue-400" />
          Templates & Documents
        </h2>
      </div>
      
      <div className="p-6">
        <label className="flex flex-col items-center justify-center w-full h-32 border-2 border-slate-600 border-dashed rounded-lg cursor-pointer bg-slate-900/50 hover:bg-slate-700 transition-colors group">
          <div className="flex flex-col items-center justify-center pt-5 pb-6">
            {isUploading ? (
              <Loader2 className="w-8 h-8 text-blue-500 animate-spin mb-2" />
            ) : (
              <UploadCloud className="w-8 h-8 text-slate-400 group-hover:text-blue-400 mb-2 transition-colors" />
            )}
            <p className="mb-2 text-sm text-slate-400">
              <span className="font-semibold text-blue-400">Click to upload</span> or drag and drop
            </p>
            <p className="text-xs text-slate-500">DOCX, PPTX, PDF, Images</p>
          </div>
          <input type="file" className="hidden" multiple onChange={handleFileUpload} disabled={isUploading} />
        </label>

        {uploadedFiles.length > 0 && (
          <div className="mt-6">
            <h3 className="text-sm font-medium text-slate-400 mb-3 uppercase tracking-wider">Uploaded Files</h3>
            <ul className="space-y-2">
              {uploadedFiles.map((file, idx) => (
                <li key={idx} className="flex items-center gap-3 p-3 bg-slate-900 rounded-lg border border-slate-700">
                  <FileIcon className="w-5 h-5 text-indigo-400" />
                  <span className="text-sm text-slate-200 truncate">{file}</span>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  )
}
