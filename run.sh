#!/bin/bash
# ============================================
# Amazon Product Success Prediction - RUN
# One-click launcher for Linux/Mac
# ============================================

clear
echo ""
echo "========================================================"
echo "   Amazon Product Success Prediction"
echo "========================================================"
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please run ./setup.sh first"
    exit 1
fi

# Check if streamlit is installed
if ! python3 -c "import streamlit" &> /dev/null; then
    echo "ERROR: Required dependencies not found"
    echo "Please run ./setup.sh first"
    exit 1
fi

# Start Docker containers if Docker is available
if command -v docker &> /dev/null; then
    echo "Starting database..."
    docker-compose up -d > /dev/null 2>&1
fi

echo ""
echo "========================================================"
echo "       Choose which application to run:"
echo "========================================================"
echo ""
echo "  1 - Product Success Predictor"
echo "      (For products with existing reviews)"
echo "      Port: http://localhost:8501"
echo ""
echo "  2 - Entrepreneur Advisor"
echo "      (For new products without reviews)"
echo "      Port: http://localhost:8502"
echo ""
echo "  3 - Both Applications"
echo "      (Run both apps side by side)"
echo ""
echo "========================================================"
echo ""
read -p "Enter your choice (1, 2, or 3): " choice

case $choice in
    1)
        echo ""
        echo "Starting Product Success Predictor..."
        echo "Visit: http://localhost:8501"
        echo ""
        echo "Press Ctrl+C to stop the application"
        echo "========================================================"
        python3 -m streamlit run app.py
        ;;
    2)
        echo ""
        echo "Starting Entrepreneur Advisor..."
        echo "Visit: http://localhost:8502"
        echo ""
        echo "Press Ctrl+C to stop the application"
        echo "========================================================"
        python3 -m streamlit run entrepreneur_advisor_app.py --server.port 8502
        ;;
    3)
        echo ""
        echo "Starting both applications..."
        echo "Product Predictor: http://localhost:8501"
        echo "Entrepreneur Advisor: http://localhost:8502"
        echo ""
        echo "========================================================"
        
        # Run first app in background
        python3 -m streamlit run app.py > /dev/null 2>&1 &
        APP1_PID=$!
        
        # Wait a bit
        sleep 3
        
        # Run second app in background
        python3 -m streamlit run entrepreneur_advisor_app.py --server.port 8502 > /dev/null 2>&1 &
        APP2_PID=$!
        
        echo "Both applications are running!"
        echo "Press Enter to stop both applications..."
        read
        
        # Kill both processes
        kill $APP1_PID $APP2_PID 2>/dev/null
        echo "Applications stopped"
        ;;
    *)
        echo "Invalid choice. Please run the script again."
        exit 1
        ;;
esac
