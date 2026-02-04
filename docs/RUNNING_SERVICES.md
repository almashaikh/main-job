# SkillSphere - Running Both Services

## 🚀 Quick Start

Both the backend and frontend are now running successfully!

### Current Status
- ✅ **Backend (FastAPI)**: http://localhost:8000
- ✅ **Frontend (Next.js)**: http://localhost:3000
- ✅ **API Documentation**: http://localhost:8000/docs

## 📋 What's Running

### Backend (Port 8000)
- **Service**: FastAPI with Python
- **Features**: 
  - Resume parsing (PDF/DOCX)
  - Skill gap analysis
  - Job market data collection
  - AI-powered learning roadmaps
  - Real-time job matching

### Frontend (Port 3000)
- **Service**: Next.js with TypeScript
- **Features**:
  - Modern dashboard interface
  - Gap analyzer page
  - Learning roadmap visualization
  - Resume upload functionality
  - Responsive design

## 🎯 How to Use

1. **Open Frontend**: Go to http://localhost:3000
2. **Navigate to Gap Analyzer**: Click on "Gap Analyzer" in the sidebar
3. **Upload Resume**: Upload your PDF/DOCX resume
4. **Analyze Skills**: Choose a target role or paste job description
5. **View Results**: See your skill gaps and recommendations

## 🔧 Management Scripts

### Start Both Services
```bash
# Using Batch file
start_both_services.bat

# Using PowerShell
.\start_both_services.ps1
```

### Check Service Status
```bash
.\check_services.ps1
```

### Stop Services
- Press `Ctrl+C` in each terminal window
- Or close the terminal windows

## 📡 API Endpoints

The backend provides these key endpoints:

- `GET /` - Health check
- `POST /api/upload-resume` - Upload and parse resume
- `POST /api/gap-analysis` - Perform skill gap analysis
- `POST /api/analyze-job-description` - Extract skills from job description
- `POST /api/generate-roadmap` - Generate learning roadmap
- `POST /api/search-jobs` - Search real-time job opportunities
- `GET /api/roadmap/check-availability` - Check if AI roadmap is available

## 🛠️ Features Available

### ✅ Currently Working
- Resume upload and parsing
- Skill extraction from resumes
- Job description analysis
- Real-time skill gap analysis
- Market demand calculation
- Job readiness scoring
- Learning recommendations
- AI-powered roadmaps (if GEMINI_API_KEY is configured)
- **Real-time job search** - Live job opportunities from Adzuna API

### 🔄 Data Sources
- **Adzuna API**: Real-time job market data
- **200+ Skills Database**: Technical skills recognition
- **spaCy NLP**: Advanced text processing
- **Google Gemini**: AI-powered roadmap generation

## 🎨 Frontend Pages

- **Landing Page** (`/`): Welcome page with features
- **Login Page** (`/login`): Authentication interface
- **Dashboard** (`/dashboard`): Redirects to Gap Analyzer
- **Gap Analyzer** (`/dashboard/gap-analyzer`): Main analysis tool
- **Learning Roadmap** (`/dashboard/roadmap`): Personalized learning paths
- **Job Opportunities** (`/dashboard/job-opportunities`): Real-time job search with live data from Adzuna API

## 🐛 Troubleshooting

### Backend Issues
```bash
# Check if backend is running
curl http://localhost:8000

# Restart backend
cd skillgap/backend
python api.py
```

### Frontend Issues
```bash
# Check if frontend is running
curl http://localhost:3000

# Restart frontend
cd frontend
npm run dev
```

### Common Issues
1. **Port already in use**: Kill existing processes or use different ports
2. **Dependencies missing**: Run `pip install -r requirements.txt` and `npm install`
3. **spaCy model missing**: Run `python -m spacy download en_core_web_sm`

## 📊 Testing the System

1. **Upload a resume** (PDF or DOCX format)
2. **Choose target role** (e.g., "Python Developer", "Data Scientist")
3. **View analysis results**:
   - Match percentage
   - Skill gaps by priority
   - Learning recommendations
   - Job readiness score

## 🎉 Success!

Your SkillSphere application is now fully operational with:
- ✅ Real-time job market analysis
- ✅ AI-powered skill gap detection
- ✅ Personalized learning recommendations
- ✅ Modern web interface
- ✅ Complete API backend

**Start exploring at**: http://localhost:3000

---

*Last updated: January 31, 2026*