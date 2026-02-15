import requests
import sys
from pathlib import Path

# Add parent directory to path to import config
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import API_URL


def upload_pdfs_api(files):
    files_payload=[ ("files",(f.name,f.read(),"application/pdf")) for f in files]
    return requests.post(f"{API_URL}/upload_pdfs/",files=files_payload)

def ask_question(question):
    return requests.post(f"{API_URL}/ask/",data={"question":question})