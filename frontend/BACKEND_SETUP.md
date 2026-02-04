# SkillSphere - Backend API Setup

## 🚀 Quick Start

### 1. Install Backend Dependencies

```bash
cd C:\dell\Desktop\skillgap\backend
pip install fastapi uvicorn python-multipart pydantic
```

### 2. Start FastAPI Backend

```bash
cd C:\dell\Desktop\skillgap\backend
python api.py
```

The API will run on: **http://localhost:8000**
API Documentation: **http://localhost:8000/docs**

### 3. Start Frontend

Open a **new terminal**:

```bash
cd C:\dell\Desktop\frontend
npm run dev
```

Frontend will run on: **http://localhost:3000**

## 📡 API Endpoints

- `GET /` - Health check
- `GET /api/roles` - Get available target roles
- `POST /api/gap-analysis` - Analyze skill gap
- `POST /api/user-skills-analysis` - Detailed skill analysis
- `POST /api/upload-resume` - Upload resume for parsing
- `GET /api/market-skills/{role}` - Get market skills for role

## 🎯 How It Works

1. **Backend (FastAPI)** connects to your existing `gap_analyzer.py` logic
2. **Frontend (Next.js)** calls the API to get real analysis results
3. **Gap Analyzer page** displays live data from your backend

## 🔧 Features Implemented

✅ Real-time skill gap analysis
✅ Multiple target roles (Senior Full Stack, Python Dev, Frontend Dev)
✅ Dynamic skill matching and prioritization
✅ Resume upload support
✅ Market demand percentages
✅ Job readiness scoring
✅ AI-powered recommendations

## 📊 Current Available Roles

- Senior Full Stack Developer
- Python Developer  
- Frontend Developer

## 🛠️ Customization

To add more roles or connect to real market data:

1. Edit `api.py` in the backend folder
2. Update `MOCK_MARKET_DATA` dictionary
3. Or connect to your job collector and skill extractor

## 🐛 Troubleshooting

**Backend not starting?**
- Make sure you're in the correct directory
- Install dependencies: `pip install fastapi uvicorn python-multipart pydantic`

**Frontend can't connect?**
- Check backend is running on port 8000
- Verify `.env.local` has correct API URL

**CORS errors?**
- Backend is configured to allow `localhost:3000`
- Check console for specific error messages
