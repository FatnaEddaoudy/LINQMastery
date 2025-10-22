import { useState, useRef } from 'react'
import { Download, Plus, Type, Image, Square } from 'lucide-react'

const EbookDesigner = () => {
  const [title, setTitle] = useState('')
  const [content, setContent] = useState('')
  const [pages, setPages] = useState([{ title: 'Chapter 1', content: 'Start writing your content here...' }])
  const canvasRef = useRef<HTMLCanvasElement>(null)

  const addPage = () => {
    setPages([...pages, { title: `Chapter ${pages.length + 1}`, content: 'New chapter content...' }])
  }

  const updatePage = (index: number, field: 'title' | 'content', value: string) => {
    const updatedPages = pages.map((page, i) => 
      i === index ? { ...page, [field]: value } : page
    )
    setPages(updatedPages)
  }

  const exportToPDF = async () => {
    // Implementation for PDF export using jsPDF
    const { jsPDF } = await import('jspdf')
    const doc = new jsPDF()
    
    // Add title
    doc.setFontSize(20)
    doc.text(title || 'My eBook', 20, 30)
    
    // Add pages
    pages.forEach((page, index) => {
      if (index > 0) doc.addPage()
      doc.setFontSize(16)
      doc.text(page.title, 20, 50)
      doc.setFontSize(12)
      const lines = doc.splitTextToSize(page.content, 170)
      doc.text(lines, 20, 70)
    })
    
    doc.save('ebook.pdf')
  }

  return (
    <div className="p-6">
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">eBook Designer</h2>
        
        {/* Title Input */}
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            eBook Title
          </label>
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="Enter your eBook title"
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
          />
        </div>

        {/* Design Tools */}
        <div className="flex space-x-2 mb-6">
          <button className="flex items-center space-x-2 px-4 py-2 bg-gray-100 rounded-md hover:bg-gray-200">
            <Type size={16} />
            <span>Add Text</span>
          </button>
          <button className="flex items-center space-x-2 px-4 py-2 bg-gray-100 rounded-md hover:bg-gray-200">
            <Image size={16} />
            <span>Add Image</span>
          </button>
          <button className="flex items-center space-x-2 px-4 py-2 bg-gray-100 rounded-md hover:bg-gray-200">
            <Square size={16} />
            <span>Add Shape</span>
          </button>
          <button
            onClick={addPage}
            className="flex items-center space-x-2 px-4 py-2 bg-primary-500 text-white rounded-md hover:bg-primary-600"
          >
            <Plus size={16} />
            <span>Add Page</span>
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Pages Editor */}
        <div className="space-y-4">
          <h3 className="text-lg font-semibold text-gray-900">Pages</h3>
          {pages.map((page, index) => (
            <div key={index} className="border border-gray-200 rounded-lg p-4">
              <input
                type="text"
                value={page.title}
                onChange={(e) => updatePage(index, 'title', e.target.value)}
                className="w-full font-semibold text-lg mb-3 px-2 py-1 border-0 border-b border-gray-200 focus:outline-none focus:border-primary-500"
              />
              <textarea
                value={page.content}
                onChange={(e) => updatePage(index, 'content', e.target.value)}
                rows={6}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
              />
            </div>
          ))}
        </div>

        {/* Canvas Preview */}
        <div className="space-y-4">
          <div className="flex justify-between items-center">
            <h3 className="text-lg font-semibold text-gray-900">Preview</h3>
            <button
              onClick={exportToPDF}
              className="flex items-center space-x-2 px-4 py-2 bg-green-500 text-white rounded-md hover:bg-green-600"
            >
              <Download size={16} />
              <span>Export PDF</span>
            </button>
          </div>
          <div className="border border-gray-200 rounded-lg p-4 bg-white">
            <canvas
              ref={canvasRef}
              width={400}
              height={600}
              className="w-full border border-gray-300 rounded"
            />
          </div>
        </div>
      </div>
    </div>
  )
}

export default EbookDesigner