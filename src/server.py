from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from routes import main_route
import shutil
import os

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace "*" with your frontend's exact URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(

    main_route.main_route,
    prefix="/api",
    tags=["main_route"]
)