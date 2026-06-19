from fastapi import APIRouter, File, UploadFile
from services.services import extract_text_from_file
import fitz 
import os
import shutil

main_route = APIRouter()

# Directory to save the uploaded files
UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@main_route.post("/upload/")
async def upload_file(file: UploadFile = File(...)):

    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    # Read the uploaded file and save to the local disk
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    finally:
        #Close the file to free up memory
        file.file.close() 
        
    return {
        "message": "File uploaded successfully",
        "filename": file.filename,
        "content_type": file.content_type
    }

@main_route.get("/read_pdf_text")
async def read_pdf():

    await extract_text_from_file("RESUME_AL_RANDOLPH_VILLEGAS.pdf")

    return 0