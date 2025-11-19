# 📦 Amazon Product Success Prediction - Data Warehouse Project

## 🎯 For End Users - Get Started in 30 Seconds!

### ⚡ Quick Start (Windows Users)
1. **Double-click: `SETUP.bat`** (One-time setup - installs everything)
2. **Double-click: `RUN.bat`** (Launches the application)
3. **Open your browser** at http://localhost:8501 or http://localhost:8502

### 📚 New to this? Read: [QUICKSTART.md](QUICKSTART.md)
**Complete beginner-friendly guide with screenshots and troubleshooting!**

---

## 📋 Project Overview

This project implements a complete data warehouse solution for predicting product success on Amazon using machine learning. It includes:

- **ETL Pipeline**: Extract, Transform, Load data from CSV to PostgreSQL data warehouse
- **Machine Learning Model**: Random Forest classifier to predict product success
- **Two Streamlit Web Apps**: For products with and without reviews
- **Data Warehouse**: PostgreSQL star schema with dimension and fact tables
- **Entrepreneur Tools**: Market analysis and success prediction tools for new sellers

**Product Success Criteria:**
- Rating ≥ 4.0
- Number of reviews ≥ 50



------



## 🚀 For Entrepreneurs## 🚀 **NEW: For Entrepreneurs**



### Want to sell on Amazon but don't have reviews yet?### Want to sell on Amazon but don't have reviews yet?



We provide two specialized Streamlit applications to help you make data-driven decisions:We've added special tools to help you make data-driven decisions based on **price and category** alone:



#### 🎨 Web Applications#### 🎨 **Web Applications (Streamlit)**



**1. 🚀 Entrepreneur Advisor App** - For NEW products WITHOUT reviews:1. **� Entrepreneur Advisor App** - Beautiful UI for market analysis:

```bash   ```bash

streamlit run entrepreneur_advisor_app.py   streamlit run entrepreneur_advisor_app.py

```   ```

   Visit: http://localhost:8501

**Features:**

- Predict success based on price and category alone2. **📦 Product Success Predictor** - For products with existing reviews:

- Category success rate analysis (83% for Computers & Accessories)   ```bash

- Price optimization recommendations     streamlit run app.py

- Competition analysis   ```

- Profit calculator   Visit: http://localhost:8501

- Based on 1,465 real Amazon products

#### 📚 **Documentation**

Visit: http://localhost:8501

3. **�📊 [Quick Decision Guide](QUICK_GUIDE.md)** - Start here for instant answers

---4. **📖 [Complete Entrepreneur Guide](ENTREPRENEUR_GUIDE.md)** - Detailed strategies and insights



**2. 📦 Product Success Predictor** - For products WITH existing reviews:#### 🔧 **Command Line Tools**

```bash

streamlit run app.py5. **🎯 Interactive Advisor (Console)** - Test product ideas:

```   ```bash

   python entrepreneur_advisor.py

**Features:**   ```

- Predict success for products with ratings and reviews

- ML-powered predictions using Random Forest6. **📈 Market Analysis Report** - Comprehensive market insights:

- Real-time probability scores   ```bash

   python market_analysis_report.py

Visit: http://localhost:8501   ```



---**Key Findings:**

- ✅ 83% success rate in Computers & Accessories

**💡 Quick Launch (Both Apps):**- ✅ Optimal price range: $299-999

```powershell- ✅ Recommended discount: 45-55%

.\launch_apps.ps1- ✅ Best categories identified for new sellers

```

## 🛠️ Technology Stack

**Key Market Insights:**

- ✅ 83% success rate in Computers & Accessories- **Python 3.12+**

- ✅ 100% success rate in Office Products- **PostgreSQL** (via Docker)

- ✅ Optimal price range: $299-999- **Machine Learning**: scikit-learn, pandas

- ✅ Recommended discount: 45-55%- **Web Framework**: Streamlit

- **Database**: psycopg2

---

## 📁 Project Structure

## 🛠️ Technology Stack

```

- **Python 3.12+**dataWare-house/

- **PostgreSQL** (via Docker)├── app.py                          # Streamlit web application

- **Machine Learning**: scikit-learn, pandas├── check_encoder.py                # Utility to check encoded categories

- **Web Framework**: Streamlit├── docker-compose.yml              # PostgreSQL container configuration

- **Database**: psycopg2-binary├── data/

│   └── amazon.csv                  # Source dataset

---├── models/

│   ├── modelo_random_forest.pkl    # Trained ML model

## 📁 Project Structure│   └── encoder_category.pkl        # Category encoder

└── src/

```    ├── __init__.py

