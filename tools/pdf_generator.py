from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import pandas as pd
import os

def generate_pdf(input_csv="cover_letters.csv", output_pdf="cover_letters.pdf"):
    if not os.path.exists(input_csv):
        raise FileNotFoundError(f"The file {input_csv} does not exist yet.")

    df = pd.read_csv(input_csv)
    
    # Normalize columns to match your dataframe
    df.columns = df.columns.str.lower().str.strip()
    title_col = next((c for c in df.columns if 'title' in c), 'job title')
    comp_col = next((c for c in df.columns if 'company' in c), 'company')
    letter_col = next((c for c in df.columns if 'letter' in c), 'cover letter')

    c = canvas.Canvas(output_pdf, pagesize=letter)
    c.setFont("Helvetica", 12)

    y_position = 750
    for _, row in df.iterrows():
        # Header
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y_position, f"Job: {row[title_col]} at {row[comp_col]}")
        y_position -= 20
        
        # Reset font for body
        c.setFont("Helvetica", 10)
        # Basic text wrapping: reportlab drawString doesn't wrap text automatically
        text_object = c.beginText(50, y_position)
        text_object.textLines(row[letter_col][:1000]) # Taking first 1000 chars
        c.drawText(text_object)
        
        y_position -= 200 # Space between entries

        if y_position < 150:
            c.showPage()
            y_position = 750
            c.setFont("Helvetica", 12)

    c.save()
    return output_pdf