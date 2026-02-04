@echo off
echo ========================================
echo   SkillSphere Backend Server Starter
echo ========================================
echo.

cd /d C:\dell\Desktop\skillgap\backend

echo Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

echo.
echo Installing/Updating dependencies...
python -m pip install fastapi uvicorn python-multipart pydantic

echo.
echo ========================================
echo   Starting FastAPI Backend Server
echo ========================================
echo.
echo API will be available at: http://localhost:8000
echo API Documentation at: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.

python api.py
pause