dataWare-house/    ├── db_connection.py            # PostgreSQL connection utilities

├── app.py                          # Streamlit app (with reviews)    ├── etl_load_dw.py              # ETL pipeline to load data warehouse

├── entrepreneur_advisor_app.py     # Streamlit app (without reviews)    ├── preprocessing.py            # Data cleaning and preprocessing

├── launch_apps.ps1                 # PowerShell launcher for apps    ├── train_model.py              # Train model from CSV

├── docker-compose.yml              # PostgreSQL container configuration    └── train_model_from_dw.py      # Train model from data warehouse

├── requirements.txt                # Python dependencies```

├── data/

│   └── amazon.csv                  # Source dataset (1,465 products)## 🚀 Getting Started

├── models/

│   ├── modelo_random_forest.pkl    # Trained ML model### Prerequisites

│   └── encoder_category.pkl        # Category encoder

└── src/- Python 3.12 or higher

    ├── __init__.py- Docker Desktop (for PostgreSQL)

    ├── db_connection.py            # PostgreSQL connection utilities- Git

    ├── etl_load_dw.py              # ETL pipeline to load data warehouse

    ├── preprocessing.py            # Data cleaning and preprocessing### 1. Clone the Repository

    ├── train_model.py              # Train model from CSV

    └── train_model_from_dw.py      # Train model from data warehouse```bash

```git clone https://github.com/isaccv707/dataWare-house.git

cd dataWare-house

---```



## 🚀 Getting Started### 2. Install Python Dependencies



### Prerequisites```bash

pip install -r requirements.txt

- **Python 3.12+**```

- **Docker Desktop** (for PostgreSQL)

- **Git**If `requirements.txt` doesn't exist, install manually:



### 1. Clone the Repository```bash

pip install pandas scikit-learn streamlit psycopg2-binary joblib

```bash```

git clone https://github.com/isaccv707/dataWare-house.git

cd dataWare-house### 3. Start PostgreSQL Data Warehouse

```

```bash

### 2. Install Python Dependenciesdocker-compose up -d

```

```bash

pip install -r requirements.txtThis will start a PostgreSQL container with:

```- **Host**: localhost

- **Port**: 5432

### 3. Start PostgreSQL Data Warehouse- **Database**: amazon_dw

- **User**: postgres

```bash- **Password**: postgres

docker-compose up -d

```Verify the container is running:



This starts a PostgreSQL container with:```bash

- **Host**: localhostdocker ps

- **Port**: 5432```

- **Database**: dw_amazon

- **User**: postgres### 4. Run ETL Pipeline (Load Data Warehouse)

- **Password**: postgres123

Load the data from CSV into the PostgreSQL data warehouse:

Verify the container is running:

```bash```bash

docker pspython src/etl_load_dw.py

``````



### 4. Run ETL Pipeline (Load Data Warehouse)This script will:

- Create dimension and fact tables

Load data from CSV into the PostgreSQL data warehouse:- Clean and transform the data

- Load data into the data warehouse

```bash- Show statistics about loaded records

python src/etl_load_dw.py

```### 5. Train the Machine Learning Model



This script will:Train the model using data from the data warehouse:

- Create dimension and fact tables

- Clean and transform the data```bash

- Load data into the data warehousepython src/train_model_from_dw.py

- Show statistics about loaded records```



### 5. Train the Machine Learning ModelThis will:

- Read data from PostgreSQL

Train the model using data from the data warehouse:- Clean and encode categories (using first/main category)

- Train a Random Forest classifier

```bash- Save the model and encoder to `models/` folder

python src/train_model_from_dw.py- Display accuracy and classification report

```

**Expected Output:**

This will:```

- Read data from PostgreSQLAccuracy del modelo (desde DW): 0.9963

- Clean and encode categories

- Train a Random Forest classifier (300 trees)Reporte de clasificación:

- Save the model and encoder to `models/` folder              precision    recall  f1-score   support

- Display accuracy and classification report           0       1.00      1.00      1.00       240

           1       1.00      0.97      0.98        31

**Expected Output:**```

```

Accuracy del modelo (desde DW): 0.9963### 6. Run the Web Application



Reporte de clasificación:Start the Streamlit dashboard:

              precision    recall  f1-score   support

           0       1.00      1.00      1.00       240```bash

           1       1.00      0.97      0.98        31streamlit run app.py

``````



### 6. Run the Web ApplicationsThe application will open in your browser at `http://localhost:8501`



