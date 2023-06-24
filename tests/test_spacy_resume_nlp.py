from pathlib import Path
import sys

from fastapi import FastAPI
from fastapi.testclient import TestClient

FILE = Path(__file__).resolve()
ROOT = FILE.parents[1]  # project root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH

from main import app
from src.data_models import *

def test_skill_extraction_from_file():
    file_path = "tests/artifacts/jc.pdf"
    
    with TestClient(app) as TC:
        with open(file_path, "rb") as file:
            files = {"file": file}
            response = TC.post("/extract_skills_upload/", files=files)

        response_json = response.json()
        ResponseSkills(**response_json)
        assert response.status_code == 200

def test_skill_matching():
    file_path_res = "tests/artifacts/jc.pdf"
    file_path_jd = "tests/artifacts/jd_sr.pdf"

    with TestClient(app) as TC:

        files = {"file_resume": open(file_path_res, "rb"), "file_jd" : open(file_path_jd, "rb")}
        response = TC.post("/match_resume_with_jd/", files=files)
        response_json = response.json()
        ResponseJDResume(**response_json)
        assert response.status_code == 200
