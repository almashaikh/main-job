'use client'

import { useEffect, useRef, useState } from 'react'
import { Upload, FileText, Search, Target, TrendingUp, AlertCircle, CheckCircle2, XCircle, Loader2, Star, Lightbulb, AlertTriangle } from 'lucide-react'

interface ResumeData {
  skills: string[]
  name?: string
  email?: string
  phone?: string
  experience_years?: number
  raw_text?: string
}

interface ResumeFeedback {
  overall_score: number
  skill_density_analysis: {
    score: number
    status: string
    density_percentage: number
    unique_skills: number
    details: string
    top_skills: string[]
  }
  impact_words_analysis: {
    score: number
    status: string
    found_words: Record<string, string[]>
    missing_words: Record<string, string[]>
    priority_missing: string[]
    total_impact_words_found: number
    categories_with_words: number
  }
  formatting_analysis: {
    score: number
    status: string
    issues: string[]
    word_count: number
    contact_info_found: Record<string, boolean>
    details: string
    bullet_points: number
    sections_found: number
  }
  relevance_analysis: {
    score: number
    status: string
    matched_skills: number
    missing_critical_skills: string[]
  }
  improvement_suggestions: Array<{
    category: string
    priority: string
    suggestion: string
    impact: string
  }>
}

interface GapAnalysisResult {
  match_percentage: number
  readiness_score: number
  overall_readiness: string
  matched_skills_detailed: Array<{
    skill: string
    user_level: string
    market_demand: string
    percentage: number
  }>
  skill_gaps: {
    critical: Array<{ skill: string; percentage: number; demand_level: string }>
    high: Array<{ skill: string; percentage: number; demand_level: string }>
    medium: Array<{ skill: string; percentage: number; demand_level: string }>
    low: Array<{ skill: string; percentage: number; demand_level: string }>
  }
  total_gaps_by_priority: {
    critical: number
    high: number
    medium: number
    low: number
  }
  recommendations: string[]
}

interface JobMatchResult {
  match_percentage: number
  readiness: string
  recommendation: string
  user_name?: string
  matched_skills: string[]
  missing_skills: string[]
  total_required: number
  total_matched: number
}