**Option A: Launch both apps with PowerShell:**## 🔍 Category Improvements

```powershell

.\launch_apps.ps1The project now uses **cleaned, user-friendly categories**:

```

**Before:**

**Option B: Launch individually:**```

Computers&Accessories|Accessories&Peripherals|Cables&Accessories|Cables|USBCables

For products WITH reviews:```

```bash

streamlit run app.py**After:**

``````

Computers & Accessories

For products WITHOUT reviews:```

```bash

streamlit run entrepreneur_advisor_app.pyCategories are now limited to 9 main categories:

```1. Car & Motorbike

2. Computers & Accessories

The applications will open in your browser at `http://localhost:8501`3. Electronics

4. Health & Personal Care

---5. Home & Kitchen

6. Home Improvement

## 🔍 Category Improvements7. Musical Instruments

8. Office Products

The project uses **cleaned, user-friendly categories**:9. Toys & Games



**Before:**## 📊 Using the Application

```

Computers&Accessories|Accessories&Peripherals|Cables&Accessories|Cables|USBCables1. **Enter Product Details:**

```   - Original Price ($)

   - Discounted Price ($)

**After:**   - Rating (1-5)

```   - Number of Reviews

Computers & Accessories   - Product Category

```

2. **Automatic Discount Calculation:**

**9 Main Categories:**   - The app automatically calculates discount percentage

1. Car & Motorbike

2. Computers & Accessories3. **Get Prediction:**

3. Electronics   - Click "🔍 Predecir éxito del producto"

4. Health & Personal Care   - See success probability and prediction result

5. Home & Kitchen

6. Home Improvement## 🧪 Development Utilities

7. Musical Instruments

8. Office Products### Check Encoded Categories

9. Toys & Games

View all categories in the encoder:

---

```bash

## 📊 Using the Applicationspython check_encoder.py

```

### Entrepreneur Advisor App (No Reviews Needed)

### Train Model from CSV (Alternative)

1. **Select Category**: Choose from 9 main categories

2. **Set Your Price**: Enter your selling price ($)If you want to train directly from CSV without using the data warehouse:

3. **Set Discount**: Enter discount percentage

4. **Get Analysis**: ```bash

   - Success probability based on similar productspython src/train_model.py

   - Expected ratings and reviews```

   - Competition analysis

   - Profit calculations### Database Connection Test

   - Actionable recommendations

Test the PostgreSQL connection:

### Product Success Predictor (With Reviews)

```python

1. **Enter Product Details:**from src.db_connection import get_connection

   - Original Price ($)

   - Discounted Price ($)conn = get_connection()

   - Rating (1-5)print("Connection successful!")

   - Number of Reviewsconn.close()

   - Product Category```



2. **Automatic Calculations:**## 🗄️ Data Warehouse Schema

   - Discount percentage calculated automatically

### Dimension Tables

3. **Get Prediction:**

   - Success probability**dim_category**

   - Classification result- `category_key` (PK): Auto-increment ID

   - Visual progress bar- `full_category`: Complete category hierarchy

- `main_category`: First-level category

---- `sub_category`: Second-level category



## 🗄️ Data Warehouse Schema### Fact Tables



### Dimension Tables**fact_product_performance**

- `product_key` (PK): Auto-increment ID

**dim_category**- `product_id`: Original product identifier

- `category_key` (PK): Auto-increment ID- `category_key` (FK): Reference to dim_category

- `full_category`: Complete category hierarchy- `discounted_price`: Price after discount

- `main_category`: First-level category- `actual_price`: Original price

- `sub_category_1` through `sub_category_4`: Additional levels- `discount_percentage`: Percentage discount

- `rating`: Product rating (0-5)

**dim_product**- `rating_count`: Number of reviews

- `product_key` (PK): Auto-increment ID- `is_success`: Target variable (0 or 1)

- `product_id`: Original product identifier

- `product_name`: Product title## 🔧 Troubleshooting

- `about_product`: Product description

- `img_link`, `product_link`: URLs### PostgreSQL Connection Issues



### Fact TableIf you get connection errors:



**fact_product_performance**1. Check Docker is running:

- `product_key` (FK): Reference to dim_product   ```bash

- `category_key` (FK): Reference to dim_category   docker ps

- `discounted_price`: Price after discount   ```

- `actual_price`: Original price

- `discount_percentage`: Percentage discount2. Restart the container:

