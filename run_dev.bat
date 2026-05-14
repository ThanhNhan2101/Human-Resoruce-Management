@echo off
REM HRM Project - Startup Script for Windows
REM Usage: run_dev.bat [command]
REM Commands: web, celery, beat, all, stop

setlocal enabledelayedexpansion

set PROJECT_DIR=%~dp0
cd /d %PROJECT_DIR%

REM Colors (Windows doesn't support ANSI, so using basic output)
echo.
echo ==================================================
echo HRM Project - Development Server Startup
echo ==================================================
echo.

REM Check if python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python or activate virtual environment.
    exit /b 1
)

REM Parse arguments
if "%1"=="" (
    set command=all
) else (
    set command=%1
)

if "%command%"=="web" (
    echo Starting Django Development Server...
    echo Server will be available at: http://localhost:8000
    python manage.py runserver
    
) else if "%command%"=="celery" (
    echo Starting Celery Worker...
    echo Make sure Redis is running on localhost:6379
    celery -A config worker -l info
    
) else if "%command%"=="beat" (
    echo Starting Celery Beat (Scheduler)...
    echo Make sure Redis is running on localhost:6379
    celery -A config beat -l info
    
) else if "%command%"=="all" (
    echo.
    echo To run all services, open multiple terminal windows and run:
    echo.
    echo Terminal 1 - Django Web Server:
    echo   python manage.py runserver
    echo.
    echo Terminal 2 - Redis (if not already running):
    echo   redis-server
    echo.
    echo Terminal 3 - Celery Worker:
    echo   celery -A config worker -l info
    echo.
    echo Terminal 4 (Optional) - Celery Beat:
    echo   celery -A config beat -l info
    echo.
    
) else if "%command%"=="stop" (
    echo.
    echo To stop services:
    echo - Celery: Press Ctrl+C in the terminal
    echo - Django: Press Ctrl+C in the terminal
    echo.
) else (
    echo Unknown command: %command%
    echo.
    echo Available commands:
    echo   web   - Start Django development server
    echo   celery- Start Celery worker
    echo   beat  - Start Celery beat scheduler
    echo   all   - Show instructions for running all services
    echo   stop  - Show how to stop services
    echo.
)

endlocal
