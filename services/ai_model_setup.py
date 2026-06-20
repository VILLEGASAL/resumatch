from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from typing import List

import os

load_dotenv()

API_KEY = os.getenv("API_KEY")

class APPLICANT_SCORE_CARD(BaseModel):
    match_percentage:int = Field(
        description="An integer from 0 to 100 representing the overall fit based on the rubric."
    )
    strengths:List[str] = Field(
        description="List of 3 to 5 key skills or experiences from the resume that perfectly match the job description."
    )
    missing_skills:List[str] = Field(
        description="List of required skills or qualifications from the job description that are explicitly missing from the resume."
    )
    recommendation:str = Field(
        description="A short final verdict. Must be one of: 'Strong Hire', 'Interview', 'Keep on File', or 'Reject'."
    )

llm = ChatGoogleGenerativeAI(

    model="gemini-2.5-flash",
    api_key=API_KEY,
    temperature=0.0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    
)

SYSTEM_PROMPT = """

You are an expert Technical Recruiter and an advanced Applicant Tracking System (ATS). 
Your task is to objectively evaluate a candidate's resume against a provided job description and output the results strictly in the required structured format.

### Evaluation Rubric:
1.  **Analyze the Job Description:** Identify mandatory skills, preferred skills, required years of experience, and educational requirements.
2.  **Analyze the Resume:** Extract the candidate's actual skills, quantifiable experience, and education. Do not hallucinate or assume skills that are not explicitly stated.
3.  **Calculate Match Percentage (0-100):**
    *   Start at 100.
    *   Deduct heavy points (10-20) for missing mandatory skills or significant experience gaps.
    *   Deduct minor points (5-10) for missing preferred skills.
    *   Add points back if the candidate shows exceptional quantifiable achievements related to the role.
    *   A score of 90-100% means a near-perfect fit. 70-80% is a solid match. Below 50% means unqualified.
4.  **Identify Strengths & Gaps:** Clearly list what makes the candidate a great fit, and what critical requirements they are missing.

### Inputs:
**Job Description:**
{job_description}

**Candidate Resume:**
{resume_text}

Analyze the inputs based on the rubric and provide the structured scorecard.

"""

prompt_template = ChatPromptTemplate.from_template(SYSTEM_PROMPT)

structured_llm = llm.with_structured_output(APPLICANT_SCORE_CARD)

chain = prompt_template | structured_llm