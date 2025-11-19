#!/bin/bash
# ============================================
# Amazon Product Success Prediction - SETUP
# One-click installation script for Linux/Mac
# ============================================

echo ""
echo "========================================================"
echo "   Amazon Product Success Prediction - SETUP"
echo "========================================================"
echo ""
echo "This script will install everything you need."
echo ""
read -p "Press Enter to continue..."

echo ""
echo "[1/5] Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8+ from your package manager"
    exit 1
fi
echo "✓ Python found: $(python3 --version)"

echo ""
echo "[2/5] Checking Docker installation..."
if ! command -v docker &> /dev/null; then
    echo "WARNING: Docker is not installed"
    echo "Docker is needed for the PostgreSQL database"
    read -p "Continue without Docker? (y/n): " CONTINUE
    if [ "$CONTINUE" != "y" ]; then
        exit 1
    fi
else
    echo "✓ Docker found: $(docker --version)"
fi

echo ""
echo "[3/5] Installing Python dependencies..."
python3 -m pip install --upgrade pip
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi
echo "✓ Dependencies installed!"

echo ""
echo "[4/5] Starting PostgreSQL database..."
if command -v docker &> /dev/null; then
    docker-compose up -d
    if [ $? -eq 0 ]; then
        echo "✓ Database started!"
        echo "Waiting for database to be ready..."
        sleep 5
    else
        echo "WARNING: Could not start Docker containers"
    fi
fi

echo ""
echo "[5/5] Setting up data warehouse and training ML models..."
python3 src/etl_load_dw.py
echo "✓ Setup complete!"

echo ""
echo "========================================================"
echo "                 SETUP COMPLETE!"
echo "========================================================"
echo ""
echo "You can now run the application using:"
echo "  • ./run.sh (Linux/Mac)"
echo "  • Or: streamlit run app.py"
echo ""
echo "========================================================"
echo ""
