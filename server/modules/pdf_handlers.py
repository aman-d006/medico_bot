import os
import shutil
import tempfile
from fastapi import UploadFile

UPLOAD_DIR="./uploaded_docs"

def save_uploaded_files(files:list[UploadFile]) -> list[str]:
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_path=[]

    for file in files:
        temp_path=os.path(UPLOAD_DIR)/file.filename
        with open(temp_path, "wb") as f:
            f.write(file.file.read())   
        file_path.append(str(temp_path)) 
    return file_path 
