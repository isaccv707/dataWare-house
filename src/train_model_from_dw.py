# src/train_model_from_dw.py

import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

from db_connection import get_connection


def load_data_from_dw() -> pd.DataFrame:
    """
    Lee los datos de la tabla de hechos + dimensión de categorías
    desde PostgreSQL (DW) y devuelve un DataFrame listo para modelar.
    """
    conn = get_connection()

    query = """
        SELECT
            f.discounted_price,
            f.actual_price,
            f.discount_percentage,
            f.rating,
            f.rating_count,
            f.is_success,
            c.full_category AS category
        FROM dw_amazon.fact_product_performance f
        JOIN dw_amazon.dim_category c
          ON f.category_key = c.category_key;
    """

    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


def prepare_data(df: pd.DataFrame):
    """
    Prepara X, y a partir del DataFrame leído desde el DW.
    Extrae la categoría de nivel superior del campo full_category.
    """
    df = df.copy()

    # Aseguramos tipos numéricos
    numeric_cols = [
        "discounted_price",
        "actual_price",
        "discount_percentage",
        "rating",
        "rating_count",
        "is_success",
    ]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=numeric_cols + ["category"])

    # Extract top-level category from hierarchical category string
    # e.g., "Electronics|HomeTheater,TV&Video|Televisions" -> "Electronics"
    df["category"] = df["category"].astype(str).str.split("|").str[0]

    feature_cols = [
        "discounted_price",
        "actual_price",
        "discount_percentage",
        "rating",
        "rating_count",
        "category",
    ]

    X = df[feature_cols]
    y = df["is_success"].astype(int)

    return X, y


def train_and_save_model(X, y):
    """
    Entrena el modelo RandomForest y guarda el modelo
    y el preprocessor en la carpeta models/.
    """
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Create preprocessor for one-hot encoding the category column
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(drop='first', sparse_output=False, handle_unknown='ignore'), ['category'])
        ],
        remainder='passthrough'  # Keep numeric columns as-is
    )

    # Fit and transform training data
    X_train_transformed = preprocessor.fit_transform(X_train)
    X_test_transformed = preprocessor.transform(X_test)

    model = RandomForestClassifier(
        n_estimators=300,
        max_depth=15,
        min_samples_split=10,
        random_state=42,
        n_jobs=-1,
    )

    model.fit(X_train_transformed, y_train)

    # Evaluación
    y_pred = model.predict(X_test_transformed)
    acc = accuracy_score(y_test, y_pred)

    print(f"Accuracy del modelo (desde DW): {acc:.4f}")
    print("\nReporte de clasificación:")
    print(classification_report(y_test, y_pred))

    # Guardar modelo y preprocessor (mismos nombres que usa app.py)
    os.makedirs("models", exist_ok=True)

    joblib.dump(model, "models/modelo_random_forest.pkl")
    joblib.dump(preprocessor, "models/encoder_category.pkl")

    print("\nModelo y preprocessor guardados en carpeta 'models/'.")


def main():
    print("Leyendo datos desde el Data Warehouse (PostgreSQL)...")
    df = load_data_from_dw()
    print(f"Registros leídos: {len(df)}")

    print("Preparando datos para entrenamiento...")
    X, y = prepare_data(df)

    print("Entrenando modelo Random Forest...")
    train_and_save_model(X, y)


if __name__ == "__main__":
    main()
