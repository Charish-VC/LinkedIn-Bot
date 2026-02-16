# Function to check if a command exists
function Test-CommandExists {
    param ($Command)
    $oldPreference = $ErrorActionPreference
    $ErrorActionPreference = 'Stop'
    try {
        if (Get-Command $Command -ErrorAction SilentlyContinue) {
            return $true
        }
        return $false
    }
    catch {
        return $false
    }
    finally {
        $ErrorActionPreference = $oldPreference
    }
}

Write-Host " Starting Job Bot Setup & Run Script..." -ForegroundColor Green

# 1. Check/Create Virtual Environment
if (-not (Test-Path "venv")) {
    Write-Host "Virtual environment not found. Creating one..." -ForegroundColor Yellow
    python -m venv venv
    if (-not (Test-Path "venv")) {
        Write-Host "Failed to create virtual environment. Please check your python installation." -ForegroundColor Red
        exit
    }
    Write-Host "Virtual environment created." -ForegroundColor Green
}
else {
    Write-Host "Virtual environment found." -ForegroundColor Green
}

# 2. Activate Virtual Environment
$venvPython = ".\venv\Scripts\python.exe"
if (-not (Test-Path $venvPython)) {
    Write-Host " Python executable not found in venv. Recreating venv might be required." -ForegroundColor Red
    exit
}

# 3. Install/Update Dependencies
Write-Host "Checking and installing dependencies..." -ForegroundColor Cyan
& $venvPython -m pip install -r requirements.txt | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to install dependencies." -ForegroundColor Red
    # Continue anyway? No, probably should stop.
    exit
}
Write-Host " Dependencies installed." -ForegroundColor Green


# 4. Run the main script
Write-Host " Launching Job Bot..." -ForegroundColor Green
& $venvPython main.py

if ($LASTEXITCODE -ne 0) {
    Write-Host " Bot finished with errors." -ForegroundColor Red
}
else {
    Write-Host " Bot finished successfully." -ForegroundColor Green
}

Write-Host "Press any key to exit..."
$host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") | Out-Null
