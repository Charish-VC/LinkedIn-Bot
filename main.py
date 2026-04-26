# main.py

import yaml
from graph import create_job_bot_graph, load_config, create_initial_state
from rich.console import Console

console = Console()


def main():
    console.print("\n[bold green]🚀 Starting Job Application Agent Pipeline (LangGraph Edition)[/bold green]\n")

    try:
        config = load_config()
    except Exception as e:
        console.print(f"[bold red]❌ Error loading config: {e}[/bold red]")
        return
    
    keywords = config.get('job_search', {}).get('keywords', [])
    locations = config.get('job_search', {}).get('locations', [])
    
    console.print(f"📋 Searching for: {', '.join(keywords)}")
    console.print(f"📍 Locations: {', '.join(locations)}\n")

    bot_graph = create_job_bot_graph()
    initial_state = create_initial_state(config)

    try:
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