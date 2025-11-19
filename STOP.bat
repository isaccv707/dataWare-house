@echo off
REM ============================================
REM Amazon Product Success Prediction - STOP
REM Stop all services
REM ============================================

color 0C
echo.
echo ========================================================
echo    Stopping Amazon Product Success Prediction
echo ========================================================
echo.

echo Stopping Docker containers...
docker-compose down
if errorlevel 1 (
    echo Could not stop Docker containers (they may not be running)
) else (
    echo ✓ Docker containers stopped
)

echo.
echo Stopping any running Streamlit processes...
taskkill /F /IM streamlit.exe >nul 2>&1
if errorlevel 1 (
    echo No Streamlit processes found
) else (
    echo ✓ Streamlit processes stopped
)

echo.
echo ========================================================
echo                  All services stopped
echo ========================================================
echo.
pause
