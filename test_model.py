import joblib
import pandas as pd

# Load model and preprocessor
preprocessor = joblib.load('models/encoder_category.pkl')
model = joblib.load('models/modelo_random_forest.pkl')

print('✅ Available categories:')
cats = preprocessor.named_transformers_['cat'].categories_[0].tolist()
for i, cat in enumerate(cats, 1):
    print(f'  {i}. {cat}')

print(f'\n📊 Total categories: {len(cats)}')

# Test prediction
X = pd.DataFrame([{
    'discounted_price': 999,
    'actual_price': 1999,
    'discount_percentage': 50,
    'rating': 4.2,
    'rating_count': 100,
    'category': 'Home&Kitchen'
}])

X_transformed = preprocessor.transform(X)
pred = model.predict(X_transformed)
prob = model.predict_proba(X_transformed)[0][1]

print(f'\n✅ Test Prediction: {"SUCCESS" if pred[0]==1 else "NOT SUCCESS"}')
print(f'📈 Confidence: {prob:.1%}')
