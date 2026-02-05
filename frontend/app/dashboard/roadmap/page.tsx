'use client'

import { useState, useEffect } from 'react'
import { 
  BookOpen, Target, Clock, CheckCircle2, ArrowRight, 
  TrendingUp, Lightbulb, ExternalLink, Play, FileText,
  AlertCircle, Loader2, Code, Video, FileCode, Star,
  Calendar, Award, Zap, ChevronDown, ChevronUp
} from 'lucide-react'

interface Prerequisite {
  name: string
  importance: string
  estimated_time: string
  description: string
  resources?: Resource[]
}

interface LearningStage {
  stage: number
  name: string
  skills: string[]
  topics: string[]
  estimated_time: string
  description: string
  resources?: Resource[]
}

interface Project {
  name: string
  difficulty: string
  description: string
  skills_practiced: string[]
}

interface Resource {
  title: string
  platform: string
  type: string
  url: string
  difficulty: string
  duration: string
  description: string
  rating: string
  is_free: boolean
}

interface Roadmap {
  skill: string
  level: string
  prerequisites: Prerequisite[]
  learning_path: LearningStage[]
  projects: Project[]
  resources_needed: Array<{ category: string; items: string[] }>
  metadata: {
    generated_at: string
    total_prerequisites: number
    total_stages: number
    total_projects: number
    estimated_total_time: string
  }
  mermaid_diagram?: string
}

