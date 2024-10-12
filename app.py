from flask import Flask, request, jsonify, render_template
import os
import time
from selenium import webdriver
from job_scraper import scrape_jobs_indeed, scrape_jobs_linkedin, init_driver

app = Flask(__name__)

# Path to store uploaded resumes
UPLOAD_FOLDER = './uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Route for rendering the home page
@app.route('/')
def index():
    return render_template('index.html')

# Route for form submission
@app.route('/submit', methods=['POST'])
def submit_form():
    job_preferences = request.form['job_preferences'].split(',')
    experience_level = request.form['experience_level']
    introduction = request.form['introduction']
    why_hire = request.form['why_hire']
    
    # Handling file upload
    resume = request.files['resume']
    resume_path = os.path.join(app.config['UPLOAD_FOLDER'], resume.filename)
    resume.save(resume_path)

    # Initialize web driver for job application process
    driver = init_driver()

    # Loop through each job preference and apply to jobs on Indeed/LinkedIn
    for job in job_preferences:
        jobs_indeed = scrape_jobs_indeed(driver, job.strip(), 'remote')  # Assuming remote jobs
        for job in jobs_indeed:
            apply_for_job(driver, job, resume_path)

    driver.quit()

    # Return success response
    return jsonify({'message': 'Your resume will be uploaded to all related upcoming and existing job postings.'})

# Function to apply for a job
def apply_for_job(driver, job, resume_path, update_resume=False):
    driver.get(job['link'])
    time.sleep(3)

    try:
        upload_button = driver.find_element('xpath', '//input[@type="file"]')
        if update_resume:
            print("Updating resume...")
        upload_button.send_keys(resume_path)  # Upload the resume

        submit_button = driver.find_element('xpath', '//button[@type="submit"]')
        submit_button.click()

        print(f"Successfully applied for {job['title']} at {job['company']}")

    except Exception as e:
        print(f"Could not apply for {job['title']}. Error: {e}")

# Start the Flask app
if __name__ == "__main__":
    app.run(debug=True)
