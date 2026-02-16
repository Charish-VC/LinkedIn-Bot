# 🤖 AI Job Application Bot

A powerful, automated job application assistant that searches for jobs on LinkedIn, parses your resume, generates personalized cover letters, and compiles them into a PDF application package.

Now features a **Flask Web Interface** for easy resume uploads and real-time monitoring!

## 🌟 Features

-   **LinkedIn Job Search**: Automatically finds jobs matching your keywords and location.
-   **Resume Analysis**: Extracted structured data from your PDF resume using local LLMs.
-   **Cover Letter Generation**: Writes unique, tailored cover letters for each job found.
-   **PDF Compilation**: Merges all applications into a single professional PDF.
-   **Modern Web UI**: Upload resumes and track progress via a clean dashboard.
-   **Privacy First**: Runs locally using **Ollama** (Mistral/Llama3) - no data leaves your machine.

## 📂 Project Structure

```text
Job-bot/
├── app.py                  # Flask Web Application Entry Point
├── graph.py                # LangGraph Workflow Definition
├── main.py                 # CLI Entry Point
├── run.ps1                 # PowerShell Setup & Run Script
├── run_web.bat             # Batch Script to Launch Web Interface
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

### Prerequisites

1.  **Python 3.10+**
2.  **Ollama**: Install from [ollama.com](https://ollama.com/) and pull the models:
    ```bash
    ollama pull mistral
    ollama pull llama3
    ```
3.  **Chrome**: Ensure Google Chrome is installed.

### Installation

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/Charish-VC/LinkedIn-Bot.git
    cd LinkedIn-Bot/Job-bot
    ```

2.  **Setup & Run (Automated)**:
    -   To launch the **Web Interface**:
        Double-click `run_web.bat` or run:
        ```cmd
        .\run_web.bat
        ```
    -   To run in **Terminal Mode**:
        Run the PowerShell script:
        ```powershell
        .\run.ps1
        ```

3.  **Manual Setup**:
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    pip install -r requirements.txt
    ```

## 🖥️ Usage

### Web Interface
1.  Open `http://127.0.0.1:5000` in your browser.
2.  Upload your **Resume (PDF)**.
3.  Click **"Launch Job Search"**.
4.  Watch as the bot finds jobs and generates cover letters in real-time!
5.  Download the final `final_applications.pdf` when done.

### Configuration
Edit `config/config.yaml` to change search terms:
```yaml
job_search:
  keywords:
    - "Data Analyst"
    - "Software Engineer"
  locations:
    - "New York"
    - "Remote"
```

## 🛠️ Built With

-   **LangChain & LangGraph**: Orchestration and State Management
-   **Flask**: Web Backend
-   **Ollama**: Local LLM Inference
-   **Selenium**: Web Scraping
-   **Pandas**: Data Handling
-   **ReportLab**: PDF Generation

## ⚠️ Note
This bot uses Selenium to automate a browser. Ensure your LinkedIn session is valid. If asked to log in, please do so manually in the browser window that pops up.

## 📄 License
MIT License