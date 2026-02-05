"""
FastAPI Backend for SkillSphere
Connects frontend to existing gap analyzer backend logic
"""

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional, Union
import sys
import json
import tempfile
import os
from pathlib import Path
import PyPDF2

# Load environment variables first
from dotenv import load_dotenv
load_dotenv()

# Import backend modules
from resume_parser import ResumeParser
from skill_extractor_updated import SkillExtractor
from gap_analyzer import GapAnalyzer
from multi_source_collector import JobCollector
from resume_feedback_analyzer import ResumeFeedbackAnalyzer


# Import roadmap module
try:
    import google.generativeai as genai
    
    # Import roadmap classes
    import importlib.util
    current_dir = Path(__file__).parent
    spec = importlib.util.spec_from_file_location("ai_learning_roadmap", current_dir / "ai-learning-roadmap.py")
    roadmap_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(roadmap_module)
    
    RoadmapBuilder = roadmap_module.RoadmapBuilder
    ROADMAP_AVAILABLE = True
except Exception as e:
    print(f"⚠️ Warning: Roadmap module not available: {e}")
    ROADMAP_AVAILABLE = False
    RoadmapBuilder = None

app = FastAPI(title="SkillSphere API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize modules
resume_parser = ResumeParser()
skill_extractor = SkillExtractor()
gap_analyzer = GapAnalyzer()
job_collector = JobCollector()
feedback_analyzer = ResumeFeedbackAnalyzer()

# Initialize roadmap builder if available
roadmap_builder = None
if ROADMAP_AVAILABLE:
    try:
        gemini_key = os.getenv("GEMINI_API_KEY")
        if gemini_key:
            roadmap_builder = RoadmapBuilder(gemini_key)
            print("✅ Roadmap Builder initialized successfully")
        else:
            print("⚠️ GEMINI_API_KEY not found - roadmap features will be disabled")
    except Exception as e:
        print(f"⚠️ Could not initialize roadmap builder: {e}")

# Request/Response Models
class ResumeUploadResponse(BaseModel):
    success: bool
    skills: List[str]
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    experience_years: Optional[int] = None
    raw_text: Optional[str] = None

class JobDescriptionRequest(BaseModel):
    job_description: str
    job_title: Optional[str] = "Target Role"

class GapAnalysisRequest(BaseModel):
    user_skills: List[str]
    job_description: Optional[str] = None
    target_role: Optional[str] = None
    use_saved_market_data: bool = False
    market_data_file: Optional[str] = None

class ResumeFeedbackRequest(BaseModel):
    resume_text: str
    skills: List[str]
    target_role: Optional[str] = None

class ResumeFeedbackResponse(BaseModel):
    overall_score: int
    skill_density_analysis: Dict
    impact_words_analysis: Dict
    formatting_analysis: Dict
    relevance_analysis: Dict
    improvement_suggestions: List[Dict]

class RoadmapRequest(BaseModel):
    skill: str
    level: str = "beginner"  # beginner, intermediate, advanced

class RoadmapSkillsRequest(BaseModel):
    skills: List[str]
    level: str = "beginner"

class JobSearchRequest(BaseModel):
    role: str
    location: str = "India"
    page: int = 1

@app.get("/")
async def root():
    """Health check"""
    return {
        "status": "online",
        "service": "SkillSphere API",
        "version": "1.0.0"
    }

@app.post("/api/upload-resume", response_model=ResumeUploadResponse)
async def upload_resume(file: UploadFile = File(...)):
    """
    Upload and parse resume to extract skills
    Supports PDF and DOCX formats
    """
    import traceback
    try:
        print(f"📄 Received file: {file.filename}")
        
        # Validate file type
        if not file.filename.endswith(('.pdf', '.docx', '.doc')):
            raise HTTPException(
                status_code=400, 
                detail="Only PDF and DOCX files are supported"
            )
        
        # Save temporarily
        suffix = Path(file.filename).suffix
        print(f"💾 Saving temp file with suffix: {suffix}")
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_path = tmp_file.name
        
        print(f"📂 Temp file saved at: {tmp_path}")
        
        # Parse resume
        print(f"🔍 Parsing resume...")
        resume_data = resume_parser.parse_file(tmp_path)
        print(f"✅ Parsed successfully. Found {len(resume_data.get('skills', []))} skills")
        
        # Clean up temp file
        Path(tmp_path).unlink()
        
        return ResumeUploadResponse(
            success=True,
            skills=resume_data.get('skills', []),
            name=resume_data.get('name'),
            email=resume_data.get('email'),
            phone=resume_data.get('phone'),
            experience_years=resume_data.get('experience_years'),
            raw_text=resume_data.get('raw_text')
        )
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        print(traceback.format_exc())
        # Clean up temp file if exists
        if 'tmp_path' in locals():
            try:
                Path(tmp_path).unlink()
            except:
                pass
        raise HTTPException(status_code=500, detail=f"Error parsing resume: {str(e)}")

@app.post("/api/resume-feedback", response_model=ResumeFeedbackResponse)
async def analyze_resume_feedback(request: ResumeFeedbackRequest):
    """
    Analyze resume and provide smart feedback & improvement suggestions
    """
    import traceback
    try:
        print(f"📋 Analyzing resume for feedback...")
        
        # Analyze resume with target role context
        feedback = feedback_analyzer.analyze_resume(
            resume_text=request.resume_text,
            skills=request.skills,
            target_role=request.target_role
        )
        
        print(f"✅ Resume feedback analysis complete. Overall score: {feedback['overall_score']}")
        
        return ResumeFeedbackResponse(
            overall_score=feedback['overall_score'],
            skill_density_analysis=feedback['skill_density_analysis'],
            impact_words_analysis=feedback['impact_words_analysis'],
            formatting_analysis=feedback['formatting_analysis'],
            relevance_analysis=feedback['relevance_analysis'],
            improvement_suggestions=feedback['improvement_suggestions']
        )
        
    except Exception as e:
        print(f"❌ ERROR analyzing resume feedback: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error analyzing resume: {str(e)}")

@app.post("/api/analyze-job-description")
async def analyze_job_description(request: JobDescriptionRequest):
    """
    Extract required skills from a job description
    """
    try:
        # Extract skills from job description
        required_skills = skill_extractor.extract_from_text(request.job_description)
        
        return {
            "job_title": request.job_title,
            "required_skills": sorted(list(required_skills)),
            "total_skills": len(required_skills)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing job description: {str(e)}")

@app.post("/api/gap-analysis")
async def perform_gap_analysis(request: GapAnalysisRequest):
    """
    Perform skill gap analysis
    Can compare against:
    1. Specific job description (text)
    2. Real-time market data (collect jobs for role)
    3. Saved market analysis data
    
    Accepts JSON request body
    """
    import traceback
    try:
        parsed_skills = request.user_skills
        target_role = request.target_role
        job_description = request.job_description
        use_saved = request.use_saved_market_data
            
        print(f"🎯 Gap analysis request - Target role: {target_role}")
        print(f"📊 User skills count: {len(parsed_skills) if isinstance(parsed_skills, list) else 0}")
        
        user_skills_list = parsed_skills if isinstance(parsed_skills, list) else []
        job_desc_text = job_description
        
        # Determine market skills source
        if job_desc_text:
            print(f"📝 Using job description (text or PDF)")
            # Extract skills from provided job description
            required_skills_set = skill_extractor.extract_from_text(job_desc_text)
            role_name = target_role or "Target Job"
            
            # Convert to market skills format expected by gap_analyzer
            market_skills = [
                {
                    "skill": skill,
                    "percentage": 100.0,  # Job description = 100% required
                    "count": 1,
                    "demand_level": "Critical"
                }
                for skill in required_skills_set
            ]
            
        elif target_role and not use_saved:
            # Collect real-time jobs for the target role
            print(f"🌐 Collecting real-time jobs for: {target_role}")
            jobs = job_collector.collect_from_adzuna(target_role, pages=2)  # 2 pages = ~100 jobs
            
            if not jobs or len(jobs) == 0:
                raise HTTPException(
                    status_code=404,
                    detail=f"No jobs found for role: {target_role}. Try a different role name."
                )
            
            print(f"✅ Collected {len(jobs)} jobs. Analyzing skills...")
            
            # Analyze jobs to extract skills
            analysis_result = skill_extractor.analyze_jobs(jobs)
            market_skills = analysis_result['skills']  # Get the skills list from the analysis result
            role_name = target_role
            
            print(f"✅ Found {len(market_skills)} market skills")
            
        elif use_saved:
            print(f"📂 Using saved market data - feature not yet implemented")
            raise HTTPException(
                status_code=400,
                detail="Saved market data feature not yet implemented. Please use real-time analysis."
            )
            
        else:
            raise HTTPException(
                status_code=400,
                detail="Please provide either a target_role or job_description for analysis."
            )
        
        # Perform gap analysis using your existing logic
        print(f"🔍 Performing gap analysis...")
        analysis = gap_analyzer.analyze_gap(
            user_skills=user_skills_list,
            market_skills=market_skills,
            target_role=role_name
        )
        
        # Restructure response to match frontend expectations
        readiness_data = analysis.get('readiness_score', {})
        
        response = {
            'target_role': analysis.get('target_role'),
            'match_percentage': analysis.get('match_percentage', 0),
            'readiness_score': readiness_data.get('score', 0),
            'overall_readiness': readiness_data.get('level', 'Unknown'),
            'readiness_message': readiness_data.get('message', ''),
            'total_required_skills': analysis.get('total_required_skills', 0),
            'user_skills_count': analysis.get('user_skills_count', 0),
            'matched_skills_count': analysis.get('matched_skills_count', 0),
            'missing_skills_count': analysis.get('missing_skills_count', 0),
            'matched_skills': analysis.get('matched_skills', []),
            'matched_skills_detailed': [
                {
                    'skill': s['skill'],
                    'percentage': s.get('demand_percentage', 0),
                    'market_demand': s.get('demand_level', 'Unknown'),
                    'user_level': 'Present'
                }
                for s in analysis.get('matched_skills_detailed', [])
            ],
            'skill_gaps': {
                'critical': [
                    {
                        'skill': s['skill'],
                        'percentage': s.get('demand_percentage', 0),
                        'demand_level': s.get('priority', 'Critical')
                    }
                    for s in analysis.get('skill_gaps', {}).get('critical', [])
                ],
                'high': [
                    {
                        'skill': s['skill'],
                        'percentage': s.get('demand_percentage', 0),
                        'demand_level': s.get('priority', 'High')
                    }
                    for s in analysis.get('skill_gaps', {}).get('high', [])
                ],
                'medium': [
                    {
                        'skill': s['skill'],
                        'percentage': s.get('demand_percentage', 0),
                        'demand_level': s.get('priority', 'Medium')
                    }
                    for s in analysis.get('skill_gaps', {}).get('medium', [])
                ],
                'low': [
                    {
                        'skill': s['skill'],
                        'percentage': s.get('demand_percentage', 0),
                        'demand_level': s.get('priority', 'Low')
                    }
                    for s in analysis.get('skill_gaps', {}).get('low', [])
                ]
            },
            'total_gaps_by_priority': analysis.get('total_gaps_by_priority', {}),
            'recommendations': analysis.get('recommendations', []),
            'extra_skills': analysis.get('extra_skills', [])
        }
        
        print(f"✅ Gap analysis complete!")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ ERROR in gap analysis: {str(e)}")
        import traceback
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error performing gap analysis: {str(e)}")

@app.post("/api/gap-analysis-with-pdf")
async def perform_gap_analysis_with_pdf(
    user_skills: str = Form(...),
    target_role: Optional[str] = Form(None),
    job_description_file: UploadFile = File(...),
):
    """
    Perform skill gap analysis with job description from PDF file
    """
    import traceback
    try:
        # Parse user skills from JSON string
        parsed_skills = json.loads(user_skills) if isinstance(user_skills, str) else user_skills
        
        print(f"🎯 Gap analysis (PDF) - Target role: {target_role}")
        print(f"📊 User skills count: {len(parsed_skills)}")
        print(f"📄 Processing job description PDF: {job_description_file.filename}")
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            content = await job_description_file.read()
            temp_file.write(content)
            temp_path = temp_file.name
        
        try:
            # Extract text from PDF
            with open(temp_path, 'rb') as pdf_file:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                job_desc_text = ""
                for page in pdf_reader.pages:
                    job_desc_text += page.extract_text() + "\n"
            print(f"✅ Extracted {len(job_desc_text)} characters from job description PDF")
        finally:
            # Clean up temp file
            os.unlink(temp_path)
        
        # Extract skills from job description
        print(f"📝 Using job description from PDF")
        required_skills_set = skill_extractor.extract_from_text(job_desc_text)
        role_name = target_role or "Target Job"
        
        # Convert to market skills format
        market_skills = [
            {
                "skill": skill,
                "percentage": 100.0,
                "count": 1,
                "demand_level": "Critical"
            }
            for skill in required_skills_set
        ]
        
        # Perform gap analysis
        print(f"🔍 Performing gap analysis...")
        analysis = gap_analyzer.analyze_gap(
            user_skills=parsed_skills,
            market_skills=market_skills,
            target_role=role_name
        )
        
        # Restructure response
        readiness_data = analysis.get('readiness_score', {})
        
        response = {
            'target_role': analysis.get('target_role'),
            'match_percentage': analysis.get('match_percentage', 0),
            'readiness_score': readiness_data.get('score', 0),
            'overall_readiness': readiness_data.get('level', 'Unknown'),
            'readiness_message': readiness_data.get('message', ''),
            'total_required_skills': analysis.get('total_required_skills', 0),
            'user_skills_count': analysis.get('user_skills_count', 0),
            'matched_skills_count': analysis.get('matched_skills_count', 0),
            'missing_skills_count': analysis.get('missing_skills_count', 0),
            'matched_skills': analysis.get('matched_skills', []),
            'matched_skills_detailed': [
                {
                    'skill': s['skill'],
                    'percentage': s.get('demand_percentage', 0),
                    'market_demand': s.get('demand_level', 'Unknown'),
                    'user_level': 'Present'
                }
                for s in analysis.get('matched_skills_detailed', [])
            ],
            'skill_gaps': {
                'critical': [
                    {
                        'skill': s['skill'],
                        'percentage': s.get('demand_percentage', 0),
                        'demand_level': s.get('priority', 'Critical')
                    }
                    for s in analysis.get('skill_gaps', {}).get('critical', [])
                ],
                'high': [
                    {
                        'skill': s['skill'],
                        'percentage': s.get('demand_percentage', 0),
                        'demand_level': s.get('priority', 'High')
                    }
                    for s in analysis.get('skill_gaps', {}).get('high', [])
                ],
                'medium': [
                    {
                        'skill': s['skill'],
                        'percentage': s.get('demand_percentage', 0),
                        'demand_level': s.get('priority', 'Medium')
                    }
                    for s in analysis.get('skill_gaps', {}).get('medium', [])
                ],
                'low': [
                    {
                        'skill': s['skill'],
                        'percentage': s.get('demand_percentage', 0),
                        'demand_level': s.get('priority', 'Low')
                    }
                    for s in analysis.get('skill_gaps', {}).get('low', [])
                ]
            },
            'total_gaps_by_priority': analysis.get('total_gaps_by_priority', {}),
            'recommendations': analysis.get('recommendations', []),
            'extra_skills': analysis.get('extra_skills', [])
        }
        
        print(f"✅ Gap analysis complete!")
        return response
        
    except Exception as e:
        print(f"❌ ERROR in gap analysis with PDF: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error performing gap analysis: {str(e)}")

from fastapi import Form

@app.post("/api/match-job")
async def match_specific_job(
    resume_file: UploadFile = File(...),
    job_description: str = Form(...)
):
    """
    Complete workflow: Upload resume and match against job description
    """
    import traceback
    try:
        print(f"📄 Match job - Received file: {resume_file.filename}")
        print(f"📝 Job description length: {len(job_description) if job_description else 0}")
        
        # Step 1: Parse resume
        suffix = Path(resume_file.filename).suffix
        print(f"💾 Saving temp file...")
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
            content = await resume_file.read()
            tmp_file.write(content)
            tmp_path = tmp_file.name
        
        print(f"🔍 Parsing resume from: {tmp_path}")
        resume_data = resume_parser.parse_file(tmp_path)
        Path(tmp_path).unlink()
        
        user_skills = resume_data.get('skills', [])
        print(f"✅ Found {len(user_skills)} user skills")
        
        # Step 2: Extract skills from job description
        print(f"🔍 Extracting skills from job description...")
        required_skills = skill_extractor.extract_from_text(job_description)
        print(f"✅ Found {len(required_skills)} required skills")
        
        # Step 3: Calculate match
        user_skills_set = set(user_skills)
        required_skills_set = set(required_skills)
        
        matched = user_skills_set.intersection(required_skills_set)
        missing = required_skills_set - user_skills_set
        
        match_percentage = (len(matched) / len(required_skills_set) * 100) if required_skills_set else 0
        
        # Determine readiness
        if match_percentage >= 80:
            readiness = "Excellent"
            recommendation = "Apply now - You're a great fit!"
        elif match_percentage >= 60:
            readiness = "Good"
            recommendation = "Strong candidate - Highlight matching skills"
        elif match_percentage >= 40:
            readiness = "Fair"
            recommendation = "Consider upskilling critical gaps first"
        else:
            readiness = "Needs Work"
            recommendation = "Significant upskilling required"
        
        print(f"✅ Match complete: {match_percentage:.1f}%")
        
        return {
            "match_percentage": round(match_percentage, 2),
            "readiness": readiness,
            "recommendation": recommendation,
            "user_name": resume_data.get('name'),
            "matched_skills": sorted(list(matched)),
            "missing_skills": sorted(list(missing)),
            "total_required": len(required_skills_set),
            "total_matched": len(matched)
        }
        
    except Exception as e:
        print(f"❌ ERROR in match_job: {str(e)}")
        print(traceback.format_exc())
        if 'tmp_path' in locals():
            try:
                Path(tmp_path).unlink()
            except:
                pass
        raise HTTPException(status_code=500, detail=f"Error matching job: {str(e)}")

@app.get("/api/market-data-files")
async def list_market_data_files():
    """
    List available market analysis files
    """
    try:
        analysis_files = list(Path('.').glob('skill_analysis*.json'))
        
        files = []
        for f in analysis_files:
            with open(f, 'r', encoding='utf-8') as file:
                data = json.load(file)
                files.append({
                    "filename": f.name,
                    "role": data.get('analyzed_role', 'Unknown'),
                    "total_jobs": data.get('total_jobs', 0),
                    "unique_skills": data.get('unique_skills', 0)
                })
        
        return {"files": files}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing files: {str(e)}")

# ============================================
# LEARNING ROADMAP ENDPOINTS
# ============================================

@app.post("/api/generate-roadmap")
async def generate_roadmap(request: RoadmapRequest):
    """
    Generate a personalized learning roadmap for a single skill
    """
    if not ROADMAP_AVAILABLE or not roadmap_builder:
        raise HTTPException(
            status_code=503,
            detail="Roadmap generation service is not available. Please ensure GEMINI_API_KEY is configured."
        )
    
    try:
        print(f"🎯 Generating roadmap for: {request.skill} (Level: {request.level})")
        
        # Generate complete roadmap
        roadmap = roadmap_builder.build_complete_roadmap(
            skill=request.skill,
            level=request.level
        )
        
        print(f"✅ Roadmap generated successfully")
        return roadmap
        
    except Exception as e:
        print(f"❌ ERROR generating roadmap: {str(e)}")
        import traceback
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error generating roadmap: {str(e)}")

@app.post("/api/generate-roadmaps-bulk")
async def generate_roadmaps_bulk(request: RoadmapSkillsRequest):
    """
    Generate learning roadmaps for multiple skills (e.g., from skill gap analysis)
    Returns simplified roadmaps for each skill
    """
    if not ROADMAP_AVAILABLE or not roadmap_builder:
        raise HTTPException(
            status_code=503,
            detail="Roadmap generation service is not available. Please ensure GEMINI_API_KEY is configured."
        )
    
    try:
        print(f"🎯 Generating roadmaps for {len(request.skills)} skills")
        
        roadmaps = []
        for skill in request.skills[:10]:  # Limit to 10 skills to avoid timeout
            try:
                print(f"   • Generating roadmap for: {skill}")
                roadmap = roadmap_builder.build_complete_roadmap(
                    skill=skill,
                    level=request.level
                )
                roadmaps.append({
                    "skill": skill,
                    "success": True,
                    "roadmap": roadmap
                })
            except Exception as e:
                print(f"   ⚠️ Failed to generate roadmap for {skill}: {e}")
                roadmaps.append({
                    "skill": skill,
                    "success": False,
                    "error": str(e)
                })
        
        print(f"✅ Generated {len([r for r in roadmaps if r['success']])} roadmaps successfully")
        
        return {
            "total_requested": len(request.skills),
            "total_generated": len([r for r in roadmaps if r['success']]),
            "roadmaps": roadmaps
        }
        
    except Exception as e:
        print(f"❌ ERROR generating bulk roadmaps: {str(e)}")
        import traceback
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error generating roadmaps: {str(e)}")

@app.get("/api/roadmap/check-availability")
async def check_roadmap_availability():
    """
    Check if roadmap generation is available
    """
    return {
        "available": ROADMAP_AVAILABLE and roadmap_builder is not None,
        "gemini_configured": bool(os.getenv("GEMINI_API_KEY")),
        "message": "Roadmap generation is ready" if (ROADMAP_AVAILABLE and roadmap_builder) else "Configure GEMINI_API_KEY to enable roadmap generation"
    }

@app.post("/api/search-jobs")
async def search_jobs(request: JobSearchRequest):
    """
    Search for real-time job opportunities using Adzuna API
    """
    try:
        print(f"🔍 Searching jobs for: {request.role} in {request.location} (Page {request.page})")
        
        # Use the job collector to fetch real-time jobs
        jobs = job_collector.collect_from_adzuna(
            role=request.role,
            location=request.location,
            pages=1,  # Fetch one page at a time for better performance
            page_offset=request.page - 1  # Convert to 0-based indexing
        )
        
        if not jobs:
            return {
                "results": [],
                "count": 0,
                "message": f"No jobs found for '{request.role}' in {request.location}"
            }
        
        # Format jobs for frontend
        formatted_jobs = []
        for job in jobs:
            formatted_job = {
                "id": job.get('id', f"job_{len(formatted_jobs)}"),
                "title": job.get('title', 'Job Title Not Available'),
                "company": {
                    "display_name": job.get('company', 'Company Not Specified')
                },
                "location": {
                    "display_name": job.get('location', request.location)
                },
                "description": job.get('description', 'No description available'),
                "created": job.get('created', '2024-01-01T00:00:00Z'),
                "salary_min": job.get('salary_min'),
                "salary_max": job.get('salary_max'),
                "redirect_url": job.get('redirect_url', '#'),
                "contract_type": job.get('contract_type', 'Full-time'),
                "category": {
                    "label": job.get('category', 'Technology')
                }
            }
            formatted_jobs.append(formatted_job)
        
        print(f"✅ Found {len(formatted_jobs)} jobs")
        
        return {
            "results": formatted_jobs,
            "count": len(formatted_jobs) * 10,  # Estimate total (Adzuna doesn't provide exact count)
            "page": request.page,
            "role": request.role,
            "location": request.location
        }
        
    except Exception as e:
        print(f"❌ ERROR searching jobs: {str(e)}")
        import traceback
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error searching jobs: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting SkillSphere FastAPI Backend...")
    print("📡 API will be available at: http://localhost:8000")
    print("📚 API docs available at: http://localhost:8000/docs")
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
