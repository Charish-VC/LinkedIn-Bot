from agents.job_search_agent import JobSearchAgent

# Manually passing lists
agent = JobSearchAgent(
    keywords=[ "Data Analyst"],
    locations=["Dubai"]
)

agent.run()