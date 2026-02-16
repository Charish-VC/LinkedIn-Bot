# agents/job_search_agent.py

import yaml
import pandas as pd
from tools.linkedin_scraper import scrape_jobs


def load_config(config_path="config.yaml"):
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


class JobSearchAgent:
    def __init__(self, keywords, locations, max_jobs_per_search=25):
        self.keywords = keywords
        self.locations = locations
        self.max_jobs = max_jobs_per_search

    def run(self, output_csv="jobs.csv"):
        all_jobs = []

        for keyword in self.keywords:
            for location in self.locations:
                jobs = scrape_jobs(
                    keyword=keyword,
                    location=location,
                    max_jobs=self.max_jobs
                )
                all_jobs.extend(jobs)

        if not all_jobs:
            print("❌ No jobs collected.")
            return None

        df = pd.DataFrame(all_jobs)
        df.to_csv(output_csv, index=False)

        print(f"📁 Saved {len(df)} jobs to {output_csv}")
        return df


# Standalone test (now config-driven)
if __name__ == "__main__":
    config = load_config("config.yaml")

    job_cfg = config["job_search"]

    agent = JobSearchAgent(
        keywords=job_cfg["keywords"],
        locations=job_cfg["locations"],
        max_jobs_per_search=job_cfg.get("max_jobs_per_search", 25)
    )

    agent.run()
