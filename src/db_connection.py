# src/db_connection.py
import psycopg2

DB_HOST = "localhost"
DB_PORT = 5432            # IMPORTANTE: el puerto del docker-compose ("5433:5432")
DB_NAME = "dw_amazon"
DB_USER = "postgres"
DB_PASSWORD = "postgres123"  # la que pusimos en docker-compose.yml

def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )

if __name__ == "__main__":
    # Prueba rápida de conexión
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT current_database(), current_schema();")
        row = cur.fetchone()
        print("Conectado a:", row)
        cur.close()
        conn.close()
    except Exception as e:
        print("Error al conectar:", e)
