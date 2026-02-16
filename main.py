# main.py

import yaml
from agents.job_search_agent import JobSearchAgent
from agents.resume_agent import ResumeAgent
from agents.cover_letter_agent import CoverLetterAgent
from agents.pdf_agent import PDFAgent

def load_config(config_path="config/config.yaml"):
    """Load configuration from YAML file"""
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def main():
    print("\n🚀 Starting Job Application Agent Pipeline\n")

    # Load configuration
    config = load_config()
    
    # Extract config values
    keywords = config['job_search']['keywords']
    locations = config['job_search']['locations']
    resume_file = config['resume']['file']
    llm_model = config['llm']['model']

    print(f"📋 Searching for: {', '.join(keywords)}")
    print(f"📍 Locations: {', '.join(locations)}\n")

    # 1️⃣ Job Search
    job_agent = JobSearchAgent(
        keywords=keywords,
        locations=locations,
        max_jobs_per_search=10
    )
    jobs_df = job_agent.run(output_csv="jobs.csv")

    if jobs_df is None or jobs_df.empty:
        print("❌ Job search failed or no jobs found. Stopping pipeline.")
        return

    # 2️⃣ Resume Parsing
    resume_agent = ResumeAgent(model=llm_model) 
    resume_data = resume_agent.run(resume_path=resume_file)

    if not resume_data:
        print("❌ Resume parsing failed. Stopping pipeline.")
        return

    # 3️⃣ Cover Letter Generation
    cover_agent = CoverLetterAgent(model_name=llm_model)
    cover_agent.run(
        input_csv="jobs.csv", 
        user_context=resume_data["structured_resume"]
    )

    # 4️⃣ PDF Generation
    pdf_agent = PDFAgent(
        input_file="cover_letters.csv",
        output_file="final_applications.pdf"
    )
    pdf_agent.run()

    print("\n✅ Pipeline completed successfully!")

if __name__ == "__main__":
    main()