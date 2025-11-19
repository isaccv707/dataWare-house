"""
System Requirements Checker
Verifies all dependencies are installed and configured correctly
"""

import sys
import subprocess
import platform

def print_header():
    print("\n" + "=" * 60)
    print("  Amazon Product Success Prediction - System Check")
    print("=" * 60 + "\n")

def print_result(check_name, passed, message=""):
    status = "✓ PASS" if passed else "✗ FAIL"
    color = "\033[92m" if passed else "\033[91m"
    reset = "\033[0m"
    
    print(f"{color}{status}{reset} - {check_name}")
    if message:
        print(f"      {message}")

def check_python_version():
    """Check if Python version is 3.8 or higher"""
    version = sys.version_info
    required = (3, 8)
    passed = version >= required
    
    message = f"Python {version.major}.{version.minor}.{version.micro} detected"
    if not passed:
        message += f" (Required: Python {required[0]}.{required[1]}+)"
    
    print_result("Python Version", passed, message)
    return passed

def check_pip():
    """Check if pip is installed"""
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"], 
                      capture_output=True, check=True)
        print_result("pip Package Manager", True)
        return True
    except:
        print_result("pip Package Manager", False, "pip is not installed")
        return False

def check_docker():
    """Check if Docker is installed and running"""
    try:
        result = subprocess.run(["docker", "--version"], 
                               capture_output=True, text=True)
        if result.returncode == 0:
            version = result.stdout.strip()
            print_result("Docker", True, version)
            
            # Check if Docker daemon is running
            result = subprocess.run(["docker", "ps"], 
                                   capture_output=True)
            if result.returncode == 0:
                print_result("Docker Daemon", True, "Running")
                return True
            else:
                print_result("Docker Daemon", False, "Not running - please start Docker Desktop")
                return False
        else:
            print_result("Docker", False, "Not installed (optional)")
            return False
    except FileNotFoundError:
        print_result("Docker", False, "Not installed (optional but recommended)")
        return False

def check_required_packages():
    """Check if required Python packages are installed"""
    required_packages = [
        'streamlit',
        'pandas',
        'numpy',
        'sklearn',
        'joblib',
        'psycopg2'
    ]
    
    all_installed = True
    for package in required_packages:
        try:
            __import__(package)
            print_result(f"Package: {package}", True)
        except ImportError:
            print_result(f"Package: {package}", False, "Not installed")
            all_installed = False
    
    return all_installed

def check_data_files():
    """Check if required data files exist"""
    import os
    
    files_to_check = [
        ('data/amazon.csv', 'Dataset'),
        ('models/modelo_random_forest.pkl', 'ML Model (will be created if missing)'),
        ('models/encoder_category.pkl', 'Category Encoder (will be created if missing)')
    ]
    
    all_exist = True
    for file_path, description in files_to_check:
        exists = os.path.exists(file_path)
        print_result(f"File: {description}", exists or "Model" in description, 
                    f"{file_path}")
        if not exists and "Model" not in description:
            all_exist = False
    
    return all_exist

def check_database_connection():
    """Check if PostgreSQL database is accessible"""
    try:
        import psycopg2
        conn = psycopg2.connect(
            dbname="dw_amazon",
            user="postgres",
            password="postgres123",
            host="localhost",
            port="5432"
        )
        conn.close()
        print_result("Database Connection", True, "PostgreSQL accessible at localhost:5432")
        return True
    except Exception as e:
        print_result("Database Connection", False, 
                    "Cannot connect (run docker-compose up -d)")
        return False

def main():
    print_header()
    
    results = {
        "Python Version": check_python_version(),
        "pip": check_pip(),
        "Docker": check_docker(),
        "Python Packages": check_required_packages(),
        "Data Files": check_data_files(),
        "Database": check_database_connection()
    }
    
    print("\n" + "=" * 60)
    print("  SUMMARY")
    print("=" * 60)
    
    passed = sum(results.values())
    total = len(results)
    
    print(f"\nPassed: {passed}/{total} checks")
    
    if passed == total:
        print("\n✓ System is ready! You can run the application.")
        print("\nNext steps:")
        print("  • Windows: Double-click RUN.bat")
        print("  • Linux/Mac: ./run.sh")
        print("  • Or: streamlit run app.py")
    else:
        print("\n✗ Some checks failed. Please fix the issues above.")
        print("\nTo fix:")
        print("  1. Install missing dependencies: pip install -r requirements.txt")
        print("  2. Start Docker: docker-compose up -d")
        print("  3. Run setup: python src/etl_load_dw.py")
        print("\nOr run the automated setup:")
        print("  • Windows: Double-click SETUP.bat")
        print("  • Linux/Mac: ./setup.sh")
    
    print("\n" + "=" * 60 + "\n")
    
    return 0 if passed == total else 1

if __name__ == "__main__":
    sys.exit(main())
