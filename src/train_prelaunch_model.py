import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder

from preprocessing import load_dataset, clean_dataset, add_target, prepare_prelaunch_features

DATA_PATH = "data/amazon.csv"
MODEL_PATH = "models/modelo_prelaunch.pkl"
ENCODER_PATH = "models/encoder_prelaunch.pkl"

def train_model():
    print("1) Cargando dataset...")
    df = load_dataset(DATA_PATH)

    print("2) Limpiando dataset...")
    df = clean_dataset(df)

    print("3) Creando variable objetivo (is_success)...")
    df = add_target(df)

    print("4) Preparando features para modelo PRE-LAUNCH (sin ratings)...")
    X, y = prepare_prelaunch_features(df)
    
    print(f"   Features utilizadas: {list(X.columns)}")
    print(f"   Total de registros: {len(X)}")

    print("5) Train/Test split...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print("6) Creando pipeline con OneHotEncoder para categorías...")
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

    # Save the preprocessor
    joblib.dump(preprocessor, ENCODER_PATH)
    print(f"Preprocessor guardado: {ENCODER_PATH}")

    print("7) Entrenando modelo Random Forest PRE-LAUNCH...")
    print("   (Este modelo NO usa ratings - ideal para nuevos vendedores)")
    model = RandomForestClassifier(
        n_estimators=300, 
        max_depth=10,
        min_samples_split=15,
        random_state=42
    )
    model.fit(X_train_transformed, y_train)

    preds = model.predict(X_test_transformed)
    acc = accuracy_score(y_test, preds)

    print("\n" + "="*60)
    print("📊 RESULTADOS DEL MODELO PRE-LAUNCH")
    print("="*60)
    print(f"🎯 Accuracy: {acc:.4f}")
    print("\n📄 Reporte de Clasificación:")
    print(classification_report(y_test, preds))

    # Feature importance
    feature_names = (
        list(preprocessor.named_transformers_['cat'].get_feature_names_out(['category'])) +
        ['discounted_price', 'actual_price', 'discount_percentage']
    )
    importances = pd.DataFrame({
        'feature': feature_names,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print("\n🔍 Importancia de Features:")
    print(importances.to_string(index=False))

    joblib.dump(model, MODEL_PATH)
    print(f"\n🎉 Modelo PRE-LAUNCH guardado en: {MODEL_PATH}")
    print(f"💡 Este modelo puede predecir éxito basándose SOLO en precio y categoría")

if __name__ == "__main__":
    train_model()