export default function RoadmapPage() {
  const [skill, setSkill] = useState('')
  const [level, setLevel] = useState<'beginner' | 'intermediate' | 'advanced'>('beginner')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [roadmap, setRoadmap] = useState<Roadmap | null>(null)
  const [availabilityChecked, setAvailabilityChecked] = useState(false)
  const [isAvailable, setIsAvailable] = useState(false)
  const [expandedStages, setExpandedStages] = useState<Set<number>>(new Set())
  const [activeTab, setActiveTab] = useState<'overview' | 'prerequisites' | 'path' | 'projects'>('overview')

  const API_BASE = 'http://localhost:8000'

  useEffect(() => {
    checkAvailability()
  }, [])

  const checkAvailability = async () => {
    try {
      const response = await fetch(`${API_BASE}/api/roadmap/check-availability`)
      const data = await response.json()
      setIsAvailable(data.available)
      if (!data.available) {
        setError(data.message)
      }
      setAvailabilityChecked(true)
    } catch (err) {
      setError('Could not connect to backend')
      setAvailabilityChecked(true)
    }
  }

  const handleGenerateRoadmap = async () => {
    if (!skill.trim()) {
      setError('Please enter a skill to learn')
      return
    }

    setLoading(true)
    setError('')

    try {
      const response = await fetch(`${API_BASE}/api/generate-roadmap`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          skill: skill.trim(),
          level: level,
        }),
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Failed to generate roadmap')
      }

      const data = await response.json()
      setRoadmap(data)
      setActiveTab('overview')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error generating roadmap')
    } finally {
      setLoading(false)
    }
  }

  const toggleStage = (stageNumber: number) => {
    const newExpanded = new Set(expandedStages)
    if (newExpanded.has(stageNumber)) {
      newExpanded.delete(stageNumber)
    } else {
      newExpanded.add(stageNumber)
    }
    setExpandedStages(newExpanded)
  }

  const getImportanceColor = (importance: string) => {
    switch (importance.toLowerCase()) {
      case 'critical':
        return 'text-red-400 bg-red-500/10 border-red-500/30'
      case 'important':
        return 'text-orange-400 bg-orange-500/10 border-orange-500/30'
      case 'recommended':
        return 'text-yellow-400 bg-yellow-500/10 border-yellow-500/30'
      default:
        return 'text-gray-400 bg-gray-500/10 border-gray-500/30'
    }
  }

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty.toLowerCase()) {
      case 'beginner':
        return 'text-green-400 bg-green-500/10 border-green-500/30'
      case 'intermediate':
        return 'text-yellow-400 bg-yellow-500/10 border-yellow-500/30'
      case 'advanced':
        return 'text-red-400 bg-red-500/10 border-red-500/30'
      default:
        return 'text-gray-400 bg-gray-500/10 border-gray-500/30'
    }
  }

  const getResourceIcon = (type: string) => {
    switch (type.toLowerCase()) {
      case 'video':
        return <Video className="w-4 h-4" />
      case 'course':
        return <BookOpen className="w-4 h-4" />
      case 'article':
        return <FileText className="w-4 h-4" />
      case 'documentation':
        return <FileCode className="w-4 h-4" />
      case 'interactive':
        return <Code className="w-4 h-4" />
      default:
        return <ExternalLink className="w-4 h-4" />
    }
  }

  if (!availabilityChecked) {
    return (
      <div className="p-6 lg:p-8">
        <div className="max-w-7xl mx-auto">
          <div className="text-center py-20">
            <Loader2 className="w-12 h-12 text-blue-400 animate-spin mx-auto" />
            <p className="text-gray-400 mt-4">Checking service availability...</p>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="p-6 lg:p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-10 text-center">
          <h1 className="text-4xl font-bold text-white mb-2">AI Learning Roadmap</h1>
          <p className="text-gray-400 text-lg">
            Generate personalized learning paths with AI-powered recommendations
          </p>
        </div>

        {/* Input Section */}
        <div className="bg-gray-800/50 backdrop-blur-sm rounded-xl border border-gray-700 p-6 mb-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Skill Input */}
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                What do you want to learn?
              </label>
              <input
                type="text"
                value={skill}
                onChange={(e) => setSkill(e.target.value)}
                placeholder="e.g., React, Python, Data Science, Machine Learning"
                className="w-full px-4 py-3 bg-gray-900/50 border border-gray-600 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
                disabled={loading || !isAvailable}
              />
            </div>

            {/* Level Selection */}
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Your current level
              </label>
              <div className="grid grid-cols-3 gap-2">
                {(['beginner', 'intermediate', 'advanced'] as const).map((lvl) => (
                  <button
                    key={lvl}
                    onClick={() => setLevel(lvl)}
                    disabled={loading || !isAvailable}
                    className={`px-4 py-3 rounded-lg font-medium transition-all ${
                      level === lvl
                        ? 'bg-blue-500 text-white border-2 border-blue-400'
                        : 'bg-gray-900/50 text-gray-400 border border-gray-600 hover:border-gray-500'
                    } ${loading || !isAvailable ? 'opacity-50 cursor-not-allowed' : ''}`}
                  >
                    {lvl.charAt(0).toUpperCase() + lvl.slice(1)}
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* Generate Button */}
          <button
            onClick={handleGenerateRoadmap}
            disabled={loading || !isAvailable || !skill.trim()}
            className="mt-6 w-full px-6 py-3 bg-gradient-to-r from-blue-500 to-purple-500 text-white rounded-lg font-medium hover:from-blue-600 hover:to-purple-600 transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
          >
            {loading ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                Generating your personalized roadmap...
              </>
            ) : (
              <>
                <Zap className="w-5 h-5" />
                Generate Learning Roadmap
              </>
            )}
          </button>

          {/* Error Message */}
          {error && (
            <div className="mt-4 p-4 bg-red-500/10 border border-red-500/30 rounded-lg flex items-start gap-3">
              <AlertCircle className="w-5 h-5 text-red-400 flex-shrink-0 mt-0.5" />
              <div className="text-red-400 text-sm">{error}</div>
            </div>
          )}
        </div>

        {/* Roadmap Display */}
        {roadmap && (
          <div className="space-y-6">
            {/* Summary Cards */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div className="bg-gradient-to-br from-blue-500/20 to-blue-600/20 border border-blue-500/30 rounded-xl p-4">
                <div className="flex items-center justify-between mb-2">
                  <Clock className="w-8 h-8 text-blue-400" />
                </div>
                <div className="text-2xl font-bold text-white">
                  {roadmap.metadata.estimated_total_time}
                </div>
                <div className="text-sm text-blue-300">Total Time</div>
              </div>

              <div className="bg-gradient-to-br from-purple-500/20 to-purple-600/20 border border-purple-500/30 rounded-xl p-4">
                <div className="flex items-center justify-between mb-2">
                  <CheckCircle2 className="w-8 h-8 text-purple-400" />
                </div>
                <div className="text-2xl font-bold text-white">
                  {roadmap.metadata.total_prerequisites}
                </div>
                <div className="text-sm text-purple-300">Prerequisites</div>
              </div>

              <div className="bg-gradient-to-br from-green-500/20 to-green-600/20 border border-green-500/30 rounded-xl p-4">
                <div className="flex items-center justify-between mb-2">
                  <TrendingUp className="w-8 h-8 text-green-400" />
                </div>
                <div className="text-2xl font-bold text-white">
                  {roadmap.metadata.total_stages}
                </div>
                <div className="text-sm text-green-300">Learning Stages</div>
              </div>

              <div className="bg-gradient-to-br from-orange-500/20 to-orange-600/20 border border-orange-500/30 rounded-xl p-4">
                <div className="flex items-center justify-between mb-2">
                  <Code className="w-8 h-8 text-orange-400" />
                </div>
                <div className="text-2xl font-bold text-white">
                  {roadmap.metadata.total_projects}
                </div>
                <div className="text-sm text-orange-300">Project Ideas</div>
              </div>
            </div>

            {/* Tabs */}
            <div className="bg-gray-800/50 backdrop-blur-sm rounded-xl border border-gray-700 overflow-hidden">
              <div className="flex border-b border-gray-700">
                {[
                  { id: 'overview', label: 'Overview', icon: Target },
                  { id: 'prerequisites', label: 'Prerequisites', icon: CheckCircle2 },
                  { id: 'path', label: 'Learning Path', icon: TrendingUp },
                  { id: 'projects', label: 'Projects', icon: Code },
                ].map((tab) => (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id as any)}
                    className={`flex-1 px-6 py-4 flex items-center justify-center gap-2 font-medium transition-all ${
                      activeTab === tab.id
                        ? 'bg-blue-500/20 text-blue-400 border-b-2 border-blue-400'
                        : 'text-gray-400 hover:text-gray-300 hover:bg-gray-700/30'
                    }`}
                  >
                    <tab.icon className="w-5 h-5" />
                    {tab.label}
                  </button>
                ))}
              </div>

              <div className="p-6">
                {/* Overview Tab */}
                {activeTab === 'overview' && (
                  <div className="space-y-6">
                    <div>
                      <h2 className="text-2xl font-bold text-white mb-2">
                        Learning Roadmap: {roadmap.skill}
                      </h2>
                      <p className="text-gray-400">
                        Level: <span className="text-blue-400 font-medium capitalize">{roadmap.level}</span>
                      </p>
                    </div>

                    {roadmap.resources_needed && roadmap.resources_needed.length > 0 && (
                      <div className="bg-gray-900/50 rounded-lg p-5 border border-gray-700">
                        <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                          <Lightbulb className="w-5 h-5 text-yellow-400" />
                          Resources You'll Need
                        </h3>
                        <div className="space-y-4">
                          {roadmap.resources_needed.map((category, idx) => (
                            <div key={idx}>
                              <h4 className="text-sm font-medium text-gray-300 mb-2">
                                {category.category}
                              </h4>
                              <ul className="space-y-1">
                                {category.items.map((item, itemIdx) => (
                                  <li key={itemIdx} className="text-gray-400 text-sm flex items-center gap-2">
                                    <div className="w-1.5 h-1.5 rounded-full bg-blue-400" />
                                    {item}
                                  </li>
                                ))}
                              </ul>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                      <div className="bg-purple-500/10 border border-purple-500/30 rounded-lg p-4">
                        <div className="text-3xl font-bold text-purple-400 mb-1">
                          {roadmap.prerequisites.length}
                        </div>
                        <div className="text-sm text-gray-400">Skills to learn first</div>
                      </div>
                      <div className="bg-blue-500/10 border border-blue-500/30 rounded-lg p-4">
                        <div className="text-3xl font-bold text-blue-400 mb-1">
                          {roadmap.learning_path.length}
                        </div>
                        <div className="text-sm text-gray-400">Learning stages</div>
                      </div>
                      <div className="bg-green-500/10 border border-green-500/30 rounded-lg p-4">
                        <div className="text-3xl font-bold text-green-400 mb-1">
                          {roadmap.projects.length}
                        </div>
                        <div className="text-sm text-gray-400">Hands-on projects</div>
                      </div>
                    </div>
                  </div>
                )}

                {/* Prerequisites Tab */}
                {activeTab === 'prerequisites' && (
                  <div className="space-y-4">
                    <div className="mb-6">
                      <h3 className="text-xl font-semibold text-white mb-2">
                        Prerequisites
                      </h3>
                      <p className="text-gray-400">
                        Skills you should know before starting
                      </p>
                    </div>

                    {roadmap.prerequisites.map((prereq, idx) => (
                      <div
                        key={idx}
                        className="bg-gray-900/50 rounded-lg p-5 border border-gray-700 hover:border-gray-600 transition-all"
                      >
                        <div className="flex items-start justify-between mb-3">
                          <div className="flex-1">
                            <h4 className="text-lg font-semibold text-white mb-2">
                              {prereq.name}
                            </h4>
                            <p className="text-gray-400 text-sm mb-3">
                              {prereq.description}
                            </p>
                            <div className="flex items-center gap-3">
                              <span className={`px-3 py-1 rounded-full text-xs font-medium border ${getImportanceColor(prereq.importance)}`}>
                                {prereq.importance}
                              </span>
                              <span className="flex items-center gap-1 text-gray-400 text-sm">
                                <Clock className="w-4 h-4" />
                                {prereq.estimated_time}
                              </span>
                            </div>
                          </div>
                        </div>

                        {/* Resources */}
                        {prereq.resources && prereq.resources.length > 0 && (
                          <div className="mt-4 pt-4 border-t border-gray-700">
                            <h5 className="text-sm font-medium text-gray-300 mb-3">
                              Recommended Resources
                            </h5>
                            <div className="space-y-2">
                              {prereq.resources.map((resource, resIdx) => (
                                <a
                                  key={resIdx}
                                  href={resource.url}
                                  target="_blank"
                                  rel="noopener noreferrer"
                                  className="flex items-center justify-between p-3 bg-gray-800/50 rounded-lg hover:bg-gray-800 transition-all border border-gray-700 hover:border-gray-600 group"
                                >
                                  <div className="flex items-center gap-3">
                                    <div className="text-blue-400">
                                      {getResourceIcon(resource.type)}
                                    </div>
                                    <div>
                                      <div className="text-white text-sm font-medium group-hover:text-blue-400 transition-colors">
                                        {resource.title}
                                      </div>
                                      <div className="text-gray-500 text-xs">
                                        {resource.platform} • {resource.duration}
                                        {resource.is_free && ' • Free'}
                                      </div>
                                    </div>
                                  </div>
                                  <ExternalLink className="w-4 h-4 text-gray-500 group-hover:text-blue-400 transition-colors" />
                                </a>
                              ))}
                            </div>
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                )}

                {/* Learning Path Tab */}
                {activeTab === 'path' && (
                  <div className="space-y-4">
                    <div className="mb-6">
                      <h3 className="text-xl font-semibold text-white mb-2">
                        Learning Path
                      </h3>
                      <p className="text-gray-400">
                        Follow these stages in order to master {roadmap.skill}
                      </p>
                    </div>

                    {roadmap.learning_path.map((stage, idx) => (
                      <div
                        key={idx}
                        className="bg-gray-900/50 rounded-lg border border-gray-700 hover:border-gray-600 transition-all overflow-hidden"
                      >
                        <button
                          onClick={() => toggleStage(stage.stage)}
                          className="w-full p-5 flex items-center justify-between hover:bg-gray-800/30 transition-all"
                        >
                          <div className="flex items-center gap-4">
                            <div className="w-10 h-10 rounded-full bg-blue-500/20 border border-blue-500/30 flex items-center justify-center text-blue-400 font-bold">
                              {stage.stage}
                            </div>
                            <div className="text-left">
                              <h4 className="text-lg font-semibold text-white mb-1">
                                {stage.name}
                              </h4>
                              <div className="flex items-center gap-3 text-sm text-gray-400">
                                <span className="flex items-center gap-1">
                                  <Clock className="w-4 h-4" />
                                  {stage.estimated_time}
                                </span>
                                <span>•</span>
                                <span>{stage.topics.length} topics</span>
                              </div>
                            </div>
                          </div>
                          {expandedStages.has(stage.stage) ? (
                            <ChevronUp className="w-5 h-5 text-gray-400" />
                          ) : (
                            <ChevronDown className="w-5 h-5 text-gray-400" />
                          )}
                        </button>

                        {expandedStages.has(stage.stage) && (
                          <div className="px-5 pb-5 space-y-4">
                            <p className="text-gray-400 text-sm">
                              {stage.description}
                            </p>

                            {/* Topics */}
                            <div>
                              <h5 className="text-sm font-medium text-gray-300 mb-2">
                                Topics to Cover
                              </h5>
                              <div className="flex flex-wrap gap-2">
                                {stage.topics.map((topic, topicIdx) => (
                                  <span
                                    key={topicIdx}
                                    className="px-3 py-1 bg-gray-800 border border-gray-700 rounded-full text-sm text-gray-300"
                                  >
                                    {topic}
                                  </span>
                                ))}
                              </div>
                            </div>

                            {/* Skills */}
                            {stage.skills && stage.skills.length > 0 && (
                              <div>
                                <h5 className="text-sm font-medium text-gray-300 mb-2">
                                  Skills You'll Learn
                                </h5>
                                <div className="flex flex-wrap gap-2">
                                  {stage.skills.map((skill, skillIdx) => (
                                    <span
                                      key={skillIdx}
                                      className="px-3 py-1 bg-blue-500/10 border border-blue-500/30 rounded-full text-sm text-blue-400"
                                    >
                                      {skill}
                                    </span>
                                  ))}
                                </div>
                              </div>
                            )}

                            {/* Resources */}
                            {stage.resources && stage.resources.length > 0 && (
                              <div>
                                <h5 className="text-sm font-medium text-gray-300 mb-3">
                                  Learning Resources
                                </h5>
                                <div className="space-y-2">
                                  {stage.resources.map((resource, resIdx) => (
                                    <a
                                      key={resIdx}
                                      href={resource.url}
                                      target="_blank"
                                      rel="noopener noreferrer"
                                      className="flex items-center justify-between p-3 bg-gray-800/50 rounded-lg hover:bg-gray-800 transition-all border border-gray-700 hover:border-gray-600 group"
                                    >
                                      <div className="flex items-center gap-3">
                                        <div className="text-blue-400">
                                          {getResourceIcon(resource.type)}
                                        </div>
                                        <div>
                                          <div className="text-white text-sm font-medium group-hover:text-blue-400 transition-colors">
                                            {resource.title}
                                          </div>
                                          <div className="text-gray-500 text-xs flex items-center gap-2">
                                            <span>{resource.platform}</span>
                                            <span>•</span>
                                            <span>{resource.duration}</span>
                                            {resource.is_free && (
                                              <>
                                                <span>•</span>
                                                <span className="text-green-400">Free</span>
                                              </>
                                            )}
                                            {resource.rating && (
                                              <>
                                                <span>•</span>
                                                <span className="flex items-center gap-1">
                                                  <Star className="w-3 h-3 text-yellow-400 fill-yellow-400" />
                                                  {resource.rating}
                                                </span>
                                              </>
                                            )}
                                          </div>
                                        </div>
                                      </div>
                                      <ExternalLink className="w-4 h-4 text-gray-500 group-hover:text-blue-400 transition-colors" />
                                    </a>
                                  ))}
                                </div>
                              </div>
                            )}
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                )}

                {/* Projects Tab */}
                {activeTab === 'projects' && (
                  <div className="space-y-4">
                    <div className="mb-6">
                      <h3 className="text-xl font-semibold text-white mb-2">
                        Project Ideas
                      </h3>
                      <p className="text-gray-400">
                        Build these projects to practice your skills
                      </p>
                    </div>

                    {roadmap.projects.map((project, idx) => (
                      <div
                        key={idx}
                        className="bg-gray-900/50 rounded-lg p-5 border border-gray-700 hover:border-gray-600 transition-all"
                      >
                        <div className="flex items-start justify-between mb-3">
                          <div className="flex-1">
                            <div className="flex items-center gap-3 mb-2">
                              <h4 className="text-lg font-semibold text-white">
                                {project.name}
                              </h4>
                              <span className={`px-3 py-1 rounded-full text-xs font-medium border ${getDifficultyColor(project.difficulty)}`}>
                                {project.difficulty}
                              </span>
                            </div>
                            <p className="text-gray-400 text-sm mb-4">
                              {project.description}
                            </p>
                            <div>
                              <h5 className="text-sm font-medium text-gray-300 mb-2">
                                Skills Practiced
                              </h5>
                              <div className="flex flex-wrap gap-2">
                                {project.skills_practiced.map((skill, skillIdx) => (
                                  <span
                                    key={skillIdx}
                                    className="px-3 py-1 bg-green-500/10 border border-green-500/30 rounded-full text-sm text-green-400"
                                  >
                                    {skill}
                                  </span>
                                ))}
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
