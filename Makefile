# Makefile for LinkedIn Job Application Bot

# Set up virtual environment, install dependencies, and download Ollama model
setup:
	@echo "Setting up environment..."
	python3 -m venv venv
	. venv/bin/activate && pip install --upgrade pip
	. venv/bin/activate && pip install -r requirements.txt
	@echo "Downloading and setting up Ollama model (Mistral 7B)..."
	ollama pull mistral
	@echo "Setup complete!"

# Activate the virtual environment
activate:
	@echo "Activating virtual environment..."
	. venv/bin/activate

# Run the LinkedIn bot script
run:
	@echo "Running LinkedIn bot..."
	. venv/bin/activate && python linkedin_bot.py

# Run the cover letter generator
cover_letters:
	@echo "Generating cover letters..."
	. venv/bin/activate && python generate_cover_letter.py

# Save application materials to PDF
save_pdf:
	@echo "Saving application materials to PDF..."
	. venv/bin/activate && python save_as_pdf.py

# Clean up the project (remove virtual environment)
clean:
	@echo "Cleaning up..."
	rm -rf venv
	@echo "Cleanup complete!"