import streamlit as st
import joblib
import pandas as pd

# ================================
# CONFIGURACIÓN GENERAL DE STREAMLIT
# ================================
st.set_page_config(
    page_title="Predicción de Éxito | Amazon ML",
    page_icon="📦",
    layout="centered",
)

# ================================
# CSS PERSONALIZADO
# ================================
st.markdown("""
<style>
.big-title {
    text-align: center;
    font-size: 36px !important;
    font-weight: 700 !important;
    color: #16a34a;
    margin-bottom: 0.2rem;
}
.subtitle {
    text-align: center;
    font-size: 16px;
    color: #555;
    margin-top: 0;
}
.result-card {
    padding: 20px;
    border-radius: 12px;
    background-color: #f7f7f7;
    text-align: center;
    margin-top: 20px;
    border: 1px solid #e0e0e0;
}
.footer-text {
    text-align: center;
    font-size: 12px;
    color: #777;
    margin-top: 2rem;
}
</style>
""", unsafe_allow_html=True)

# ================================
# Cargar modelo y preprocessor
# ================================
MODEL_PATH = "models/modelo_random_forest.pkl"
ENCODER_PATH = "models/encoder_category.pkl"

model = joblib.load(MODEL_PATH)
preprocessor = joblib.load(ENCODER_PATH)

# ================================
# SIDEBAR (INFO PROFESIONAL)
# ================================
st.sidebar.title("ℹ️ Sobre el modelo")
st.sidebar.write(
    """
Este modelo fue entrenado con datos reales de productos de Amazon.

**Definición de producto exitoso:**
- Rating ≥ 4.0  
- Número de reseñas ≥ 50  

El modelo utiliza un **Random Forest** con 300 árboles y considera:

- Precio original  
- Precio con descuento  
- % de descuento  
- Rating  
- Número de reseñas  
- Categoría codificada  
"""
)

st.sidebar.markdown("---")
st.sidebar.caption("Proyecto académico de Machine Learning • Predicción de éxito de productos")

# ================================
# ENCABEZADO PRINCIPAL
# ================================
st.markdown('<p class="big-title">📦 Predicción de Éxito de Productos</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Modelo de Machine Learning entrenado desde cero con datos de Amazon</p>', unsafe_allow_html=True)

st.write("---")

# ================================
# FORMULARIO DE ENTRADA (PRO)
# ================================
with st.form("prediction_form"):
    st.subheader("📝 Ingresa los datos del producto")

    col1, col2 = st.columns(2)

    with col1:
        actual_price = st.number_input("💰 Precio original", min_value=1.0, value=2000.0)
        rating = st.number_input("⭐ Rating (1–5)", min_value=1.0, max_value=5.0, step=0.1, value=4.5)

    with col2:
        discounted_price = st.number_input("🏷️ Precio con descuento", min_value=0.0, value=1200.0)
        rating_count = st.number_input("🧾 Número de reseñas", min_value=0, value=150)

    # Cálculo del % de descuento
    if actual_price > 0:
        discount_percentage = ((actual_price - discounted_price) / actual_price) * 100
    else:
        discount_percentage = 0.0

    st.markdown(f"**🔻 Descuento calculado automáticamente:** `{discount_percentage:.2f}%`")

    # Get unique categories from the preprocessor's one-hot encoder
    cat_encoder = preprocessor.named_transformers_['cat']
    categories = cat_encoder.categories_[0].tolist()
    
    category = st.selectbox("📂 Categoría del producto", categories)

    submitted = st.form_submit_button("🔍 Predecir éxito del producto")

# ================================
# PREDICCIÓN
# ================================
if submitted:
    # Construir el DataFrame con las mismas features del entrenamiento (sin codificar)
    X = pd.DataFrame([{
        "discounted_price": discounted_price,
        "actual_price": actual_price,
        "discount_percentage": discount_percentage,
        "rating": rating,
        "rating_count": rating_count,
        "category": category
    }])

    # Apply the preprocessor transformation (one-hot encoding for category)
    X_transformed = preprocessor.transform(X)

    pred = model.predict(X_transformed)[0]
    prob = float(model.predict_proba(X_transformed)[0][1])

    # Tarjeta de resultado
    st.markdown('<div class="result-card">', unsafe_allow_html=True)

    if pred == 1:
        st.success(f"🎉 **¡Producto Exitoso!**\nProbabilidad estimada: **{prob:.2f}**")
    else:
        st.error(f"❌ **Producto NO exitoso**\nProbabilidad estimada: **{prob:.2f}**")

    st.write("### 🔬 Probabilidad de éxito")
    st.progress(prob)

    st.markdown('</div>', unsafe_allow_html=True)

# ================================
# FOOTER
# ================================
st.markdown('<p class="footer-text">Desarrollado como proyecto académico de Machine Learning • Streamlit + Random Forest</p>', unsafe_allow_html=True)
