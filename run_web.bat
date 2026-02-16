@echo off
if not exist "venv" (
    echo Virtual environment not found. Please run run.ps1 first to setup.
    pause
    exit /b
)

echo Starting Job Bot Web Server...
echo Open http://127.0.0.1:5000 in your browser
venv\Scripts\python.exe app.py
pause
