@echo off
REM ============================================
REM Amazon Product Success Prediction - SETUP
REM One-click installation script
REM ============================================

color 0A
echo.
echo ========================================================
echo    Amazon Product Success Prediction - SETUP
echo ========================================================
echo.
echo This script will install everything you need to run the application.
echo.
echo What will be installed:
echo   - Python dependencies (pandas, streamlit, scikit-learn, etc.)
echo   - Database setup (PostgreSQL via Docker)
echo   - Machine Learning models training
echo.
echo ========================================================
echo.
pause

echo.
echo [1/5] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)
echo ✓ Python found!

echo.
echo [2/5] Checking Docker installation...
docker --version >nul 2>&1
if errorlevel 1 (
    echo WARNING: Docker is not installed
    echo Docker is needed for the PostgreSQL database
    echo You can download Docker Desktop from: https://www.docker.com/products/docker-desktop
    echo.
    set /p CONTINUE="Do you want to continue without Docker? (y/n): "
    if /i not "%CONTINUE%"=="y" exit /b 1
) else (
    echo ✓ Docker found!
)

echo.
echo [3/5] Installing Python dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install Python dependencies
    pause
    exit /b 1
)
echo ✓ Dependencies installed!

echo.
echo [4/5] Starting PostgreSQL database...
docker-compose up -d
if errorlevel 1 (
    echo WARNING: Could not start Docker containers
    echo The app will still work but without database features
) else (
    echo ✓ Database started!
    echo Waiting for database to be ready...
    timeout /t 5 /nobreak >nul
)

echo.
echo [5/5] Setting up the data warehouse and training ML models...
python src/etl_load_dw.py
if errorlevel 1 (
    echo WARNING: Data warehouse setup failed
    echo The app will still work with the basic model
)
echo ✓ Setup complete!

echo.
echo ========================================================
echo                  SETUP COMPLETE!
echo ========================================================
echo.
echo You can now run the application using:
echo   • Double-click RUN.bat (Recommended for beginners)
echo   • Or run: launch_apps.ps1
echo.
echo The application will open in your web browser automatically.
echo ========================================================
echo.
pause
