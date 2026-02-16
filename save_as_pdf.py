from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import pandas as pd

df = pd.read_csv("cover_letters.csv")

pdf_file = "cover_letters.pdf"
c = canvas.Canvas(pdf_file, pagesize=letter)
c.setFont("Helvetica", 12)

y_position = 750
for _, row in df.iterrows():
    c.drawString(50, y_position, f"Job: {row['Job Title']} at {row['Company']}")
    y_position -= 20
    c.drawString(50, y_position, row["Cover Letter"][:500])  # Truncate for space
    y_position -= 100

    if y_position < 100:
        c.showPage()
        c.setFont("Helvetica", 12)
        y_position = 750

c.save()
print(f"PDF saved as {pdf_file}")