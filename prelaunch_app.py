import streamlit as st
import joblib
import pandas as pd

# ================================
# CONFIGURACIÓN GENERAL DE STREAMLIT
# ================================
st.set_page_config(
    page_title="Predicción Pre-Lanzamiento | Amazon ML",
    page_icon="🚀",
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
    color: #0ea5e9;
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
.info-box {
    padding: 15px;
    border-radius: 8px;
    background-color: #e0f2fe;
    border-left: 4px solid #0ea5e9;
    margin: 20px 0;
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
MODEL_PATH = "models/modelo_prelaunch.pkl"
ENCODER_PATH = "models/encoder_prelaunch.pkl"

model = joblib.load(MODEL_PATH)
preprocessor = joblib.load(ENCODER_PATH)

# ================================
# SIDEBAR (INFO PROFESIONAL)
# ================================
st.sidebar.title("ℹ️ Sobre este modelo")
st.sidebar.write(
    """
### 🚀 Modelo Pre-Lanzamiento

**Perfecto para nuevos vendedores que:**
- Aún no tienen reseñas
- Están planeando un nuevo producto
- Quieren validar su estrategia de precio

**Features utilizadas:**
- ✅ Precio original  
- ✅ Precio con descuento  
- ✅ % de descuento  
- ✅ Categoría del producto  
- ❌ NO requiere ratings

**Definición de éxito:**
Basado en productos similares que lograron:
- Rating ≥ 4.0  
- Reseñas ≥ 50  
"""
)

st.sidebar.markdown("---")
st.sidebar.caption("🎓 Proyecto académico • ML para nuevos vendedores")

# ================================
# ENCABEZADO PRINCIPAL
# ================================
st.markdown('<p class="big-title">🚀 Predicción Pre-Lanzamiento</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Para nuevos vendedores SIN reseñas aún</p>', unsafe_allow_html=True)

st.markdown('<div class="info-box">💡 <b>Este modelo predice el potencial de éxito basándose SOLO en tu estrategia de precio y categoría</b></div>', unsafe_allow_html=True)

st.write("---")

# ================================
# FORMULARIO DE ENTRADA
# ================================
with st.form("prelaunch_form"):
    st.subheader("📝 Configura tu estrategia de precio")

    col1, col2 = st.columns(2)

    with col1:
        actual_price = st.number_input("💰 Precio original (₹)", min_value=1.0, value=2000.0, help="El precio antes del descuento")

    with col2:
        discounted_price = st.number_input("🏷️ Precio de venta (₹)", min_value=0.0, value=1500.0, help="El precio final para el cliente")

    # Cálculo del % de descuento
    if actual_price > 0:
        discount_percentage = ((actual_price - discounted_price) / actual_price) * 100
    else:
        discount_percentage = 0.0

    # Visual del descuento
    col_disc1, col_disc2, col_disc3 = st.columns([1, 2, 1])
    with col_disc2:
        st.metric(
            label="🔻 Descuento Calculado", 
            value=f"{discount_percentage:.1f}%",
            help="Descuento atractivo: 30-60%"
        )

    # Get unique categories
    cat_encoder = preprocessor.named_transformers_['cat']
    categories = cat_encoder.categories_[0].tolist()
    
    category = st.selectbox(
        "📂 Categoría del producto", 
        categories,
        help="Selecciona la categoría que mejor describe tu producto"
    )

    submitted = st.form_submit_button("🔍 Predecir Potencial de Éxito")

# ================================
# PREDICCIÓN
# ================================
if submitted:
    # Construir el DataFrame
    X = pd.DataFrame([{
        "discounted_price": discounted_price,
        "actual_price": actual_price,
        "discount_percentage": discount_percentage,
        "category": category
    }])

    # Apply the preprocessor transformation
    X_transformed = preprocessor.transform(X)

    pred = model.predict(X_transformed)[0]
    prob = float(model.predict_proba(X_transformed)[0][1])

    # Tarjeta de resultado
    st.markdown('<div class="result-card">', unsafe_allow_html=True)

    if pred == 1:
        st.success(f"🎉 **¡Alto Potencial de Éxito!**")
        st.write(f"Confianza del modelo: **{prob:.1%}**")
        st.write("✅ Tu estrategia de precio es prometedora para esta categoría")
    else:
        st.warning(f"⚠️ **Potencial Moderado**")
        st.write(f"Confianza del modelo: **{prob:.1%}**")
        st.write("💡 Considera ajustar el precio o revisar la categoría")

    st.progress(prob)
    
    st.markdown('</div>', unsafe_allow_html=True)

    # Recomendaciones
    st.write("---")
    st.subheader("💡 Recomendaciones")
    
    col_rec1, col_rec2 = st.columns(2)
    
    with col_rec1:
        if discount_percentage < 20:
            st.info("📉 Descuento bajo. Considera ofertas de 30-60%")
        elif discount_percentage > 70:
            st.warning("📈 Descuento muy alto. ¿Es sostenible?")
        else:
            st.success("✅ Descuento atractivo (30-60%)")
    
    with col_rec2:
        if discounted_price < 500:
            st.info("💵 Producto económico - bueno para volumen")
        elif discounted_price > 5000:
            st.info("💎 Producto premium - enfócate en calidad")
        else:
            st.success("✅ Rango de precio competitivo")

# ================================
# FOOTER
# ================================
st.markdown('<p class="footer-text">🚀 Modelo Pre-Lanzamiento • Ideal para nuevos vendedores sin historial de reseñas</p>', unsafe_allow_html=True)
