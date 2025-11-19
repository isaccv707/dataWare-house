import pandas as pd

def load_dataset(path: str):
    return pd.read_csv(path)

def extract_clean_category(category_str: str) -> str:
    """
    Extrae la categoría más específica (última) de la jerarquía
    y la limpia para mostrarla de forma legible.
    
    Ejemplo:
    'Computers&Accessories|Cables|USBCables' -> 'USB Cables'
    """
    if pd.isna(category_str) or category_str == "Unknown":
        return "Unknown"
    
    # Tomar la última parte de la jerarquía (más específica)
    parts = str(category_str).split("|")
    last_part = parts[-1] if parts else "Unknown"
    
    # Separar palabras pegadas con & o mayúsculas
    import re
    # Separar por &
    clean = last_part.replace("&", " & ")
    # Insertar espacio antes de mayúsculas (CamelCase)
    clean = re.sub(r'([a-z])([A-Z])', r'\1 \2', clean)
    
    return clean.strip()

def clean_dataset(df: pd.DataFrame):
    df = df.copy()

    numeric_cols = [
        "discounted_price",
        "actual_price",
        "discount_percentage",
        "rating",
        "rating_count",
    ]

    # Convertir a número
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.drop_duplicates()

    # Limpiar categorías: extraer la categoría legible
    df["category_display"] = df["category"].apply(extract_clean_category)
    
    # Mantener la categoría original para el encoding
    # pero usar la limpia como alternativa

    # Rellenar nulos
    df = df.fillna({
        "discounted_price": 0,
        "actual_price": 0,
        "discount_percentage": 0,
        "rating": df["rating"].median(),
        "rating_count": 0,
        "category": "Unknown",
        "category_display": "Unknown"
    })

    return df

def add_target(df: pd.DataFrame):
    df = df.copy()

    df["is_success"] = (
        (df["rating"] >= 4.0) &
        (df["rating_count"] >= 50)
    ).astype(int)

    return df

def prepare_features(df: pd.DataFrame):
    # Usar category_display en lugar de category cruda
    X = df[[
        "discounted_price",
        "actual_price",
        "discount_percentage",
        "rating",
        "rating_count",
        "category_display"
    ]].rename(columns={"category_display": "category"})

    y = df["is_success"]

    return X, y
