# main.py

import yaml
from graph import create_job_bot_graph
from rich.console import Console

console = Console()

def load_config(config_path="config/config.yaml"):
    """Load configuration from YAML file"""
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def main():
    console.print("\n[bold green]🚀 Starting Job Application Agent Pipeline (LangGraph Edition)[/bold green]\n")

    # Load configuration
    try:
        config = load_config()
    except Exception as e:
        console.print(f"[bold red]❌ Error loading config: {e}[/bold red]")
        return
    
    # Extract config values
    keywords = config['job_search']['keywords']
    locations = config['job_search']['locations']
    resume_file = config['resume']['file']
    llm_model = config['llm']['model']
    max_jobs = config['job_search'].get('max_jobs_per_search', 10)

    console.print(f"📋 Searching for: {', '.join(keywords)}")
    console.print(f"📍 Locations: {', '.join(locations)}\n")

    # Initialize Graph
    bot_graph = create_job_bot_graph()

    # Initial State
    initial_state = {
        "keywords": keywords,
        "locations": locations,
        "resume_path": resume_file,
        "llm_model": llm_model,
        "max_jobs": max_jobs,
        "jobs": [],           # Empty start
        "resume_data": {},
        "cover_letters": [],
        "final_pdf": ""
    }

    # Execute Graph
    try:
        # invoke returns the final state
        final_state = bot_graph.invoke(initial_state)
        
        if final_state.get("error"):
            console.print(f"[bold red]❌ Pipeline Error: {final_state['error']}[/bold red]")
        else:
            console.print("\n[bold green]✅ Pipeline completed successfully![/bold green]")
            if final_state.get("final_pdf"):
                console.print(f"📄 Applications saved to: [bold underline]{final_state['final_pdf']}[/bold underline]")

    except Exception as e:
         console.print(f"[bold red]❌ Runtime Error: {e}[/bold red]")

if __name__ == "__main__":
    main()