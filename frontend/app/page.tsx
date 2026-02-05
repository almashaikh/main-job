import Link from 'next/link'
import { ArrowRight, Sparkles, Target, TrendingUp, Briefcase } from 'lucide-react'

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-black to-gray-900">
      {/* Navigation */}
      <nav className="border-b border-gray-800 backdrop-blur-sm bg-black/50 fixed w-full z-50 transition-smooth">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-2 group cursor-pointer">
              <Sparkles className="w-8 h-8 text-blue-500 transition-smooth group-hover:animate-bounce-soft" />
              <span className="text-2xl font-bold text-white transition-smooth group-hover:text-blue-400">SkillSphere</span>
            </div>
            <div className="flex items-center space-x-4">
              <Link 
                href="/login"
                className="px-4 py-2 text-gray-300 hover:text-white transition-smooth"
              >
                Login
              </Link>
              <Link 
                href="/login"
                className="px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-smooth hover-lift flex items-center space-x-2 group"
              >
                <span>Get Started</span>
                <ArrowRight className="w-4 h-4 transition-smooth group-hover:translate-x-1" />
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="pt-32 pb-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto text-center">
          <div className="inline-flex items-center space-x-2 px-4 py-2 bg-blue-500/10 border border-blue-500/20 rounded-full mb-8 animate-fade-in">
            <Sparkles className="w-4 h-4 text-blue-400" />
            <span className="text-blue-400 text-sm font-medium">AI-Powered Career Analysis</span>
          </div>
          
          <h1 className="text-5xl md:text-7xl font-bold text-white mb-6 leading-tight animate-slide-up">
            Analyze Your Skills
            <br />
            <span className="bg-gradient-to-r from-blue-400 to-purple-600 bg-clip-text text-transparent">
              Find Your Dream Job
            </span>
          </h1>
          
          <p className="text-xl text-gray-400 mb-12 max-w-3xl mx-auto animate-slide-up" style={{ animationDelay: '0.15s' }}>
            Transform your professional journey with AI-powered skill gap analysis, personalized learning roadmaps, 
            and real-time job opportunities from India's largest job aggregator.
          </p>

          <div className="flex justify-center animate-scale-in" style={{ animationDelay: '0.3s' }}>
            <Link 
              href="/login"
              className="px-8 py-4 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-lg font-semibold transition-smooth hover-lift flex items-center justify-center space-x-2 group"
            >
              <span>Start Free Trial</span>
              <ArrowRight className="w-5 h-5 transition-smooth group-hover:translate-x-1" />
            </Link>
          </div>
        </div>
      </section>

      {/* Features Grid */}
      <section className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16 animate-fade-in">
            <h2 className="text-4xl font-bold text-white mb-4">Everything You Need to Succeed</h2>
            <p className="text-xl text-gray-400">Powerful tools to accelerate your career growth</p>
          </div>

          <div className="grid md:grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Feature 1 - Skill Gap Analyzer */}
            <div className="p-8 bg-gradient-to-br from-gray-800/50 to-gray-900/50 border border-gray-700 rounded-2xl hover:border-green-500/50 transition-smooth group card-hover animate-slide-up">
              <div className="w-12 h-12 bg-green-500/10 rounded-lg flex items-center justify-center mb-4 group-hover:bg-green-500/20 transition-smooth">
                <Target className="w-6 h-6 text-green-400 transition-smooth group-hover:scale-110" />
              </div>
              <h3 className="text-xl font-semibold text-white mb-2">Skill Gap Analyzer</h3>
              <p className="text-gray-400">
                Identify skill gaps and get recommendations to bridge them for your dream role.
              </p>
            </div>

            {/* Feature 2 - Learning Roadmap */}
            <div className="p-8 bg-gradient-to-br from-gray-800/50 to-gray-900/50 border border-gray-700 rounded-2xl hover:border-purple-500/50 transition-smooth group card-hover animate-slide-up" style={{ animationDelay: '0.1s' }}>
              <div className="w-12 h-12 bg-purple-500/10 rounded-lg flex items-center justify-center mb-4 group-hover:bg-purple-500/20 transition-smooth">
                <TrendingUp className="w-6 h-6 text-purple-400 transition-smooth group-hover:scale-110" />
              </div>
              <h3 className="text-xl font-semibold text-white mb-2">Learning Roadmap</h3>
              <p className="text-gray-400">
                Get personalized learning paths tailored to your career goals and current skill level.
              </p>
            </div>

            {/* Feature 3 - Job Opportunities */}
            <div className="p-8 bg-gradient-to-br from-gray-800/50 to-gray-900/50 border border-gray-700 rounded-2xl hover:border-orange-500/50 transition-smooth group card-hover animate-slide-up" style={{ animationDelay: '0.2s' }}>
              <div className="w-12 h-12 bg-orange-500/10 rounded-lg flex items-center justify-center mb-4 group-hover:bg-orange-500/20 transition-smooth">
                <Briefcase className="w-6 h-6 text-orange-400 transition-smooth group-hover:scale-110" />
              </div>
              <h3 className="text-xl font-semibold text-white mb-2">Job Opportunities</h3>
              <p className="text-gray-400">
                Discover real-time job listings from India's largest job aggregator that match your skills and career aspirations.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl mx-auto text-center">
          <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-3xl p-12 card-hover animate-fade-in transition-smooth">
            <h2 className="text-4xl font-bold text-white mb-4">
              Ready to Find Your Next Opportunity?
            </h2>
            <p className="text-xl text-blue-100 mb-8">
              Analyze your skills, discover gaps, and find jobs that match your profile
            </p>
            <Link 
              href="/login"
              className="inline-flex items-center space-x-2 px-8 py-4 bg-white text-blue-600 rounded-lg text-lg font-semibold hover:bg-gray-100 transition-smooth hover-lift group"
            >
              <span>Get Started Now</span>
              <ArrowRight className="w-5 h-5 transition-smooth group-hover:translate-x-1" />
            </Link>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-gray-800 py-12 px-4 sm:px-6 lg:px-8 transition-smooth">
        <div className="max-w-7xl mx-auto text-center">
          <div className="flex items-center justify-center space-x-2 mb-4 group cursor-pointer">
            <Sparkles className="w-6 h-6 text-blue-500 transition-smooth group-hover:animate-bounce-soft" />
            <span className="text-xl font-bold text-white transition-smooth group-hover:text-blue-400">SkillSphere</span>
          </div>
          <p className="text-gray-400 transition-smooth">
            © 2026 SkillSphere. All rights reserved.
          </p>
        </div>
      </footer>
    </div>
  )
}
