from fastapi import APIRouter, File, UploadFile
from modules.load_vectorstore import load_vectorstore
from typing import List
from fastapi.responses import JSONResponse
from logger import logger


router=APIRouter()

@router.post("/upload_pdfs/")
async def upload_pdfs(files:List[UploadFile]=File(...)):
    try:
        logger.info(f"Received {len(files)} files for upload.")
        load_vectorstore(files)
        logger.info("Files uploaded and processed successfully.")
        return JSONResponse(content={"message": "Files uploaded and processed successfully."})
    except Exception as e:
        logger.exception(f"Error uploading files: {e}")
        return JSONResponse(content={"error": "Failed to upload and process files."}, status_code=500)