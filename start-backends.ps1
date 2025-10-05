# PowerShell script to start JOBPLEXITY Backend Services
Write-Host "Starting JOBPLEXITY Backend Services..." -ForegroundColor Green

Write-Host ""
Write-Host "Starting Resume Analyzer Service (Port 5001)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\backend-resume-anaalyser'; python -m pip install -r requirements.txt; python main.py" -WindowStyle Normal

Write-Host ""
Write-Host "Starting Resume Builder Service (Port 5000)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\backend-tailured-resume-builder'; python -m pip install -r requirements.txt; python app.py" -WindowStyle Normal

Write-Host ""
Write-Host "Both backend services are starting..." -ForegroundColor Green
Write-Host "Resume Analyzer: http://localhost:5001" -ForegroundColor Cyan
Write-Host "Resume Builder: http://localhost:5000" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press any key to continue..." -ForegroundColor White
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
