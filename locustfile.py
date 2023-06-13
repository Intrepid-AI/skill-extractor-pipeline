from locust import HttpUser, task, between
import os

class WebsiteUser(HttpUser):
    wait_time = between(1, 5)
    host = "http://localhost:8000" 
    
    @task
    def upload_files(self):
        file_resume_path = os.path.join(os.getcwd(),"artifacts","jc.pdf")  # Specify the path to the resume file
        file_jd_path = os.path.join(os.getcwd(),"artifacts","jd_sr.pdf") # Specify the path to the JD file

        with open(file_resume_path, 'rb') as file_resume, open(file_jd_path, 'rb') as file_jd:
            files = [
                ("file_resume", (file_resume.name, file_resume, 'multipart/form-data')),
                ("file_jd", (file_jd.name, file_jd, 'multipart/form-data'))
            ]
            self.client.post("/matching_resume_with_job_description/", files=files)
