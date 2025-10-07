# Mozart Dueling AI Launcher
Write-Host "Starting Mozart Dueling AI..." -ForegroundColor Green

# Change to script directory
Set-Location $PSScriptRoot

# Try to run Mozart
try {
    python LAUNCH_GUI.py
    if ($LASTEXITCODE -ne 0) {
        throw "Python script failed with exit code $LASTEXITCODE"
    }
}
catch {
    Write-Host "Error: Failed to start Mozart Dueling AI" -ForegroundColor Red
    Write-Host "Please run setup.py first to install dependencies." -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}
