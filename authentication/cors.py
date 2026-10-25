from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# import os
# from dotenv import load_dotenv

# load_dotenv()  # Load environment variables from .env file
from config import settings

app =FastAPI()

origins = settings.origin  # Get allowed origins from environment variables



app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow specified origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)


@app.get("/")
async def home():
    return {"message": "CORS is enabled!"}