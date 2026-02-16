import ollama
import pandas as pd
import os

class CoverLetterAgent:
    def __init__(self, model_name="llama3"):
        self.model_name = model_name

    def generate_cover_letter(self, job_title, company_name, user_context):
        # The prompt now includes your resume data!
        prompt = f"""
        Write a professional and personalized cover letter for a {job_title} position at {company_name}.
        
        MY RESUME BACKGROUND:
        {user_context}

        INSTRUCTIONS:
        1. Keep it concise (3 paragraphs max).
        2. Highlight relevant skills from my background that match the job title.
        3. Use a formal and confident tone.
        """
        response = ollama.generate(model=self.model_name, prompt=prompt)
        return response['response']

    def run(self, input_csv="jobs.csv", output_csv="cover_letters.csv", user_context=""):
        if not os.path.exists(input_csv):
            print(f"❌ Error: {input_csv} not found.")
            return

        df = pd.read_csv(input_csv)
        df.columns = df.columns.str.lower().str.strip()
        
        title_col = next((c for c in df.columns if 'title' in c), None)
        comp_col = next((c for c in df.columns if 'company' in c), None)

        if not title_col or not comp_col:
            print(f"❌ Could not find columns. Found: {df.columns.tolist()}")
            return

        print(f"Generating personalized letters for {len(df)} jobs...")
        
        # We pass the user_context into the lambda function here
        df["cover_letter"] = df.apply(
            lambda row: self.generate_cover_letter(row[title_col], row[comp_col], user_context), 
            axis=1
        )

        df.to_csv(output_csv, index=False)
        print(f"✅ Saved to {output_csv}")