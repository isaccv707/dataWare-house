# src/etl_load_dw.py
import pandas as pd
from db_connection import get_connection

DATA_PATH = "data/amazon.csv"

def load_raw_dataset(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)

    # Nos aseguramos de que las columnas clave existan
    expected_cols = [
        "product_id", "product_name", "category",
        "discounted_price", "actual_price", "discount_percentage",
        "rating", "rating_count", "about_product",
        "user_id", "user_name",
        "review_id", "review_title", "review_content",
        "img_link", "product_link",
    ]
    missing = [c for c in expected_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Faltan columnas en el CSV: {missing}")

    return df


def clean_for_dw(df: pd.DataFrame) -> pd.DataFrame:
    """Convierte tipos básicos y elimina duplicados por product_id."""
    df = df.copy()

    # Conversión de numéricos (maneja strings, NaN, etc.)
    numeric_cols = [
        "discounted_price",
        "actual_price",
        "discount_percentage",
        "rating",
        "rating_count",
    ]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Rellenos básicos
    df["discounted_price"] = df["discounted_price"].fillna(0)
    df["actual_price"] = df["actual_price"].fillna(0)
    df["discount_percentage"] = df["discount_percentage"].fillna(0)
    df["rating"] = df["rating"].fillna(df["rating"].median())
    df["rating_count"] = df["rating_count"].fillna(0)

    df["category"] = df["category"].fillna("Unknown")

    # Nos quedamos con un registro por product_id (si hubiera duplicados)
    df = df.drop_duplicates(subset=["product_id"])

    # Creamos is_success como en el modelo
    df["is_success"] = (
        (df["rating"] >= 4.0) & (df["rating_count"] >= 50)
    ).astype(int)

    return df


def insert_dim_category(df: pd.DataFrame, conn) -> dict:
    """Inserta categorías únicas en dim_category y devuelve un mapa full_category -> category_key."""
    cur = conn.cursor()

    categories = df["category"].dropna().unique()

    # Preparamos los valores con niveles de jerarquía
    records = []
    for cat in categories:
        parts = str(cat).split("|")
        main_category = parts[0] if len(parts) > 0 else None
        sub1 = parts[1] if len(parts) > 1 else None
        sub2 = parts[2] if len(parts) > 2 else None
        sub3 = parts[3] if len(parts) > 3 else None
        sub4 = parts[4] if len(parts) > 4 else None

        records.append(
            (cat, main_category, sub1, sub2, sub3, sub4)
        )

    # Insertar
    cur.executemany(
        """
        INSERT INTO dw_amazon.dim_category (
            full_category, main_category, sub_category_1, sub_category_2, sub_category_3, sub_category_4
        )
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        records,
    )

    conn.commit()

    # Crear diccionario full_category -> category_key
    cur.execute("SELECT category_key, full_category FROM dw_amazon.dim_category")
    rows = cur.fetchall()
    cat_map = {full: key for key, full in rows}

    cur.close()
    return cat_map


def insert_dim_product(df: pd.DataFrame, conn) -> dict:
    """Inserta productos únicos en dim_product y devuelve product_id -> product_key."""
    cur = conn.cursor()

    products = df[[
        "product_id", "product_name", "about_product", "img_link", "product_link"
    ]].drop_duplicates(subset=["product_id"])

    records = [
        (
            row["product_id"],
            row["product_name"],
            row["about_product"],
            row["img_link"],
            row["product_link"],
        )
        for _, row in products.iterrows()
    ]

    cur.executemany(
        """
        INSERT INTO dw_amazon.dim_product (
            product_id, product_name, about_product, img_link, product_link
        )
        VALUES (%s, %s, %s, %s, %s)
        """,
        records,
    )

    conn.commit()

    # Crear diccionario product_id -> product_key
    cur.execute("SELECT product_key, product_id FROM dw_amazon.dim_product")
    rows = cur.fetchall()
    prod_map = {pid: key for key, pid in rows}

    cur.close()
    return prod_map


def insert_fact_product_performance(df: pd.DataFrame, conn, prod_map: dict, cat_map: dict):
    """Inserta los hechos en fact_product_performance."""
    cur = conn.cursor()

    records = []
    for _, row in df.iterrows():
        pid = row["product_id"]
        cat = row["category"]

        product_key = prod_map.get(pid)
        category_key = cat_map.get(cat)

        # Si por alguna razón falta clave, saltamos el registro
        if product_key is None or category_key is None:
            continue

        records.append(
            (
                product_key,
                category_key,
                float(row["discounted_price"]),
                float(row["actual_price"]),
                float(row["discount_percentage"]),
                float(row["rating"]),
                int(row["rating_count"]),
                int(row["is_success"]),
            )
        )

    cur.executemany(
        """
        INSERT INTO dw_amazon.fact_product_performance (
            product_key, category_key,
            discounted_price, actual_price, discount_percentage,
            rating, rating_count, is_success
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """,
        records,
    )

    conn.commit()
    cur.close()


def main():
    print("Leyendo dataset bruto...")
    df_raw = load_raw_dataset(DATA_PATH)

    print("Limpiando dataset para DW...")
    df_clean = clean_for_dw(df_raw)

    conn = get_connection()

    try:
        print("Cargando dimensión de categorías...")
        cat_map = insert_dim_category(df_clean, conn)
        print(f"Categorías cargadas: {len(cat_map)}")

        print("Cargando dimensión de productos...")
        prod_map = insert_dim_product(df_clean, conn)
        print(f"Productos cargados: {len(prod_map)}")

        print("Cargando tabla de hechos...")
        insert_fact_product_performance(df_clean, conn, prod_map, cat_map)
        print("Carga de fact_product_performance completada.")

    finally:
        conn.close()
        print("Conexión cerrada.")


if __name__ == "__main__":
    main()
