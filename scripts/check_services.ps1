# SkillSphere - Service Status Checker
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   SkillSphere - Service Status Check" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Backend
Write-Host "Checking Backend (Port 8000)..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000" -UseBasicParsing -TimeoutSec 5
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ Backend is running successfully!" -ForegroundColor Green
        Write-Host "   Status: $($response.StatusCode)" -ForegroundColor Gray
        Write-Host "   URL: http://localhost:8000" -ForegroundColor Gray
        Write-Host "   API Docs: http://localhost:8000/docs" -ForegroundColor Gray
    }
} catch {
    Write-Host "❌ Backend is not running" -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Gray
}

Write-Host ""

# Check Frontend
Write-Host "Checking Frontend (Port 3000)..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:3000" -UseBasicParsing -TimeoutSec 5
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ Frontend is running successfully!" -ForegroundColor Green
        Write-Host "   Status: $($response.StatusCode)" -ForegroundColor Gray
        Write-Host "   URL: http://localhost:3000" -ForegroundColor Gray
    }
} catch {
    Write-Host "❌ Frontend is not running" -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Gray
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   Status Check Complete" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan