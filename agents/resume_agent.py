import ollama
from tools.resume_parser import parse_resume

class ResumeAgent:
    def __init__(self, model="mistral"):
        self.model = model

    def run(self, resume_path: str) -> dict:
        parsed = parse_resume(resume_path)

        prompt = f"""
You are an expert resume analyzer.

Given the resume text below, extract structured information in JSON with:
- name
- education
- skills (list)
- projects (list)
- experience (list)
- summary (short professional summary)

Resume:
{parsed['raw_text']}
"""

        response = ollama.generate(
            model=self.model,
            prompt=prompt
        )

        return {
            "structured_resume": response["response"],
            "raw_text": parsed["raw_text"]
        }
