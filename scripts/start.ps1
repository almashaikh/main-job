# Start the SkillGap backend server
Set-Location $PSScriptRoot
.\venv\Scripts\python.exe -m uvicorn api:app --reload --host 0.0.0.0 --port 8000
