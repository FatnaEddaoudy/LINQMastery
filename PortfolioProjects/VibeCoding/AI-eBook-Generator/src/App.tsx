import { BookOpen } from 'lucide-react'
import Header from './components/Header'
import EbookDesigner from './components/EbookDesigner'

function App() {
  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      
      <div className="container mx-auto px-4 py-8">
        {/* Header Section */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center space-x-3 mb-4">
            <BookOpen size={48} className="text-primary-500" />
            <h1 className="text-4xl font-bold text-gray-900">AI eBook Generator</h1>
          </div>
          <p className="text-xl text-gray-600">Create complete eBooks with full content and custom backgrounds!</p>
        </div>

        {/* Main Content */}
        <div className="bg-white rounded-lg shadow-lg">
          <EbookDesigner />
        </div>
      </div>
    </div>
  )
}

export default App