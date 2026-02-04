'use client'

import { useState, useEffect, useRef } from 'react'
import Link from 'next/link'
import { Send, MessageCircle, X, RotateCcw } from 'lucide-react'

interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  category?: string
  timestamp: Date
}

interface ChatbotResponse {
  response: string
  category: string
  confidence: number
  is_in_scope: boolean
}

export default function ChatbotPage() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      role: 'assistant',
      content: "👋 Welcome to AI Career Copilot! I'm here to help you understand your skill gaps, guide your learning, and assess your interview readiness. What would you like to know?",
      timestamp: new Date(),
    }
  ])
  const [inputValue, setInputValue] = useState('')
  const [loading, setLoading] = useState(false)
  const [gapAnalysis, setGapAnalysis] = useState<any>(null)
  const [userProgress, setUserProgress] = useState<any>(null)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  // Load gap analysis data from sessionStorage or localStorage
  useEffect(() => {
    const savedGapAnalysis = sessionStorage.getItem('gapAnalysis') || localStorage.getItem('gapAnalysis')
    if (savedGapAnalysis) {
      try {
        setGapAnalysis(JSON.parse(savedGapAnalysis))
      } catch (e) {
        console.error('Error loading gap analysis:', e)
      }
    }

    const savedProgress = sessionStorage.getItem('userProgress') || localStorage.getItem('userProgress')
    if (savedProgress) {
      try {
        setUserProgress(JSON.parse(savedProgress))
      } catch (e) {
        console.error('Error loading user progress:', e)
      }
    }
  }, [])

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!inputValue.trim()) return

    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: inputValue,
      timestamp: new Date(),
    }
    
    setMessages(prev => [...prev, userMessage])
    setInputValue('')
    setLoading(true)

    try {
      // Call chatbot API
      const response = await fetch('http://localhost:8000/api/chatbot/message', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: inputValue,
          gap_analysis: gapAnalysis || {},
          user_progress: userProgress,
          user_name: localStorage.getItem('userName'),
          is_recruiter: localStorage.getItem('userRole') === 'recruiter',
        }),
      })

      if (!response.ok) {
        throw new Error('Failed to get response from chatbot')
      }

      const data: ChatbotResponse = await response.json()

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: data.response,
        category: data.category,
        timestamp: new Date(),
      }

      setMessages(prev => [...prev, assistantMessage])
    } catch (error) {
      console.error('Error:', error)
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: "Sorry, I encountered an error processing your message. Please try again.",
        timestamp: new Date(),
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setLoading(false)
    }
  }

  const handleClearHistory = async () => {
    try {
      await fetch('http://localhost:8000/api/chatbot/clear', {
        method: 'POST',
      })
      setMessages([
        {
          id: '1',
          role: 'assistant',
          content: "👋 Welcome to AI Career Copilot! I'm here to help you understand your skill gaps, guide your learning, and assess your interview readiness. What would you like to know?",
          timestamp: new Date(),
        }
      ])
    } catch (error) {
      console.error('Error clearing history:', error)
    }
  }

  const hasGapAnalysis = gapAnalysis && Object.keys(gapAnalysis).length > 0

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 to-slate-800">
      {/* Header */}
      <div className="border-b border-slate-700 bg-slate-800/50 backdrop-blur-sm">
        <div className="max-w-6xl mx-auto px-4 py-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <MessageCircle className="w-8 h-8 text-blue-400" />
              <div>
                <h1 className="text-2xl font-bold text-white">AI Career Copilot</h1>
                <p className="text-sm text-slate-400">Domain-Specific Career Assistant</p>
              </div>
            </div>
            <Link
              href="/dashboard/gap-analyzer"
              className="px-4 py-2 bg-slate-700 hover:bg-slate-600 text-white rounded-lg transition"
            >
              Back to Dashboard
            </Link>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-4xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
        {/* Info Card */}
        {!hasGapAnalysis && (
          <div className="mb-6 p-4 bg-yellow-900/30 border border-yellow-700 rounded-lg">
            <p className="text-yellow-100 text-sm">
              💡 <strong>Tip:</strong> First, run a gap analysis to unlock personalized guidance. Your skill gaps, learning roadmap, and interview readiness will help me provide better answers.
            </p>
          </div>
        )}

        {/* Chat Container */}
        <div className="h-[600px] flex flex-col bg-slate-700/50 border border-slate-600 rounded-lg overflow-hidden">
          {/* Messages Area */}
          <div className="flex-1 overflow-y-auto p-4 sm:p-6 space-y-4">
            {messages.map(message => (
              <div
                key={message.id}
                className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-[80%] p-3 sm:p-4 rounded-lg ${
                    message.role === 'user'
                      ? 'bg-blue-600 text-white rounded-br-none'
                      : 'bg-slate-600 text-slate-100 rounded-bl-none'
                  }`}
                >
                  <p className="text-sm sm:text-base whitespace-pre-wrap leading-relaxed">
                    {message.content}
                  </p>
                  <p className={`text-xs mt-1 ${
                    message.role === 'user' ? 'text-blue-100' : 'text-slate-400'
                  }`}>
                    {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </p>
                </div>
              </div>
            ))}
            {loading && (
              <div className="flex justify-start">
                <div className="bg-slate-600 text-slate-100 p-4 rounded-lg rounded-bl-none">
                  <div className="flex gap-2">
                    <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce" />
                    <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }} />
                    <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }} />
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Input Area */}
          <div className="border-t border-slate-600 bg-slate-800 p-4">
            <form onSubmit={handleSendMessage} className="flex gap-3">
              <input
                type="text"
                value={inputValue}
                onChange={e => setInputValue(e.target.value)}
                placeholder="Ask me about your skills, learning roadmap, or interview readiness..."
                disabled={loading}
                className="flex-1 bg-slate-700 text-white placeholder-slate-400 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
              />
              <button
                type="submit"
                disabled={loading || !inputValue.trim()}
                className="p-2 bg-blue-600 hover:bg-blue-700 disabled:bg-slate-600 disabled:opacity-50 text-white rounded-lg transition"
              >
                <Send className="w-5 h-5" />
              </button>
              <button
                type="button"
                onClick={handleClearHistory}
                className="p-2 bg-slate-600 hover:bg-slate-500 text-white rounded-lg transition"
                title="Clear conversation history"
              >
                <RotateCcw className="w-5 h-5" />
              </button>
            </form>
          </div>
        </div>

        {/* Example Questions */}
        <div className="mt-6 p-4 bg-slate-700/50 border border-slate-600 rounded-lg">
          <h3 className="text-sm font-semibold text-slate-200 mb-3">💬 Example Questions:</h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
            <button
              onClick={() => setInputValue('Why is Docker important for me?')}
              className="text-left text-sm p-2 bg-slate-600 hover:bg-slate-500 text-slate-100 rounded transition"
            >
              "Why is Docker important for me?"
            </button>
            <button
              onClick={() => setInputValue('What should I learn next?')}
              className="text-left text-sm p-2 bg-slate-600 hover:bg-slate-500 text-slate-100 rounded transition"
            >
              "What should I learn next?"
            </button>
            <button
              onClick={() => setInputValue('How much progress have I made?')}
              className="text-left text-sm p-2 bg-slate-600 hover:bg-slate-500 text-slate-100 rounded transition"
            >
              "How much progress have I made?"
            </button>
            <button
              onClick={() => setInputValue('Am I interview ready?')}
              className="text-left text-sm p-2 bg-slate-600 hover:bg-slate-500 text-slate-100 rounded transition"
            >
              "Am I interview ready?"
            </button>
          </div>
        </div>

        {/* Feature Description */}
        <div className="mt-6 p-4 bg-blue-900/20 border border-blue-700/50 rounded-lg">
          <h3 className="font-semibold text-blue-100 mb-2">About AI Career Copilot</h3>
          <ul className="text-sm text-blue-100/80 space-y-1 list-disc list-inside">
            <li>Domain-specific assistant for skill gap analysis and career development</li>
            <li>Provides explanations based on your gap analysis and market data</li>
            <li>Guides your learning roadmap and prioritizes skill development</li>
            <li>Assesses interview readiness and recruitment suitability</li>
            <li>Professional, data-driven responses with no hallucinations</li>
          </ul>
        </div>
      </div>
    </div>
  )
}