export default function GapAnalyzer() {
  const STORAGE_KEY = 'gapAnalyzerState'
  const resumeInputRef = useRef<HTMLInputElement | null>(null)
  const jobDescInputRef = useRef<HTMLInputElement | null>(null)
  const [analysisMethod, setAnalysisMethod] = useState<'job-description' | 'market-data'>('market-data')
  const [jobDescInputMethod, setJobDescInputMethod] = useState<'text' | 'pdf'>('text')
  const [resumeFile, setResumeFile] = useState<File | null>(null)
  const [resumeData, setResumeData] = useState<ResumeData | null>(null)
  const [resumeFeedback, setResumeFeedback] = useState<ResumeFeedback | null>(null)
  const [jobDescription, setJobDescription] = useState('')
  const [jobDescFile, setJobDescFile] = useState<File | null>(null)
  const [targetRole, setTargetRole] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [gapAnalysis, setGapAnalysis] = useState<GapAnalysisResult | null>(null)

  const API_BASE = 'http://localhost:8000'

  const handleReset = () => {
    setAnalysisMethod('market-data')
    setJobDescInputMethod('text')
    setResumeFile(null)
    setResumeData(null)
    setResumeFeedback(null)
    setJobDescription('')
    setJobDescFile(null)
    setTargetRole('')
    setGapAnalysis(null)
    setError('')
    setLoading(false)

    if (resumeInputRef.current) resumeInputRef.current.value = ''
    if (jobDescInputRef.current) jobDescInputRef.current.value = ''

    if (typeof window !== 'undefined') {
      try {
        localStorage.removeItem(STORAGE_KEY)
      } catch (storageErr) {
        console.warn('Failed to clear saved gap analyzer state', storageErr)
      }
    }
  }

  useEffect(() => {
    if (typeof window === 'undefined') return
    try {
      const stored = localStorage.getItem(STORAGE_KEY)
      if (!stored) return
      const parsed = JSON.parse(stored)
      if (parsed.analysisMethod) setAnalysisMethod(parsed.analysisMethod)
      if (parsed.jobDescInputMethod) setJobDescInputMethod(parsed.jobDescInputMethod)
      if (typeof parsed.jobDescription === 'string') setJobDescription(parsed.jobDescription)
      if (typeof parsed.targetRole === 'string') setTargetRole(parsed.targetRole)
      if (parsed.resumeData) setResumeData(parsed.resumeData)
      if (parsed.resumeFeedback) setResumeFeedback(parsed.resumeFeedback)
      if (parsed.gapAnalysis) setGapAnalysis(parsed.gapAnalysis)
    } catch (storageErr) {
      console.warn('Failed to restore gap analyzer state', storageErr)
    }
  }, [])

  useEffect(() => {
    if (typeof window === 'undefined') return
    try {
      const payload = {
        analysisMethod,
        jobDescInputMethod,
        jobDescription,
        targetRole,
        resumeData,
        resumeFeedback,
        gapAnalysis,
      }
      localStorage.setItem(STORAGE_KEY, JSON.stringify(payload))
    } catch (storageErr) {
      console.warn('Failed to persist gap analyzer state', storageErr)
    }
  }, [analysisMethod, jobDescInputMethod, jobDescription, targetRole, resumeData, resumeFeedback, gapAnalysis])

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0]
      if (!file.name.endsWith('.pdf') && !file.name.endsWith('.docx')) {
        setError('Please upload a PDF or DOCX file')
        return
      }
      setResumeFile(file)
      setError('')
    }
  }

  const handleJobDescFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0]
      if (!file.name.endsWith('.pdf')) {
        setError('Please upload a PDF file for job description')
        return
      }
      setJobDescFile(file)
      setError('')
    }
  }

  const handleUploadResume = async () => {
    if (!resumeFile) {
      setError('Please select a resume file')
      return
    }

    setLoading(true)
    setError('')

    try {
      const formData = new FormData()
      formData.append('file', resumeFile)

      const response = await fetch(`${API_BASE}/api/upload-resume`, {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        throw new Error('Failed to parse resume')
      }

      const data = await response.json()
      setResumeData(data)

      // Fetch resume feedback
      if (data.skills && data.skills.length > 0 && data.raw_text) {
        try {
          const feedbackResponse = await fetch(`${API_BASE}/api/resume-feedback`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              resume_text: data.raw_text,
              skills: data.skills,
              target_role: targetRole || undefined,
            }),
          })

          if (feedbackResponse.ok) {
            const feedbackData = await feedbackResponse.json()
            setResumeFeedback(feedbackData)
          }
        } catch (feedbackErr) {
          console.log('Note: Resume feedback analysis skipped')
        }
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error uploading resume')
    } finally {
      setLoading(false)
    }
  }

  const handleGapAnalysis = async () => {
    if (!resumeData || !resumeData.skills || resumeData.skills.length === 0) {
      setError('Please upload a resume first')
      return
    }

    if (analysisMethod === 'market-data' && !targetRole.trim()) {
      setError('Please provide a target job role')
      return
    }

    if (analysisMethod === 'job-description') {
      if (jobDescInputMethod === 'text' && !jobDescription.trim()) {
        setError('Please provide a job description')
        return
      }
      if (jobDescInputMethod === 'pdf' && !jobDescFile) {
        setError('Please upload a job description PDF')
        return
      }
    }

    setLoading(true)
    setError('')

    try {
      let response;
      
      // If job description is via PDF, use FormData with different endpoint
      if (analysisMethod === 'job-description' && jobDescInputMethod === 'pdf' && jobDescFile) {
        const formData = new FormData()
        formData.append('user_skills', JSON.stringify(resumeData.skills))
        formData.append('target_role', targetRole || 'Target Role')
        formData.append('job_description_file', jobDescFile)
        
        response = await fetch(`${API_BASE}/api/gap-analysis-with-pdf`, {
          method: 'POST',
          body: formData,
        })
      } else {
        // Use JSON for text-based job description or market data
        response = await fetch(`${API_BASE}/api/gap-analysis`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            user_skills: resumeData.skills,
            target_role: targetRole || undefined,
            job_description: analysisMethod === 'job-description' ? jobDescription : undefined,
            use_saved_market_data: false,
          }),
        })
      }

      if (!response.ok) {
        throw new Error('Failed to perform gap analysis')
      }

      const data = await response.json()
      setGapAnalysis(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error performing gap analysis')
    } finally {
      setLoading(false)
    }
  }

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'critical':
        return 'text-red-400 bg-red-500/10 border-red-500/20'
      case 'high':
        return 'text-orange-400 bg-orange-500/10 border-orange-500/20'
      case 'medium':
        return 'text-yellow-400 bg-yellow-500/10 border-yellow-500/20'
      case 'low':
        return 'text-blue-400 bg-blue-500/10 border-blue-500/20'
      default:
        return 'text-gray-400 bg-gray-500/10 border-gray-500/20'
    }
  }

  const getReadinessColor = (readiness: string) => {
    if (!readiness) return 'text-gray-400'
    
    switch (readiness.toLowerCase()) {
      case 'excellent':
      case 'ready':
        return 'text-green-400'
      case 'good':
      case 'mostly ready':
        return 'text-blue-400'
      case 'fair':
      case 'needs preparation':
        return 'text-yellow-400'
      default:
        return 'text-red-400'
    }
  }

  return (
    <div className="p-6 space-y-6 max-w-5xl mx-auto">
      {/* Header */}
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold text-white mb-3">Analyze Your Skills</h1>
        <p className="text-gray-400 text-lg">Upload your resume and select your target job role to get a comprehensive skill gap analysis with personalized recommendations.</p>
      </div>

      {/* Error Display */}
      {error && (
        <div className="bg-red-500/10 border border-red-500/20 rounded-lg p-4 flex items-center gap-3">
          <AlertCircle className="w-5 h-5 text-red-400" />
          <p className="text-red-400">{error}</p>
        </div>
      )}

      {/* Resume Upload Section */}
      <div className="bg-white/5 rounded-lg p-8 border border-slate-700">
       
        
        <div className="space-y-4">
          <label className="block">
            <div className="border-2 border-dashed border-gray-600 bg-gray-800/30 rounded-lg p-12 text-center hover:border-gray-500 hover:bg-gray-800/50 transition-all cursor-pointer">
              <Upload className="w-16 h-16 mx-auto mb-4 text-gray-400" />
              <p className="text-white text-lg mb-2">
                {resumeFile ? resumeFile.name : 'Drop your resume here, or click to browse'}
              </p>
              <p className="text-gray-400 text-sm">Supports PDF and DOCX files up to 10MB</p>
            </div>
            <input
              type="file"
              ref={resumeInputRef}
              onChange={handleFileChange}
              accept=".pdf,.docx"
              className="hidden"
            />
          </label>

          <button
            onClick={handleUploadResume}
            disabled={!resumeFile || loading}
            className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-slate-700 disabled:cursor-not-allowed text-white px-6 py-3 rounded-lg font-medium transition-colors flex items-center justify-center gap-2"
          >
            {loading ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                Parsing Resume...
              </>
            ) : (
              <>
                <FileText className="w-5 h-5" />
                Parse Resume
              </>
            )}
          </button>

          <button
            onClick={handleReset}
            className="w-full bg-slate-800 hover:bg-slate-700 text-white px-6 py-3 rounded-lg font-medium transition-colors"
          >
            Reset All Data
          </button>
        </div>
      </div>

      {/* Parsed Resume Data */}
      {resumeData && (
        <div className="bg-white/5 rounded-lg p-6 border border-slate-700">
          <h2 className="text-xl font-semibold text-white mb-4 flex items-center gap-2">
            <CheckCircle2 className="w-5 h-5 text-green-400" />
            Resume Parsed Successfully
          </h2>
          
          <div className="space-y-4">
            {resumeData.name && (
              <div>
                <p className="text-gray-400 text-sm">Name</p>
                <p className="text-white font-medium">{resumeData.name}</p>
              </div>
            )}
            
            <div className="grid grid-cols-2 gap-4">
              {resumeData.email && (
                <div>
                  <p className="text-gray-400 text-sm">Email</p>
                  <p className="text-white">{resumeData.email}</p>
                </div>
              )}
            </div>

            <div>
              <p className="text-gray-400 text-sm mb-2">Extracted Skills ({resumeData.skills.length})</p>
              <div className="flex flex-wrap gap-2">
                {resumeData.skills.map((skill, index) => (
                  <span
                    key={index}
                    className="px-3 py-1 bg-blue-500/10 border border-blue-500/30 rounded-full text-blue-400 text-sm"
                  >
                    {skill}
                  </span>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Smart Resume Feedback & Improvement Suggestions */}
      {resumeFeedback && (
        <div className="bg-white/5 rounded-lg p-6 border border-slate-700 space-y-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-2xl font-bold text-white flex items-center gap-2">
              <Lightbulb className="w-6 h-6 text-yellow-400" />
              Smart Resume Feedback
            </h2>
            <div className="text-right">
              <p className="text-gray-400 text-sm">Overall Resume Quality</p>
              <p className={`text-3xl font-bold ${
                resumeFeedback.overall_score >= 80 ? 'text-green-400' :
                resumeFeedback.overall_score >= 60 ? 'text-yellow-400' :
                'text-red-400'
              }`}>
                {resumeFeedback.overall_score}/100
              </p>
            </div>
          </div>

          {/* Skill Density Analysis */}
          <div className="bg-slate-900/50 rounded-lg p-4 border border-slate-600">
            <div className="flex items-start justify-between mb-3">
              <h3 className="text-white font-semibold flex items-center gap-2">
                <Target className="w-5 h-5 text-blue-400" />
                Skill Density & Integration
              </h3>
              <span className={`text-lg font-bold ${
                resumeFeedback.skill_density_analysis.score >= 80 ? 'text-green-400' :
                resumeFeedback.skill_density_analysis.score >= 60 ? 'text-yellow-400' :
                'text-red-400'
              }`}>
                {resumeFeedback.skill_density_analysis.score}/100
              </span>
            </div>
            <p className="text-gray-300 text-sm mb-3">{resumeFeedback.skill_density_analysis.status}</p>
            <div className="space-y-2 text-gray-400 text-sm">
              <p>• Skill Density: {resumeFeedback.skill_density_analysis.density_percentage}% of your resume content</p>
              <p>• Total Unique Skills: {resumeFeedback.skill_density_analysis.unique_skills}</p>
              {resumeFeedback.skill_density_analysis.top_skills.length > 0 && (
                <p>• Top Skills: {resumeFeedback.skill_density_analysis.top_skills.join(', ')}</p>
              )}
            </div>
          </div>

          {/* Impact Words Analysis */}
          <div className="bg-slate-900/50 rounded-lg p-4 border border-slate-600">
            <div className="flex items-start justify-between mb-3">
              <h3 className="text-white font-semibold flex items-center gap-2">
                <TrendingUp className="w-5 h-5 text-purple-400" />
                Action & Impact Words
              </h3>
              <span className={`text-lg font-bold ${
                resumeFeedback.impact_words_analysis.score >= 80 ? 'text-green-400' :
                resumeFeedback.impact_words_analysis.score >= 60 ? 'text-yellow-400' :
                'text-red-400'
              }`}>
                {resumeFeedback.impact_words_analysis.score}/100
              </span>
            </div>
            <p className="text-gray-300 text-sm mb-3">{resumeFeedback.impact_words_analysis.status}</p>
            <div className="space-y-3">
              <div>
                <p className="text-gray-400 text-sm mb-2">✓ Strong Impact Words Found:</p>
                <div className="flex flex-wrap gap-2">
                  {Object.entries(resumeFeedback.impact_words_analysis.found_words)
                    .filter(([_, words]) => words.length > 0)
                    .flatMap(([_, words]) => words)
                    .slice(0, 8)
                    .map((word, idx) => (
                      <span key={idx} className="px-2 py-1 bg-green-500/10 border border-green-500/30 rounded text-green-400 text-xs">
                        {word}
                      </span>
                    ))}
                </div>
              </div>
              {resumeFeedback.impact_words_analysis.priority_missing.length > 0 && (
                <div>
                  <p className="text-gray-400 text-sm mb-2">✗ Missing Powerful Words:</p>
                  <div className="flex flex-wrap gap-2">
                    {resumeFeedback.impact_words_analysis.priority_missing.slice(0, 6).map((word, idx) => (
                      <span key={idx} className="px-2 py-1 bg-orange-500/10 border border-orange-500/30 rounded text-orange-400 text-xs">
                        {word}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Formatting Analysis */}
          <div className="bg-slate-900/50 rounded-lg p-4 border border-slate-600">
            <div className="flex items-start justify-between mb-3">
              <h3 className="text-white font-semibold flex items-center gap-2">
                <FileText className="w-5 h-5 text-cyan-400" />
                Resume Formatting & Structure
              </h3>
              <span className={`text-lg font-bold ${
                resumeFeedback.formatting_analysis.score >= 80 ? 'text-green-400' :
                resumeFeedback.formatting_analysis.score >= 60 ? 'text-yellow-400' :
                'text-red-400'
              }`}>
                {resumeFeedback.formatting_analysis.score}/100
              </span>
            </div>
            <p className="text-gray-300 text-sm mb-3">{resumeFeedback.formatting_analysis.status}</p>
            <div className="space-y-2 text-gray-400 text-sm">
              <p>• Word Count: {resumeFeedback.formatting_analysis.word_count}</p>
              <p>• Contact Info: 
                {resumeFeedback.formatting_analysis.contact_info_found.email && ' ✓ Email'} 
                {resumeFeedback.formatting_analysis.contact_info_found.phone && ' ✓ Phone'} 
                {resumeFeedback.formatting_analysis.contact_info_found.linkedin && ' ✓ LinkedIn'}
              </p>
              {resumeFeedback.formatting_analysis.issues.length > 0 && (
                <div className="mt-2 p-2 bg-red-500/10 border border-red-500/20 rounded">
                  <p className="text-red-400 text-xs mb-1">⚠️ Issues Found:</p>
                  {resumeFeedback.formatting_analysis.issues.map((issue, idx) => (
                    <p key={idx} className="text-red-300 text-xs">• {issue}</p>
                  ))}
                </div>
              )}
            </div>
          </div>

          {/* Relevance Analysis (if target role provided) */}
          {resumeFeedback.relevance_analysis.score > 0 && (
            <div className="bg-slate-900/50 rounded-lg p-4 border border-slate-600">
              <div className="flex items-start justify-between mb-3">
                <h3 className="text-white font-semibold flex items-center gap-2">
                  <Star className="w-5 h-5 text-amber-400" />
                  Relevance to Target Role
                </h3>
                <span className={`text-lg font-bold ${
                  resumeFeedback.relevance_analysis.score >= 80 ? 'text-green-400' :
                  resumeFeedback.relevance_analysis.score >= 60 ? 'text-yellow-400' :
                  'text-red-400'
                }`}>
                  {resumeFeedback.relevance_analysis.score}/100
                </span>
              </div>
              <p className="text-gray-300 text-sm mb-3">{resumeFeedback.relevance_analysis.status}</p>
              <p className="text-gray-400 text-sm mb-2">Matched: {resumeFeedback.relevance_analysis.matched_skills} skills</p>
              {resumeFeedback.relevance_analysis.missing_critical_skills.length > 0 && (
                <div>
                  <p className="text-gray-400 text-sm mb-2">Missing Critical Skills:</p>
                  <div className="flex flex-wrap gap-2">
                    {resumeFeedback.relevance_analysis.missing_critical_skills.map((skill, idx) => (
                      <span key={idx} className="px-2 py-1 bg-red-500/10 border border-red-500/30 rounded text-red-400 text-xs">
                        {skill}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Improvement Suggestions */}
          {resumeFeedback.improvement_suggestions.length > 0 && (
            <div className="bg-gradient-to-r from-blue-500/10 to-purple-500/10 rounded-lg p-4 border border-slate-600">
              <h3 className="text-white font-semibold text-lg mb-4 flex items-center gap-2">
                <AlertTriangle className="w-5 h-5 text-yellow-400" />
                Personalized Improvement Suggestions
              </h3>
              <div className="space-y-3">
                {resumeFeedback.improvement_suggestions.map((suggestion, idx) => (
                  <div key={idx} className="bg-slate-800/50 rounded p-3 border-l-4 border-l-yellow-500">
                    <div className="flex items-start justify-between mb-2">
                      <div>
                        <p className="text-white font-semibold text-sm">{suggestion.category}</p>
                        <p className={`text-xs font-medium ${
                          suggestion.priority === 'High' ? 'text-red-400' :
                          suggestion.priority === 'Medium' ? 'text-yellow-400' :
                          'text-blue-400'
                        }`}>
                          Priority: {suggestion.priority}
                        </p>
                      </div>
                    </div>
                    <p className="text-gray-300 text-sm mb-2">💡 {suggestion.suggestion}</p>
                    <p className="text-gray-400 text-xs italic">Impact: {suggestion.impact}</p>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Analysis Method Selection */}
      {resumeData && (
        <div className="bg-white/5 rounded-lg p-8 border border-slate-700">
          <h2 className="text-xl font-semibold text-white mb-6">Choose Analysis Method</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
            {/* Job Description Option */}
            <button
              onClick={() => setAnalysisMethod('job-description')}
              className={`p-6 rounded-lg border-2 text-left transition-all ${
                analysisMethod === 'job-description'
                  ? 'border-blue-500 bg-blue-500/10'
                  : 'border-slate-600 bg-slate-900/30 hover:border-slate-500'
              }`}
            >
              <div className="flex items-start gap-3">
                <div className={`w-5 h-5 rounded-full border-2 flex items-center justify-center mt-0.5 ${
                  analysisMethod === 'job-description'
                    ? 'border-blue-500'
                    : 'border-slate-500'
                }`}>
                  {analysisMethod === 'job-description' && (
                    <div className="w-2.5 h-2.5 rounded-full bg-blue-500"></div>
                  )}
                </div>
                <div>
                  <h3 className="text-white font-semibold text-lg mb-1">Upload Job Description</h3>
                  <p className="text-gray-400 text-sm">More accurate analysis</p>
                </div>
              </div>
            </button>

            {/* Market Data Option */}
            <button
              onClick={() => setAnalysisMethod('market-data')}
              className={`p-6 rounded-lg border-2 text-left transition-all ${
                analysisMethod === 'market-data'
                  ? 'border-blue-500 bg-blue-500/10'
                  : 'border-slate-600 bg-slate-900/30 hover:border-slate-500'
              }`}
            >
              <div className="flex items-start gap-3">
                <div className={`w-5 h-5 rounded-full border-2 flex items-center justify-center mt-0.5 ${
                  analysisMethod === 'market-data'
                    ? 'border-blue-500'
                    : 'border-slate-500'
                }`}>
                  {analysisMethod === 'market-data' && (
                    <div className="w-2.5 h-2.5 rounded-full bg-blue-500"></div>
                  )}
                </div>
                <div>
                  <h3 className="text-white font-semibold text-lg mb-1">Select Job Role</h3>
                  <p className="text-gray-400 text-sm">Quick predefined roles</p>
                </div>
              </div>
            </button>
          </div>

          {/* Input Fields Based on Selection */}
          <div className="space-y-4">
            {analysisMethod === 'job-description' ? (
              <div className="space-y-4">
                {/* Toggle between Text and PDF input */}
                <div className="flex gap-3 bg-slate-900/30 p-1 rounded-lg w-fit">
                  <button
                    onClick={() => setJobDescInputMethod('text')}
                    className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                      jobDescInputMethod === 'text'
                        ? 'bg-blue-600 text-white'
                        : 'text-gray-400 hover:text-white'
                    }`}
                  >
                    Paste Text
                  </button>
                  <button
                    onClick={() => setJobDescInputMethod('pdf')}
                    className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                      jobDescInputMethod === 'pdf'
                        ? 'bg-blue-600 text-white'
                        : 'text-gray-400 hover:text-white'
                    }`}
                  >
                    Upload PDF
                  </button>
                </div>

                {jobDescInputMethod === 'text' ? (
                  <div>
                    <label className="block text-gray-300 text-sm mb-2 font-medium">
                      Job Description
                    </label>
                    <textarea
                      value={jobDescription}
                      onChange={(e) => setJobDescription(e.target.value)}
                      placeholder="Paste the complete job description here..."
                      rows={10}
                      className="w-full bg-slate-900/50 border border-slate-600 rounded-lg px-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
                    />
                  </div>
                ) : (
                  <div>
                    <label className="block text-gray-300 text-sm mb-2 font-medium">
                      Job Description PDF
                    </label>
                    <label className="block">
                      <div className="border-2 border-dashed border-blue-500/50 bg-slate-900/30 rounded-lg p-8 text-center hover:border-blue-400 hover:bg-slate-900/50 transition-all cursor-pointer">
                        <FileText className="w-12 h-12 mx-auto mb-3 text-gray-400" />
                        <p className="text-white mb-2">
                          {jobDescFile ? jobDescFile.name : 'Click to upload job description PDF'}
                        </p>
                        <p className="text-gray-400 text-sm">PDF files only</p>
                      </div>
                      <input
                        type="file"
                        ref={jobDescInputRef}
                        onChange={handleJobDescFileChange}
                        accept=".pdf"
                        className="hidden"
                      />
                    </label>
                  </div>
                )}
              </div>
            ) : (
              <div>
                <label className="block text-gray-300 text-sm mb-2 font-medium">
                  Target Job Role
                </label>
                <input
                  type="text"
                  value={targetRole}
                  onChange={(e) => setTargetRole(e.target.value)}
                  placeholder="e.g., Senior Full Stack Developer, Data Scientist, DevOps Engineer"
                  className="w-full bg-slate-900/50 border border-slate-600 rounded-lg px-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
                />
                <p className="text-gray-500 text-xs mt-2">We'll analyze your skills against real-time market data for this role</p>
              </div>
            )}

            <button
              onClick={handleGapAnalysis}
              disabled={
                loading || 
                (analysisMethod === 'market-data' && !targetRole.trim()) || 
                (analysisMethod === 'job-description' && jobDescInputMethod === 'text' && !jobDescription.trim()) ||
                (analysisMethod === 'job-description' && jobDescInputMethod === 'pdf' && !jobDescFile)
              }
              className="w-full bg-gradient-to-r from-blue-600 to-blue-600 hover:from-blue-700 hover:to-blue-700 disabled:from-slate-700 disabled:to-slate-700 disabled:cursor-not-allowed text-white px-6 py-4 rounded-lg font-semibold transition-all text-lg flex items-center justify-center gap-2"
            >
              {loading ? (
                <>
                  <Loader2 className="w-6 h-6 animate-spin" />
                  {analysisMethod === 'market-data' ? 'Collecting Real-Time Jobs...' : 'Analyzing...'}
                </>
              ) : (
                <>
                  <Search className="w-6 h-6" />
                  Analyze Skills
                </>
              )}
            </button>
          </div>
        </div>
      )}

          {/* Gap Analysis Results */}
          {gapAnalysis && (
            <div className="space-y-6">
              {/* Overview Cards */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="bg-gradient-to-br from-blue-600/20 to-blue-900/20 rounded-lg p-6 border border-blue-500/30">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-gray-400">Match Score</span>
                    <TrendingUp className="w-5 h-5 text-blue-400" />
                  </div>
                  <div className="text-3xl font-bold text-white">
                    {typeof gapAnalysis.match_percentage === 'number' ? gapAnalysis.match_percentage.toFixed(1) : '0.0'}%
                  </div>
                </div>

                <div className="bg-gradient-to-br from-purple-600/20 to-purple-900/20 rounded-lg p-6 border border-purple-500/30">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-gray-400">Readiness Score</span>
                    <Target className="w-5 h-5 text-purple-400" />
                  </div>
                  <div className="text-3xl font-bold text-white">
                    {typeof gapAnalysis.readiness_score === 'number' ? gapAnalysis.readiness_score.toFixed(1) : gapAnalysis.readiness_score || 'N/A'}
                  </div>
                </div>

                <div className="bg-gradient-to-br from-green-600/20 to-green-900/20 rounded-lg p-6 border border-green-500/30">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-gray-400">Status</span>
                    <CheckCircle2 className="w-5 h-5 text-green-400" />
                  </div>
                  <div className={`text-2xl font-bold ${getReadinessColor(gapAnalysis.overall_readiness)}`}>
                    {gapAnalysis.overall_readiness || 'N/A'}
                  </div>
                </div>
              </div>

              {/* Matched Skills */}
              {gapAnalysis.matched_skills_detailed && gapAnalysis.matched_skills_detailed.length > 0 && (
                <div className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
                  <h3 className="text-xl font-semibold text-white mb-4 flex items-center gap-2">
                    <CheckCircle2 className="w-5 h-5 text-green-400" />
                    Matched Skills ({gapAnalysis.matched_skills_detailed.length})
                  </h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                    {gapAnalysis.matched_skills_detailed.filter(skill => skill && skill.skill).map((skill, index) => (
                      <div
                        key={index}
                        className="bg-green-500/10 border border-green-500/20 rounded-lg p-3"
                      >
                        <div className="flex items-start justify-between">
                          <span className="text-white font-medium">{skill.skill}</span>
                          <span className="text-green-400 text-sm">
                            {skill.percentage ? `${skill.percentage.toFixed(0)}%` : ''}
                          </span>
                        </div>
                        <div className="text-gray-400 text-sm mt-1">
                          Demand: {skill.market_demand || 'N/A'}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Skill Gaps by Priority */}
              {gapAnalysis.skill_gaps && (
                <div className="space-y-4">
                  {['critical', 'high', 'medium', 'low'].map((priority) => {
                    const gaps = gapAnalysis.skill_gaps[priority as keyof typeof gapAnalysis.skill_gaps]
                    if (!gaps || gaps.length === 0) return null

                    return (
                      <div key={priority} className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
                        <h3 className={`text-lg font-semibold mb-4 flex items-center gap-2 capitalize ${getPriorityColor(priority)}`}>
                          <AlertCircle className="w-5 h-5" />
                          {priority} Priority Gaps ({gaps.length})
                        </h3>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                          {gaps.filter(skill => skill && skill.skill).map((skill, index) => (
                            <div
                              key={index}
                              className={`border rounded-lg p-3 ${getPriorityColor(priority)}`}
                            >
                              <div className="flex items-start justify-between">
                                <span className="font-medium">{skill.skill}</span>
                                <span className="text-sm">
                                  {skill.percentage ? `${skill.percentage.toFixed(0)}%` : ''}
                                </span>
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    )
                  })}
                </div>
              )}


            </div>
          )}
    </div>
  )
}

