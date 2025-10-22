import { Sparkles } from 'lucide-react'

const Header = () => {
  return (
    <header className="bg-white shadow-sm border-b">
      <div className="container mx-auto px-4 py-6">
        <div className="flex items-center space-x-3">
          <div className="p-2 bg-primary-500 rounded-lg">
            <Sparkles className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-gray-900">GeneratorAI</h1>
            <p className="text-gray-600">Create eBooks, Videos & Designs with AI</p>
          </div>
        </div>
      </div>
    </header>
  )
}

export default Header