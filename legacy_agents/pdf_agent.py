from tools.pdf_generator import generate_pdf

class PDFAgent:
    def __init__(self, input_file="cover_letters.csv", output_file="final_applications.pdf"):
        self.input_file = input_file
        self.output_file = output_file

    def run(self):
        print(f"📄 PDFAgent: Converting {self.input_file} to PDF...")
        try:
            result = generate_pdf(self.input_file, self.output_file)
            print(f"✅ PDF successfully saved as {result}")
        except Exception as e:
            print(f"❌ Error generating PDF: {e}")