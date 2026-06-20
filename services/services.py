import fitz
from fastapi import UploadFile

from services import ai_model_setup

async def extract_text_from_file(file: UploadFile):

    file_bytes = await file.read()

    document = fitz.open(stream=file_bytes, filetype="pdf")

    document_texts = ""

    for page_num in range(len(document)):
        page = document.load_page(page_num)
        document_texts += page.get_text()
    
    document.close()

    return document_texts

async def evaluate_resume(job_description_string:str, resume_texts:str):
    
    result = await ai_model_setup.chain.ainvoke({"job_description": job_description_string, "resume_text": resume_texts})

    return result
