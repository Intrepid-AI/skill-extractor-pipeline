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

client = TestClient(app)

def test_entrypoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message" : "Welcome to Skill Extractor Platform"}

def test_checkhealth():
    response = client.get("/health")
    assert response.json() == {"status":200}

