# src/train_model_from_dw.py

import os
import re
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

from db_connection import get_connection


def extract_clean_category(category_str: str) -> str:
    """
    Extrae la primera categoría (más general) de la jerarquía
    y la limpia para mostrarla de forma legible.
    
    Ejemplo:
    'Computers&Accessories|Cables|USBCables' -> 'Computers & Accessories'
    'Electronics|HomeAudio|Speakers' -> 'Electronics'
    """
    if pd.isna(category_str) or category_str == "Unknown":
        return "Unknown"
    
    # Tomar la PRIMERA parte de la jerarquía (más general)
    parts = str(category_str).split("|")
    first_part = parts[0] if parts else "Unknown"
    
    # Separar palabras pegadas con & o mayúsculas
    # Separar por &
    clean = first_part.replace("&", " & ")
    # Insertar espacio antes de mayúsculas (CamelCase)
    clean = re.sub(r'([a-z])([A-Z])', r'\1 \2', clean)
    # Insertar espacio entre número/letra mayúscula y mayúscula siguiente
    clean = re.sub(r'([0-9A-Z])([A-Z][a-z])', r'\1 \2', clean)
    
    return clean.strip()


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
                FROM fact_product_performance f
                JOIN dim_category c
                    ON f.category_key = c.category_key;
    """

    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


def prepare_data(df: pd.DataFrame):
    """
    Prepara X, y y el encoder de categoría a partir
    del DataFrame leído desde el DW.
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

    # Limpiar categorías para hacerlas más legibles
    print("Limpiando nombres de categorías...")
    df["category_display"] = df["category"].apply(extract_clean_category)
    
    print(f"Ejemplos de categorías limpias:")
    print(df[["category", "category_display"]].drop_duplicates().head(10))

    # Codificar categoría limpia con LabelEncoder
    encoder = LabelEncoder()
    df["category_encoded"] = encoder.fit_transform(df["category_display"])

    feature_cols = [
        "discounted_price",
        "actual_price",
        "discount_percentage",
        "rating",
        "rating_count",
        "category_encoded",
    ]

    X = df[feature_cols]
    y = df["is_success"].astype(int)

    return X, y, encoder


def train_and_save_model(X, y, encoder):
    """
    Entrena el modelo RandomForest y guarda el modelo
    y el encoder en la carpeta models/.
    """
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=300,
        random_state=42,
        n_jobs=-1,
    )

    model.fit(X_train, y_train)

    # Evaluación
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)

    print(f"Accuracy del modelo (desde DW): {acc:.4f}")
    print("\nReporte de clasificación:")
    print(classification_report(y_test, y_pred))

    # Guardar modelo y encoder (mismos nombres que usa app.py)
    os.makedirs("models", exist_ok=True)

    joblib.dump(model, "models/modelo_random_forest.pkl")
    joblib.dump(encoder, "models/encoder_category.pkl")

    print("\nModelo y encoder guardados en carpeta 'models/'.")


def main():
    print("Leyendo datos desde el Data Warehouse (PostgreSQL)...")
    df = load_data_from_dw()
    print(f"Registros leídos: {len(df)}")

    print("Preparando datos para entrenamiento...")
    X, y, encoder = prepare_data(df)

    print("Entrenando modelo Random Forest...")
    train_and_save_model(X, y, encoder)


if __name__ == "__main__":
    main()
