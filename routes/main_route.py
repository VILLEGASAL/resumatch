from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from services.services import extract_text_from_file, evaluate_resume
import fitz 
import os
import shutil

main_route = APIRouter()

@main_route.post("/evaluate_resume/")
async def evaluate_applicant(job_description:str = Form(...), resume_file: UploadFile = File(...)):

    #Check if file is in pdf format
    if resume_file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    try:
        #Extract the text in the PDF
        resume_texts = await extract_text_from_file(resume_file)
    
        # Check if the PDF was empty or unreadable
        if not resume_texts.strip():
             raise HTTPException(status_code=400, detail="Could not extract text from the PDF.")

        # Asses
        result = await evaluate_resume(job_description, resume_texts)


        print(result)
        return result

    except Exception as e:
        # Catch any errors (like Gemini API timeouts) and return a clean error
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

