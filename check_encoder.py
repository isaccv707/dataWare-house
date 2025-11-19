import joblib

encoder = joblib.load("models/encoder_category.pkl")

print("Categorías en orden EXACTO:")
for i, c in enumerate(encoder.classes_):
    print(i, "→", c)
