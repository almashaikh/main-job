@echo off
echo ========================================
echo   SkillSphere - Starting Both Services
echo ========================================
echo.

echo Starting Backend (FastAPI)...
echo Backend will be available at: http://localhost:8000
echo API Documentation at: http://localhost:8000/docs
echo.

start "SkillSphere Backend" cmd /k "cd /d backend && python api.py"

echo Waiting 5 seconds for backend to start...
timeout /t 5 /nobreak > nul

echo.
echo Starting Frontend (Next.js)...
echo Frontend will be available at: http://localhost:3000
echo.

start "SkillSphere Frontend" cmd /k "cd /d frontend && npm run dev"

echo.
echo ========================================
echo   Both Services Started Successfully!
echo ========================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:3000
echo API Docs: http://localhost:8000/docs
echo.
echo Press any key to exit this window...
pause > nul