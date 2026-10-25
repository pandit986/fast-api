from fastapi import FastAPI, File, UploadFile, HTTPException, Depends, Header
from fastapi.staticfiles import StaticFiles
import os
import shutil

app = FastAPI()

# step 1: Define the upload directory
UPLOAD_DIR = "uploads"

# step 2: Create the upload directory if it doesn't exist
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# step 2: Set up static files
# http://127.0.0.1:8000/uploads/filename
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="Files")


# step 3: Define the file upload endpoint
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    filename = file.filename

    # step 4: Check if the file already exists
    if os.path.exists(os.path.join(UPLOAD_DIR, filename)):
        raise HTTPException(status_code=400, detail="File already exists")

    file_path = os.path.join(UPLOAD_DIR, filename)

    # step 4: Save the uploaded file to the upload directory
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

        return {
            "filename": filename,
            "message": "File uploaded successfully",
            "file_url": f"http://127.0.0.1:8000/uploads/{filename}"
        }


# get file url api

@app.get("/file_url/{filename}")
async def get_file_url(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)

    # step 5: Check if the file exists
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    return {
        "filename": filename,
        "file_url": f"http://127.0.0.1:8000/uploads/{filename}"
    }