- `rating`: Product rating (0-5)   ```bash

- `rating_count`: Number of reviews   docker-compose restart

- `is_success`: Target variable (0 or 1)   ```



---3. Check logs:

   ```bash

## 🔧 Troubleshooting   docker-compose logs

   ```

### PostgreSQL Connection Issues

### Model Not Found

If you get connection errors:

If the app can't find the model files:

1. Check Docker is running:

   ```bash1. Ensure you've run the training script:

   docker ps   ```bash

   ```   python src/train_model_from_dw.py

   ```

2. Restart the container:

   ```bash2. Check the `models/` folder exists and contains:

   docker-compose restart   - `modelo_random_forest.pkl`

   ```   - `encoder_category.pkl`



3. Check logs:### Data Not Loading

   ```bash

   docker-compose logsIf ETL pipeline fails:

   ```

1. Verify the CSV file exists at `data/amazon.csv`

4. Verify port 5432 is not in use:2. Check PostgreSQL is accessible

   ```powershell3. Review error messages in console

   netstat -ano | findstr :5432

   ```## 📈 Model Performance



### Model Not FoundThe current model achieves:

- **Accuracy**: 99.63%

If the app can't find model files:- **Precision**: 100% (both classes)

- **Recall**: 100% (class 0), 97% (class 1)

1. Train the model:

   ```bash## 🤝 Contributing

   python src/train_model_from_dw.py

   ```1. Create a new branch for your feature

2. Make your changes

2. Verify `models/` folder contains:3. Test thoroughly

   - `modelo_random_forest.pkl`4. Submit a pull request

   - `encoder_category.pkl`

## 📝 Notes

### Streamlit Port Already in Use

- The project uses a **star schema** for the data warehouse

If port 8501 is occupied:- Categories are automatically cleaned and simplified

- The model is trained on 1,351 products after data cleaning

```bash- Random Forest with 300 estimators is used for classification

streamlit run app.py --server.port 8502

```## 🔐 Security Note



---The default PostgreSQL credentials are for development only. **Do not use these in production!**



## 📈 Model PerformanceFor production:

1. Change database credentials in `docker-compose.yml`

The current Random Forest model achieves:2. Update connection string in `src/db_connection.py`

- **Accuracy**: 99.63%3. Use environment variables for sensitive data

- **Precision**: 100% (both classes)

- **Recall**: 100% (class 0), 97% (class 1)## 📧 Contact

- **F1-Score**: 1.00 (class 0), 0.98 (class 1)

- **Repository**: https://github.com/isaccv707/dataWare-house

**Model Configuration:**---

- Algorithm: Random Forest Classifier
- Number of Estimators: 300 trees
- Training Data: 1,351 products (after cleaning)
- Features: 6 (price, discount, rating, reviews, category)

---

## 🎯 Key Insights from Data Analysis

Based on 1,465 real Amazon products:

### Category Success Rates:
- **Office Products**: 100% success rate (31 products)
- **Computers & Accessories**: 83% success rate (453 products)
- **Electronics**: 73% success rate (526 products)
- **Home & Kitchen**: 66% success rate (448 products)

### Optimal Price Ranges:
- **$500-1,000**: 77% success rate (Best!)
- **$200-500**: 71% success rate (Beginner-friendly)
- **$1,000-2,000**: 69% success rate (Good margins)

### Discount Strategy:
- **40-60%**: Recommended for new sellers
- **20-40%**: Works with strong brand/quality
- **60-80%**: Very competitive, lower margins

---

## 🤝 Contributing

1. Create a new branch for your feature
2. Make your changes
3. Test thoroughly
4. Submit a pull request

---

## 🔐 Security Note

⚠️ **Important**: The default PostgreSQL credentials are for **development only**. 

**Do not use these in production!**

For production:
1. Change database credentials in `docker-compose.yml`
2. Update connection string in `src/db_connection.py`
3. Use environment variables for sensitive data
4. Enable SSL connections

---

## 📝 Notes

- The project uses a **star schema** for the data warehouse
- Categories are automatically cleaned and simplified
- The model is trained on 1,351 products after data cleaning
- Random Forest with 300 estimators provides high accuracy
- Data is from Amazon India (prices in $)

---

## 📧 Contact & Repository

- **GitHub**: https://github.com/isaccv707/dataWare-house
- **Branch**: categorias-2
- **Owner**: isaccv707

---

## 📄 License

This is an academic/educational project for learning data warehousing and machine learning concepts.

---

**Built with ❤️ for data-driven entrepreneurship on Amazon**
