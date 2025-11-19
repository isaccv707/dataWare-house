import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder

from preprocessing import load_dataset, clean_dataset, add_target, prepare_features

DATA_PATH = "data/amazon.csv"
MODEL_PATH = "models/modelo_random_forest.pkl"
ENCODER_PATH = "models/encoder_category.pkl"

def train_model():
    print("1) Cargando dataset...")
    df = load_dataset(DATA_PATH)

    print("2) Limpiando dataset...")
    df = clean_dataset(df)

    print("3) Creando variable objetivo (is_success)...")
    df = add_target(df)

    print("4) Codificando categorías...")
    encoder = LabelEncoder()
    df["category"] = encoder.fit_transform(df["category"])
    joblib.dump(encoder, ENCODER_PATH)
    print(f"Encoder guardado: {ENCODER_PATH}")

    print("5) Preparando X y y...")
    X, y = prepare_features(df)

    print("6) Train/Test split...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print("7) Entrenando modelo...")
    model = RandomForestClassifier(n_estimators=300, random_state=42)
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)

    print("\n🔍 Accuracy:", acc)
    print("\n📄 Reporte:\n", classification_report(y_test, preds))

    joblib.dump(model, MODEL_PATH)
    print(f"\n🎉 Modelo guardado en: {MODEL_PATH}")

if __name__ == "__main__":
    train_model()
