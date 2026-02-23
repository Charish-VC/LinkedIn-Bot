# 🤖 AI Job Application Bot

A powerful, automated job application assistant that searches for jobs on LinkedIn, parses your resume, generates personalized cover letters, and compiles them into a PDF application package.

Now features a **Flask Web Interface** and full **Docker support** for a one-command setup!

## 🌟 Features

-   **LinkedIn Job Search**: Automatically finds jobs matching your keywords and location.
-   **Resume Analysis**: Extracts structured data from your PDF resume using local LLMs.
-   **Cover Letter Generation**: Writes unique, tailored cover letters for each job found.
-   **PDF Compilation**: Merges all applications into a single professional PDF.
-   **Modern Web UI**: Upload resumes and track progress via a clean dashboard.
-   **Privacy First**: Runs locally using **Ollama** (Mistral) — no data leaves your machine.
-   **Docker Ready**: Spin up the full stack (app + Ollama) with a single command.

## 📂 Project Structure

```text
Job-bot/
├── app.py                  # Flask Web Application Entry Point
├── graph.py                # LangGraph Workflow Definition
├── main.py                 # CLI Entry Point
├── Dockerfile              # Docker image definition
├── docker-compose.yml      # Orchestrates app + Ollama services
├── .dockerignore           # Files excluded from Docker image
├── run.ps1                 # PowerShell Setup & Run Script (local)
├── run_web.bat             # Batch Script to Launch Web Interface (local)
├── requirements.txt        # Python Dependencies
├── config/
│   └── config.yaml         # Configuration (Keywords, Locations, Models)
├── static/
│   └── css/
│       └── style.css       # Web UI Styling
├── templates/
│   ├── index.html          # Upload Page
│   └── results.html        # Results Dashboard
├── tools/
│   ├── linkedin_scraper.py # Selenium LinkedIn Scraper
│   ├── pdf_generator.py    # ReportLab PDF Generator
│   └── resume_parser.py    # PDF/Docx Parser
└── uploads/                # Directory for uploaded resumes
```

## 🚀 Getting Started

### Option 1 — Docker (Recommended)

The easiest way to run the bot. No manual Python setup needed.

**Prerequisites**: [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/Charish-VC/LinkedIn-Bot.git
    cd LinkedIn-Bot/Job-bot
    ```

2.  **Start everything**:
    ```bash
    docker compose up --build
    ```
    This builds the app image and pulls the Ollama service automatically.

3.  **Pull the Mistral model** (first time only — run in a second terminal):
    ```bash
    docker exec -it jobbot-ollama ollama pull mistral
    ```

4.  **Open the app**: [http://localhost:5000](http://localhost:5000)

5.  **Stop**:
    ```bash
    docker compose down
    ```

> **Tip**: Edit `config/config.yaml` any time to change job keywords or locations — the container picks it up via a volume mount, no rebuild needed.

---

### Option 2 — Local Setup

**Prerequisites**:
1.  **Python 3.10+**
2.  **Ollama**: Install from [ollama.com](https://ollama.com/) and pull the model:
    ```bash
    ollama pull mistral
    ```
3.  **Chrome**: Ensure Google Chrome is installed.

**Install & Run**:

-   **Web Interface** — double-click `run_web.bat` or run:
    ```cmd
    .\run_web.bat
    ```
-   **Terminal Mode** — run the PowerShell script:
    ```powershell
    .\run.ps1
    ```
-   **Manual**:
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    pip install -r requirements.txt
    python app.py
    ```

## 🖥️ Usage

1.  Open [http://localhost:5000](http://localhost:5000) in your browser.
2.  Upload your **Resume (PDF)**.
3.  Click **"Launch Job Search"**.
4.  Watch as the bot finds jobs and generates cover letters in real-time!
5.  Download the final `final_applications.pdf` when done.

## ⚙️ Configuration

Edit `config/config.yaml` to change search terms:
```yaml
job_search:
  keywords:
    - "Data Analyst"
    - "Software Engineer"
  locations:
    - "Dubai"
llm:
  model: mistral
```

## 🛠️ Built With

-   **LangChain & LangGraph**: Orchestration and State Management
-   **Flask**: Web Backend
-   **Ollama**: Local LLM Inference (Mistral)
-   **Selenium**: LinkedIn Web Scraping
-   **Pandas**: Data Handling
-   **ReportLab**: PDF Generation
-   **Docker**: Containerisation

## ⚠️ Notes

-   This bot uses Selenium to automate a browser. Ensure your LinkedIn session is valid. If asked to log in, please do so manually in the browser window that opens.
-   LinkedIn may apply bot-detection. If scraping fails, check the logs with `docker compose logs -f jobbot`.

## 📄 License

MIT License