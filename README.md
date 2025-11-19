# Amazon Product Success Prediction - Data Warehouse Project

## 📋 Project Overview

This project implements a complete data warehouse solution for predicting product success on Amazon using machine learning. It includes:

- **ETL Pipeline**: Extract, Transform, Load data from CSV to PostgreSQL data warehouse
- **Machine Learning Model**: Random Forest classifier to predict product success
- **Web Application**: Streamlit dashboard for real-time predictions

**Product Success Criteria:**
- Rating ≥ 4.0
- Number of reviews ≥ 50

## 🛠️ Technology Stack

- **Python 3.12+**
- **PostgreSQL** (via Docker)
- **Machine Learning**: scikit-learn, pandas
- **Web Framework**: Streamlit
- **Database**: psycopg2

## 📁 Project Structure

```
dataWare-house/
├── app.py                          # Streamlit web application
├── check_encoder.py                # Utility to check encoded categories
├── docker-compose.yml              # PostgreSQL container configuration
├── data/
│   └── amazon.csv                  # Source dataset
├── models/
│   ├── modelo_random_forest.pkl    # Trained ML model
│   └── encoder_category.pkl        # Category encoder
└── src/
    ├── __init__.py
    ├── db_connection.py            # PostgreSQL connection utilities
    ├── etl_load_dw.py              # ETL pipeline to load data warehouse
    ├── preprocessing.py            # Data cleaning and preprocessing
    ├── train_model.py              # Train model from CSV
    └── train_model_from_dw.py      # Train model from data warehouse
```

## 🚀 Getting Started

### Prerequisites

- Python 3.12 or higher
- Docker Desktop (for PostgreSQL)
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/isaccv707/dataWare-house.git
cd dataWare-house
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` doesn't exist, install manually:

```bash
pip install pandas scikit-learn streamlit psycopg2-binary joblib
```

### 3. Start PostgreSQL Data Warehouse

```bash
docker-compose up -d
```

This will start a PostgreSQL container with:
- **Host**: localhost
- **Port**: 5432
- **Database**: amazon_dw
- **User**: postgres
- **Password**: postgres

Verify the container is running:

```bash
docker ps
```

### 4. Run ETL Pipeline (Load Data Warehouse)

Load the data from CSV into the PostgreSQL data warehouse:

```bash
python src/etl_load_dw.py
```

This script will:
- Create dimension and fact tables
- Clean and transform the data
- Load data into the data warehouse
- Show statistics about loaded records

### 5. Train the Machine Learning Model

Train the model using data from the data warehouse:

```bash
python src/train_model_from_dw.py
```

This will:
- Read data from PostgreSQL
- Clean and encode categories (using first/main category)
- Train a Random Forest classifier
- Save the model and encoder to `models/` folder
- Display accuracy and classification report

**Expected Output:**
```
Accuracy del modelo (desde DW): 0.9963

Reporte de clasificación:
              precision    recall  f1-score   support
           0       1.00      1.00      1.00       240
           1       1.00      0.97      0.98        31
```

### 6. Run the Web Application

Start the Streamlit dashboard:

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## 🔍 Category Improvements

The project now uses **cleaned, user-friendly categories**:

**Before:**
```
Computers&Accessories|Accessories&Peripherals|Cables&Accessories|Cables|USBCables
```

**After:**
```
Computers & Accessories
```

Categories are now limited to 9 main categories:
1. Car & Motorbike
2. Computers & Accessories
3. Electronics
4. Health & Personal Care
5. Home & Kitchen
6. Home Improvement
7. Musical Instruments
8. Office Products
9. Toys & Games

## 📊 Using the Application

1. **Enter Product Details:**
   - Original Price (₹)
   - Discounted Price (₹)
   - Rating (1-5)
   - Number of Reviews
   - Product Category

2. **Automatic Discount Calculation:**
   - The app automatically calculates discount percentage

3. **Get Prediction:**
   - Click "🔍 Predecir éxito del producto"
   - See success probability and prediction result

## 🧪 Development Utilities

### Check Encoded Categories

View all categories in the encoder:

```bash
python check_encoder.py
```

### Train Model from CSV (Alternative)

If you want to train directly from CSV without using the data warehouse:

```bash
python src/train_model.py
```

### Database Connection Test

Test the PostgreSQL connection:

```python
from src.db_connection import get_connection

conn = get_connection()
print("Connection successful!")
conn.close()
```

## 🗄️ Data Warehouse Schema

### Dimension Tables

**dim_category**
- `category_key` (PK): Auto-increment ID
- `full_category`: Complete category hierarchy
- `main_category`: First-level category
- `sub_category`: Second-level category

### Fact Tables

**fact_product_performance**
- `product_key` (PK): Auto-increment ID
- `product_id`: Original product identifier
- `category_key` (FK): Reference to dim_category
- `discounted_price`: Price after discount
- `actual_price`: Original price
- `discount_percentage`: Percentage discount
- `rating`: Product rating (0-5)
- `rating_count`: Number of reviews
- `is_success`: Target variable (0 or 1)

## 🔧 Troubleshooting

### PostgreSQL Connection Issues

If you get connection errors:

1. Check Docker is running:
   ```bash
   docker ps
   ```

2. Restart the container:
   ```bash
   docker-compose restart
   ```

3. Check logs:
   ```bash
   docker-compose logs
   ```

### Model Not Found

If the app can't find the model files:

1. Ensure you've run the training script:
   ```bash
   python src/train_model_from_dw.py
   ```

2. Check the `models/` folder exists and contains:
   - `modelo_random_forest.pkl`
   - `encoder_category.pkl`

### Data Not Loading

If ETL pipeline fails:

1. Verify the CSV file exists at `data/amazon.csv`
2. Check PostgreSQL is accessible
3. Review error messages in console

## 📈 Model Performance

The current model achieves:
- **Accuracy**: 99.63%
- **Precision**: 100% (both classes)
- **Recall**: 100% (class 0), 97% (class 1)

## 🤝 Contributing

1. Create a new branch for your feature
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## 📝 Notes

- The project uses a **star schema** for the data warehouse
- Categories are automatically cleaned and simplified
- The model is trained on 1,351 products after data cleaning
- Random Forest with 300 estimators is used for classification

## 🔐 Security Note

The default PostgreSQL credentials are for development only. **Do not use these in production!**

For production:
1. Change database credentials in `docker-compose.yml`
2. Update connection string in `src/db_connection.py`
3. Use environment variables for sensitive data

## 📧 Contact

- **Repository**: https://github.com/isaccv707/dataWare-house
---
