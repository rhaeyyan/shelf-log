@echo off
echo Activating virtual environment...
call venv\Scripts\activate

if errorlevel 1 (
    echo Virtual environment not found. Creating one now...
    python -m venv venv
    call venv\Scripts\activate
    echo Installing dependencies...
    pip install -r requirements.txt
)

echo Starting ShelfLog application...
python app.py