from weasyprint import HTML, CSS
import pandas as pd
import os


def generate_pdf(input_csv="cover_letters.csv", output_pdf="final_applications.pdf"):
    if not os.path.exists(input_csv):
        raise FileNotFoundError(f"The file {input_csv} does not exist yet.")

    df = pd.read_csv(input_csv)
    
    title_col = next((c for c in df.columns if 'title' in c.lower()), 'job_title')
    comp_col = next((c for c in df.columns if 'company' in c.lower()), 'company')
    letter_col = next((c for c in df.columns if 'letter' in c.lower()), 'cover_letter')
    date_col = next((c for c in df.columns if 'date' in c.lower()), 'date_applied')
    
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            @page {
                size: A4;
                margin: 2cm;
                @bottom-right {
                    content: "Page " counter(page) " of " counter(pages);
                    font-size: 10pt;
                    font-family: Helvetica, Arial, sans-serif;
                }
            }
            body {
                font-family: Helvetica, Arial, sans-serif;
                font-size: 11pt;
                line-height: 1.5;
                color: #333;
            }
            .job-entry {
                margin-bottom: 30px;
                padding-bottom: 20px;
                border-bottom: 1px solid #ddd;
                page-break-inside: avoid;
            }
            .job-title {
                font-size: 14pt;
                font-weight: bold;
                color: #1a1a1a;
                margin-bottom: 5px;
            }
            .company {
                font-size: 12pt;
                color: #555;
                margin-bottom: 10px;
            }
            .cover-letter {
                font-size: 11pt;
                line-height: 1.6;
                text-align: justify;
                white-space: pre-wrap;
            }
            .date-applied {
                font-size: 9pt;
                color: #888;
                margin-top: 10px;
            }
            h1 {
                font-size: 18pt;
                color: #0066cc;
                margin-bottom: 20px;
            }
        </style>
    </head>
    <body>
        <h1>Job Applications</h1>
    """
    
    for _, row in df.iterrows():
        job_title = row.get(title_col, 'Unknown Position')
        company = row.get(comp_col, 'Unknown Company')
        cover_letter = row.get(letter_col, '')
        date_applied = row.get(date_col, '')
        
        html_content += f"""
        <div class="job-entry">
            <div class="job-title">{job_title}</div>
            <div class="company">{company}</div>
            <div class="cover-letter">{cover_letter}</div>
            {f'<div class="date-applied">Applied: {date_applied}</div>' if date_applied else ''}
        </div>
        """
    
    html_content += """
    </body>
    </html>
    """
    
    css = CSS(string="""
        @page { size: A4; margin: 2cm; }
    """)
    
    HTML(string=html_content).write_pdf(output_pdf, stylesheets=[css])
    
    return output_pdf


if __name__ == "__main__":
    result = generate_pdf()
    print(f"✅ PDF generated: {result}")