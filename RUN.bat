@echo off
REM ============================================
REM Amazon Product Success Prediction - RUN
REM One-click launcher
REM ============================================

color 0B
cls
echo.
echo ========================================================
echo    Amazon Product Success Prediction
echo ========================================================
echo.
echo Starting the application...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please run SETUP.bat first
    pause
    exit /b 1
)

REM Check if streamlit is installed
python -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo ERROR: Required dependencies not found
    echo Please run SETUP.bat first to install dependencies
    pause
    exit /b 1
)

REM Start Docker containers if Docker is available
docker --version >nul 2>&1
if not errorlevel 1 (
    echo Starting database...
    docker-compose up -d >nul 2>&1
)

echo.
echo ========================================================
echo        Choose which application to run:
echo ========================================================
echo.
echo   1 - Product Success Predictor
echo       (For products with existing reviews)
echo       Port: http://localhost:8501
echo.
echo   2 - Entrepreneur Advisor
echo       (For new products without reviews)
echo       Port: http://localhost:8502
echo.
echo   3 - Both Applications
echo       (Run both apps side by side)
echo.
echo ========================================================
echo.
set /p choice="Enter your choice (1, 2, or 3): "

if "%choice%"=="1" (
    echo.
    echo Starting Product Success Predictor...
    echo Visit: http://localhost:8501
    echo.
    echo Press Ctrl+C to stop the application
    echo ========================================================
    python -m streamlit run app.py
) else if "%choice%"=="2" (
    echo.
    echo Starting Entrepreneur Advisor...
    echo Visit: http://localhost:8502
    echo.
    echo Press Ctrl+C to stop the application
    echo ========================================================
    python -m streamlit run entrepreneur_advisor_app.py --server.port 8502
) else if "%choice%"=="3" (
    echo.
    echo Starting both applications...
    echo Product Predictor: http://localhost:8501
    echo Entrepreneur Advisor: http://localhost:8502
    echo.
    echo Press Ctrl+C in each window to stop the applications
    echo ========================================================
    start "Product Success Predictor" cmd /k "python -m streamlit run app.py"
    timeout /t 3 /nobreak >nul
    start "Entrepreneur Advisor" cmd /k "python -m streamlit run entrepreneur_advisor_app.py --server.port 8502"
    echo.
    echo Both applications are running in separate windows
    pause
) else (
    echo Invalid choice. Please run the script again and choose 1, 2, or 3.
    pause
    exit /b 1
)
