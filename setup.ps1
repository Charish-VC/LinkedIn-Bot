Write-Host "Creating virtual environment..."
python -m venv venv

Write-Host "Activating virtual environment..."
.\venv\Scripts\Activate.ps1

Write-Host "Upgrading pip..."
pip install --upgrade pip

Write-Host "Installing dependencies..."
pip install -r requirements.txt

Write-Host "Checking Ollama..."
ollama --version

Write-Host "Pulling LLM model..."
ollama pull mistral

Write-Host "Setup complete ✅"
