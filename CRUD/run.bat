@echo off
REM Run the FastAPI CRUD app

cd /d "%~dp0"

if not exist "venv\Scripts\python.exe" (
    echo Creating virtual environment...
    python -m venv venv
)

echo Installing dependencies...
venv\Scripts\python.exe -m pip install --upgrade pip
venv\Scripts\python.exe -m pip install -r requirements.txt

echo Starting FastAPI server at http://127.0.0.1:8000
venv\Scripts\python.exe -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
