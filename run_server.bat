@echo off
echo Starting Personal Finance Tracker...
echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Running migrations...
python manage.py migrate

echo.
echo Starting development server...
echo Access the application at: http://localhost:8000
echo.
python manage.py runserver
