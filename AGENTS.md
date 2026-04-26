# Job-bot

Python project using venv (not uv/poetry). Windows-focused.

## Run Commands

- **Web UI**: `run_web.bat` or `venv\Scripts\python.exe app.py`
- **CLI**: `run.ps1` or `venv\Scripts\python.exe main.py`
- **Docker**: `docker compose up --build`

## Key Files

- `app.py` - Flask web server (port 5000)
- `main.py` - CLI entry point
- `graph.py` - LangGraph workflow orchestration
- `config/config.yaml` - Job keywords, locations, LLM model

## Prerequisites

- Chrome browser (uses Selenium with user profile)
- LinkedIn must be logged in manually on first run
- Ollama running locally with `mistral` model pulled

## Quirks

- Uses `venv` folder (not `.venv`)
- Chrome profile path configured in `config/config.yaml` under `selenium.chrome_profile_path`
- CSV/PDF outputs written to working directory
- LLM runs locally via Ollama - no external API calls
- Config-driven delays and anti-detection in `config/config.yaml` under `scraping`