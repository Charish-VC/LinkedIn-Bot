import operator
from typing import Annotated, List, TypedDict, Union

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_ollama import ChatOllama
from langgraph.graph import END, StateGraph, START

# Import existing tools
from tools.linkedin_scraper import scrape_jobs
from tools.resume_parser import parse_resume
from tools.pdf_generator import generate_pdf
import pandas as pd
import os

# Ollama host — defaults to localhost but can be overridden via env var
# (e.g. OLLAMA_HOST=http://ollama:11434 when running inside Docker Compose)
OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")

# Define State
class AgentState(TypedDict):
    keywords: List[str]
    locations: List[str]
    resume_path: str
    llm_model: str
    max_jobs: int
    
    # State that gets updated
    jobs: List[dict]
    resume_data: dict
    cover_letters: List[dict]
    final_pdf: str
    error:str

# --- Node Definitions ---

def search_jobs_node(state: AgentState):
    """
    Searches for jobs on LinkedIn using Selenium.
    """
    print("--- SEARCHING JOBS ---")
    all_jobs = []
    
    # Check if we already have jobs (resume capability?)
    if state.get("jobs") and len(state["jobs"]) > 0:
        print("Jobs already exist in state, skipping search.")
        return {"jobs": state["jobs"]}

    keywords = state.get("keywords", [])
    locations = state.get("locations", [])
    max_jobs = state.get("max_jobs", 10)

    for keyword in keywords:
        for location in locations:
            try:
                jobs = scrape_jobs(keyword, location, max_jobs)
                all_jobs.extend(jobs)
            except Exception as e:
                print(f"Error searching for {keyword} in {location}: {e}")
                # We don't stop, we just continue
    
    # Deduplicate based on link
    unique_jobs = {job['job_link']: job for job in all_jobs}.values()
    
    # Save to CSV for persistence/checking (optional, but good for now)
    df = pd.DataFrame(unique_jobs)
    if not df.empty:
        df.to_csv("jobs.csv", index=False)
        print(f"Saved {len(df)} jobs to jobs.csv")
    else:
        print("No jobs found.")
        return {"error": "No jobs found"}

    return {"jobs": list(unique_jobs)}


def parse_resume_node(state: AgentState):
    """
    Parses the resume and structures it using LLM.
    """
    print("--- PARSING RESUME ---")
    resume_path = state.get("resume_path")
    model_name = state.get("llm_model", "mistral")
    
    if not resume_path or not os.path.exists(resume_path):
        return {"error": f"Resume not found at {resume_path}"}
    
    try:
        # 1. Parse raw text
        parsed_data = parse_resume(resume_path)
        raw_text = parsed_data["raw_text"]
        
        # 2. Structure with LLM
        llm = ChatOllama(model=model_name, temperature=0, base_url=OLLAMA_HOST)
        
        system_msg = """You are an expert resume analyzer.
Given the resume text, extract structured information in JSON format with the following keys:
- name
- education (list)
- skills (list of strings)
- projects (list)
- experience (list)
- summary (short professional summary)

Return ONLY valid JSON."""

        messages = [
            SystemMessage(content=system_msg),
            HumanMessage(content=raw_text)
        ]
        
        # In a real production app, we'd use .with_structured_output or a parser
        # For now, relying on the prompt and model capability.
        response = llm.invoke(messages)
        structured_resume = response.content
        
        # Simple cleanup if the model creates markdown code blocks
        if "```json" in structured_resume:
            structured_resume = structured_resume.split("```json")[1].split("```")[0].strip()
        elif "```" in structured_resume:
             structured_resume = structured_resume.split("```")[1].split("```")[0].strip()

        return {
            "resume_data": {
                "raw_text": raw_text,
                "structured_resume": structured_resume
            }
        }
    except Exception as e:
        return {"error": f"Error parsing resume: {e}"}


def generate_cover_letters_node(state: AgentState):
    """
    Generates cover letters for each job found.
    """
    print("--- GENERATING COVER LETTERS ---")
    jobs = state.get("jobs", [])
    resume_data = state.get("resume_data", {})
    model_name = state.get("llm_model", "llama3")
    
    if not jobs:
        return {"error": "No jobs to generate cover letters for."}
        
    structured_resume = resume_data.get("structured_resume", "")
    
    llm = ChatOllama(model=model_name, temperature=0.7, base_url=OLLAMA_HOST)
    
    cover_letters = []
    
    for job in jobs:
        job_title = job.get("job_title", "Job")
        company = job.get("company", "Company")
        
        prompt = f"""Write a professional and personalized cover letter for a {job_title} position at {company}.
        
MY RESUME BACKGROUND:
{structured_resume}

INSTRUCTIONS:
1. Keep it concise (3 paragraphs max).
2. Highlight relevant skills from my background that match the job title.
3. Use a formal and confident tone.
4. Do NOT include placeholders like [Your Name] or [Date] if you don't have them, just sign off generically or with the Name from resume.
"""
        try:
            response = llm.invoke(prompt)
            letter_content = response.content
            
            job_record = job.copy()
            job_record["cover_letter"] = letter_content
            cover_letters.append(job_record)
            
            print(f"Generated letter for {company}")
        except Exception as e:
            print(f"Failed to generate letter for {company}: {e}")
            
    # Save to CSV
    if cover_letters:
        df = pd.DataFrame(cover_letters)
        df.to_csv("cover_letters.csv", index=False)
    
    return {"cover_letters": cover_letters}


def generate_pdf_node(state: AgentState):
    """
    Generates a PDF from the cover letters.
    """
    print("--- GENERATING PDF ---")
    
    # We rely on the existing tool which reads from CSV.
    # To be cleaner, we should probably update the tool to accept a dataframe or list,
    # but for compatibility we'll ensure the CSV exists (done in previous step).
    
    try:
        # Check if CSV exists (it should from previous step)
        if not os.path.exists("cover_letters.csv"):
             return {"error": "cover_letters.csv not found for PDF generation"}

        output_file = "final_applications.pdf"
        result_path = generate_pdf("cover_letters.csv", output_file)
        print(f"PDF Generated at: {result_path}")
        return {"final_pdf": result_path}
    except Exception as e:
        return {"error": f"Error generating PDF: {e}"}


# --- Graph Construction ---

def create_job_bot_graph():
    workflow = StateGraph(AgentState)
    
    workflow.add_node("search_jobs", search_jobs_node)
    workflow.add_node("parse_resume", parse_resume_node)
    workflow.add_node("generate_cover_letters", generate_cover_letters_node)
    workflow.add_node("generate_pdf", generate_pdf_node)
    
    # Define edges
    # Check for errors after each step ideally, but for now linear
    
    workflow.add_edge(START, "search_jobs")
    
    # Conditional edge to check if search failed
    def check_search_success(state):
        if state.get("error"):
            return END
        return "parse_resume"
        
    workflow.add_conditional_edges("search_jobs", check_search_success)
    
    def check_parse_success(state):
        if state.get("error"):
            return END
        return "generate_cover_letters"
        
    workflow.add_conditional_edges("parse_resume", check_parse_success)
    
    def check_letters_success(state):
        if state.get("error"):
            return END
        return "generate_pdf"
        
    workflow.add_conditional_edges("generate_cover_letters", check_letters_success)
    
    workflow.add_edge("generate_pdf", END)
    
    return workflow.compile()
