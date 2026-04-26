import os
import threading
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, send_file
from werkzeug.utils import secure_filename
from graph import create_job_bot_graph, load_config, create_initial_state
import yaml

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['Result_FOLDER'] = 'results'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

job_status = "Idle"
job_results = {}


def run_pipeline(resume_path):
    global job_status, job_results
    job_status = "Running"
    
    try:
        config = load_config()
        bot_graph = create_job_bot_graph()
        initial_state = create_initial_state(config, resume_path)

        final_state = bot_graph.invoke(initial_state)
        
        job_results = final_state
        job_status = "Completed"
        print("✅ Background job completed successfully.")
        
    except Exception as e:
        job_status = f"Failed: {str(e)}"
        print(f"❌ Background job failed: {e}")


@app.route('/')
def index():
    return render_template('index.html', status=job_status)


@app.route('/upload', methods=['POST'])
def upload_file():
    global job_status
    
    if 'resume' not in request.files:
        return redirect(request.url)
        
    file = request.files['resume']
    
    if file.filename == '':
        return redirect(request.url)
        
    if file:
        filename = "resume.pdf"
        file_path = os.path.join(os.getcwd(), filename)
        file.save(file_path)

        thread = threading.Thread(target=run_pipeline, args=(file_path,))
        thread.start()
        
        return redirect(url_for('results'))


@app.route('/results')
def results():
    global job_status, job_results
    
    jobs = []
    cover_letters = []
    
    if os.path.exists("jobs.csv"):
        try:
            jobs_df = pd.read_csv("jobs.csv")
            jobs = jobs_df.to_dict(orient='records')
        except:
            pass
            
    if os.path.exists("cover_letters.csv"):
        try:
            cl_df = pd.read_csv("cover_letters.csv")
            cover_letters = cl_df.to_dict(orient='records')
        except:
            pass
    
    return render_template('results.html', status=job_status, jobs=jobs, cover_letters=cover_letters)


@app.route('/download_pdf')
def download_pdf():
    if os.path.exists("final_applications.pdf"):
        return send_file("final_applications.pdf", as_attachment=True)
    return "File not found", 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)