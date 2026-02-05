'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { 
  Sparkles, 
  User, 
  Briefcase, 
  FileText, 
  TrendingUp, 
  Target, 
  BookOpen, 
  MessageSquare,
  Bell,
  Search,
  Settings,
  LogOut,
  Menu,
  X
} from 'lucide-react'
import { useState } from 'react'

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const pathname = usePathname()
  const [sidebarOpen, setSidebarOpen] = useState(false)

  const navigation = [
    { name: 'Gap Analyzer', href: '/dashboard/gap-analyzer', icon: Target },
    { name: 'Learning Roadmap', href: '/dashboard/roadmap', icon: TrendingUp },
    { name: 'Job Opportunities', href: '/dashboard/job-opportunities', icon: Briefcase },
  ]

  return (
    <div className="min-h-screen bg-black">
      {/* Mobile Sidebar Overlay */}
      {sidebarOpen && (
        <div 
          className="fixed inset-0 bg-black/50 backdrop-blur-sm z-40 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Sidebar */}
      <aside className={`
        fixed top-0 left-0 h-full bg-[#0f0f0f] border-r border-gray-800 w-64 z-50 transition-transform duration-300 ease-in-out
        ${sidebarOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}
      `}>
        <div className="flex flex-col h-full">
          {/* Logo */}
          <div className="h-16 flex items-center justify-between px-6 border-b border-gray-800">
            <Link href="/" className="flex items-center space-x-2 group cursor-pointer">
              <Sparkles className="w-6 h-6 text-blue-500 transition-smooth group-hover:animate-bounce-soft" />
              <span className="text-xl font-bold text-white transition-smooth group-hover:text-blue-400">SkillSphere</span>
            </Link>
            <button
              onClick={() => setSidebarOpen(false)}
              className="lg:hidden text-gray-400 hover:text-white"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          {/* Navigation */}
          <nav className="flex-1 overflow-y-auto py-4 px-3">
            <div className="space-y-1">
              {navigation.map((item) => {
                const isActive = pathname === item.href
                const Icon = item.icon
                return (
                  <Link
                    key={item.name}
                    href={item.href}
                    onClick={() => setSidebarOpen(false)}
                    className={`
                      flex items-center space-x-3 px-3 py-2.5 rounded-lg transition-smooth group relative overflow-hidden
                      ${isActive 
                        ? 'bg-gradient-to-r from-blue-600 to-blue-700 text-white shadow-lg shadow-blue-600/50' 
                        : 'text-gray-400 hover:bg-gray-800/80 hover:text-white'
                      }
                    `}
                  >
                    <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white to-transparent opacity-0 group-hover:opacity-10 translate-x-[-100%] group-hover:translate-x-[100%] transition-all duration-500"></div>
                    <Icon className={`w-5 h-5 flex-shrink-0 transition-smooth ${isActive ? 'group-hover:scale-110' : 'group-hover:scale-120'}`} />
                    <span className="text-sm font-medium">{item.name}</span>
                  </Link>
                )
              })}
            </div>
          </nav>

          {/* User Profile */}
          <div className="p-4 border-t border-gray-800">
            <div className="flex items-center space-x-3 mb-3">
              <div className="w-10 h-10 rounded-full bg-gradient-to-r from-blue-500 to-purple-600 flex items-center justify-center text-white font-semibold transition-smooth hover-scale hover-glow cursor-pointer">
                JD
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-white truncate">John Doe</p>
                <p className="text-xs text-gray-400 truncate">john@example.com</p>
              </div>
            </div>
            <div className="flex space-x-2">
              <button className="flex-1 flex items-center justify-center space-x-2 px-3 py-2 bg-gray-800 hover:bg-gray-700 rounded-lg text-sm text-gray-300 transition-smooth hover-lift group">
                <Settings className="w-4 h-4 transition-smooth group-hover:rotate-90" />
                <span>Settings</span>
              </button>
              <Link 
                href="/login"
                className="flex items-center justify-center px-3 py-2 bg-gray-800 hover:bg-gray-700 rounded-lg text-gray-300 transition-smooth hover-lift group"
              >
                <LogOut className="w-4 h-4 transition-smooth group-hover:scale-110" />
              </Link>
            </div>
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <div className="lg:pl-64">
        {/* Top Header */}
        <header className="h-16 bg-[#0f0f0f] border-b border-gray-800 fixed top-0 right-0 left-0 lg:left-64 z-30">
          <div className="h-full px-4 sm:px-6 lg:px-8 flex items-center justify-between">
            <button
              onClick={() => setSidebarOpen(true)}
              className="lg:hidden text-gray-400 hover:text-white"
            >
              <Menu className="w-6 h-6" />
            </button>

            <div className="flex-1"></div>

            {/* Right Section */}
            <div className="flex items-center space-x-4">
              <button className="relative p-2 text-gray-400 hover:text-white transition-smooth group">
                <Bell className="w-5 h-5 transition-smooth group-hover:animate-bounce-soft" />
                <span className="absolute top-1 right-1 w-2 h-2 bg-blue-500 rounded-full animate-pulse"></span>
              </button>
            </div>
          </div>
        </header>

        {/* Page Content */}
        <main className="pt-16 min-h-screen">
          {children}
        </main>
      </div>
    </div>
  )
}
