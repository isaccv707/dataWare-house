# Launch Script for Streamlit Apps
# Run both apps on different ports

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "  Amazon Success Prediction Apps Launcher" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Available applications:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Product Success Predictor (app.py)" -ForegroundColor Green
Write-Host "   - For products with existing reviews" -ForegroundColor Gray
Write-Host "   - Port: 8501" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Entrepreneur Advisor (entrepreneur_advisor_app.py)" -ForegroundColor Magenta
Write-Host "   - For new products without reviews" -ForegroundColor Gray
Write-Host "   - Port: 8502" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Both apps (side by side)" -ForegroundColor Cyan
Write-Host ""

$choice = Read-Host "Enter your choice (1, 2, or 3)"

switch ($choice) {
    "1" {
        Write-Host "`nLaunching Product Success Predictor..." -ForegroundColor Green
        Write-Host "Visit: http://localhost:8501" -ForegroundColor Cyan
        streamlit run app.py
    }
    "2" {
        Write-Host "`nLaunching Entrepreneur Advisor..." -ForegroundColor Magenta
        Write-Host "Visit: http://localhost:8502" -ForegroundColor Cyan
        streamlit run entrepreneur_advisor_app.py --server.port 8502
    }
    "3" {
        Write-Host "`nLaunching both applications..." -ForegroundColor Cyan
        Write-Host "Product Predictor: http://localhost:8501" -ForegroundColor Green
        Write-Host "Entrepreneur Advisor: http://localhost:8502" -ForegroundColor Magenta
        Write-Host ""
        Write-Host "Press Ctrl+C to stop both apps" -ForegroundColor Yellow
        
        # Launch first app in background
        Start-Process powershell -ArgumentList "-NoExit", "-Command", "streamlit run app.py"
        
        # Wait a bit
        Start-Sleep -Seconds 3
        
        # Launch second app
        streamlit run entrepreneur_advisor_app.py --server.port 8502
    }
    default {
        Write-Host "Invalid choice. Please run again and select 1, 2, or 3." -ForegroundColor Red
    }
}
