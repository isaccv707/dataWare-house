import pandas as pd

def load_dataset(path: str):
    return pd.read_csv(path)

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

    # Rellenar nulos
    df = df.fillna({
        "discounted_price": 0,
        "actual_price": 0,
        "discount_percentage": 0,
        "rating": df["rating"].median(),
        "rating_count": 0,
        "category": "Unknown"
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
    X = df[[
        "discounted_price",
        "actual_price",
        "discount_percentage",
        "rating",
        "rating_count",
        "category"
    ]]

    y = df["is_success"]

    return X, y
