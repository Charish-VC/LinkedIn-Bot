# LinkedIn Job Application Bot 🚀

This project automates job searching and cover letter generation using **Helium** for web scraping and **Ollama** for AI-generated personalized cover letters. The goal is to streamline the internship/job application process while staying compliant with LinkedIn’s terms of service.

## Features ✅
- **Automated Job Scraping:** Extracts job postings from LinkedIn using Helium.
- **AI-Generated Cover Letters:** Uses Ollama to generate personalized cover letters for each job posting.
- **Organized Application Materials:** Saves extracted job details and cover letters in structured files (CSV/PDF).
- **Manual Application Control:** Gathers all necessary information but requires manual submission to comply with LinkedIn’s policies.

## Installation 📥
### Prerequisites
Ensure you have the following installed:
- **Python 3.x**
- **Helium & Selenium**
- **Ollama**
- **Make (for easy setup on macOS/Linux)**

### Quick Setup (Mac/Linux)
Clone the repository and set up the environment using Make:
```bash
# Clone the repository
git clone https://github.com/yourusername/linkedin-bot.git
cd linkedin-bot

# Run the setup
make setup