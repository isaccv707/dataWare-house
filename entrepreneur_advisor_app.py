"""
Amazon Entrepreneur Advisor - Streamlit UI
Interactive tool to predict product success on Amazon without reviews
"""

import streamlit as st
import pandas as pd
import numpy as np

# ================================
# CONFIGURACIÓN GENERAL DE STREAMLIT
# ================================
st.set_page_config(
    page_title="Asesor de Emprendedores | Amazon",
    page_icon="🚀",
    layout="wide",
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
    color: #FF9900;
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
.success-card {
    padding: 20px;
    border-radius: 12px;
    background-color: #d4edda;
    border: 2px solid #28a745;
    margin-top: 20px;
}
.warning-card {
    padding: 20px;
    border-radius: 12px;
    background-color: #fff3cd;
    border: 2px solid #ffc107;
    margin-top: 20px;
}
.danger-card {
    padding: 20px;
    border-radius: 12px;
    background-color: #f8d7da;
    border: 2px solid #dc3545;
    margin-top: 20px;
}
.metric-card {
    padding: 15px;
    border-radius: 8px;
    background-color: #ffffff;
    border: 1px solid #e0e0e0;
    margin: 10px 0;
}
.footer-text {
    text-align: center;
    font-size: 12px;
    color: #777;
    margin-top: 2rem;
}
.category-badge {
    display: inline-block;
    padding: 5px 10px;
    border-radius: 5px;
    background-color: #FF9900;
    color: white;
    font-weight: bold;
    margin: 5px;
}
</style>
""", unsafe_allow_html=True)

# ================================
# FUNCIONES DE CARGA DE DATOS
# ================================

@st.cache_data
def load_data():
    """Load and clean the Amazon dataset"""
    df = pd.read_csv('data/amazon.csv')
    
    # Clean numeric columns
    df['discounted_price'] = pd.to_numeric(
        df['discounted_price'].str.replace('$', '').str.replace(',', ''), 
        errors='coerce'
    )
    df['actual_price'] = pd.to_numeric(
        df['actual_price'].str.replace('$', '').str.replace(',', ''), 
        errors='coerce'
    )
    df['discount_percentage'] = pd.to_numeric(
        df['discount_percentage'].str.replace('%', ''), 
        errors='coerce'
    )
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
    df['rating_count'] = pd.to_numeric(
        df['rating_count'].str.replace(',', ''), 
        errors='coerce'
    ).fillna(0).astype(int)
    
    # Extract main category
    df['main_category'] = df['category'].str.split('|').str[0]
    
    # Define success
    df['is_successful'] = ((df['rating'] >= 4.0) & (df['rating_count'] >= 50)).astype(int)
    
    # Remove NaN values
    df = df.dropna(subset=['discounted_price', 'actual_price', 'discount_percentage'])
    
    return df

@st.cache_data
def get_category_stats(df):
    """Get category statistics"""
    category_stats = df.groupby('main_category').agg({
        'is_successful': 'mean',
        'product_id': 'count',
        'discounted_price': 'median',
        'discount_percentage': 'mean'
    }).round(2)
    
    category_stats.columns = ['Success_Rate', 'Product_Count', 'Median_Price', 'Avg_Discount']
    category_stats = category_stats[category_stats['Product_Count'] >= 2]
    category_stats = category_stats.sort_values('Success_Rate', ascending=False)
    
    return category_stats

def predict_success(category, price, discount_pct, df):
    """Predict success probability based on similar products"""
    
    # Filter for the category
    similar_products = df[df['main_category'] == category].copy()
    
    if len(similar_products) == 0:
        return None
    
    # Calculate similarity based on price and discount
    similar_products['price_diff'] = abs(similar_products['discounted_price'] - price)
    similar_products['discount_diff'] = abs(similar_products['discount_percentage'] - discount_pct)
    
    # Similarity score (closer = higher score)
    similar_products['similarity_score'] = (
        1 / (1 + similar_products['price_diff'] / max(price, 1)) * 0.6 +
        1 / (1 + similar_products['discount_diff'] / 10) * 0.4
    )
    
    # Get top 50 most similar products
    top_similar = similar_products.nlargest(min(50, len(similar_products)), 'similarity_score')
    
    # Calculate statistics
    success_rate = top_similar['is_successful'].mean()
    avg_rating = top_similar['rating'].mean()
    avg_reviews = top_similar['rating_count'].mean()
    
    # Competition analysis
    price_competitors = similar_products[
        (similar_products['discounted_price'] >= price * 0.8) &
        (similar_products['discounted_price'] <= price * 1.2)
    ]
    
    num_competitors = len(price_competitors)
    competitor_avg_rating = price_competitors['rating'].mean() if len(price_competitors) > 0 else 0
    
    results = {
        'success_rate': success_rate,
        'avg_rating': avg_rating,
        'avg_reviews': avg_reviews,
        'num_competitors': num_competitors,
        'competitor_avg_rating': competitor_avg_rating,
        'sample_size': len(top_similar)
    }
    
    return results

def get_verdict(success_rate):
    """Get recommendation based on success rate"""
    if success_rate >= 0.75:
        return "🟢 EXCELENTE", "Esta es una oportunidad muy prometedora! Productos similares tienen una tasa de éxito muy alta.", "success"
    elif success_rate >= 0.60:
        return "🟢 BUENO", "Fuerte oportunidad con buen potencial. Enfócate en calidad y servicio al cliente.", "success"
    elif success_rate >= 0.45:
        return "🟡 MODERADO", "Oportunidad decente pero competitiva. Necesitarás marketing fuerte y excelente calidad de producto.", "warning"
    elif success_rate >= 0.30:
        return "🟠 DESAFIANTE", "Segmento de mercado difícil. Considera ajustar tu precio o elegir una categoría diferente.", "warning"
    else:
        return "🔴 ALTO RIESGO", "Mercado muy desafiante. Recomendamos explorar otras categorías o ajustar significativamente tu estrategia.", "danger"

# ================================
# CARGAR DATOS
# ================================

try:
    df = load_data()
    category_stats = get_category_stats(df)
except Exception as e:
    st.error(f"Error al cargar los datos: {e}")
    st.stop()

# ================================
# SIDEBAR (INFO PROFESIONAL)
# ================================
st.sidebar.title("ℹ️ Sobre este asesor")
st.sidebar.write(f"""
Este asesor analiza **{len(df):,}** productos reales de Amazon para predecir 
el éxito de tu producto **sin necesidad de reseñas**.

**Definición de producto exitoso:**
- Rating ≥ 4.0  
- Número de reseñas ≥ 50  

**El análisis considera:**
- Categoría del producto
- Precio de venta
- Porcentaje de descuento
- Productos similares en el mercado
- Nivel de competencia
""")

st.sidebar.markdown("---")

st.sidebar.subheader("🏆 Top 5 Categorías")
for idx, (cat, row) in enumerate(category_stats.head(5).iterrows(), 1):
    st.sidebar.write(f"**{idx}. {cat}**")
    st.sidebar.progress(row['Success_Rate'])
    st.sidebar.caption(f"Tasa de éxito: {row['Success_Rate']*100:.1f}%")

st.sidebar.markdown("---")
st.sidebar.caption("💡 Herramienta para emprendedores • Basado en datos reales de Amazon")

# ================================
# ENCABEZADO PRINCIPAL
# ================================
st.markdown('<p class="big-title">🚀 Asesor de Emprendedores Amazon</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Predice el éxito de tu producto sin necesidad de reseñas • Basado en precio y categoría</p>', unsafe_allow_html=True)

st.write("---")

# ================================
# MÉTRICAS GENERALES
# ================================
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Productos Analizados", f"{len(df):,}")

with col2:
    overall_success = df['is_successful'].mean()
    st.metric("Tasa de Éxito General", f"{overall_success*100:.1f}%")

with col3:
    median_price = df['discounted_price'].median()
    st.metric("Precio Medio", f"${median_price:,.0f}")

with col4:
    avg_discount = df['discount_percentage'].mean()
    st.metric("Descuento Promedio", f"{avg_discount:.1f}%")

st.write("---")

# ================================
# FORMULARIO DE ENTRADA (PRO)
# ================================
st.subheader("📝 Ingresa los datos de tu producto")
st.write("Como emprendedor sin reseñas, analiza tu producto basado en categoría y precio")

with st.form("prediction_form"):
    col1, col2 = st.columns(2)

    with col1:
        # Category selection
        category = st.selectbox(
            "📂 Categoría del producto",
            options=category_stats.index.tolist(),
            help="Selecciona la categoría principal de tu producto"
        )
        
        # Show category stats
        if category:
            cat_stats = category_stats.loc[category]
            st.info(f"""
            **Estadísticas de la categoría:**
            - Tasa de éxito: {cat_stats['Success_Rate']*100:.1f}%
            - Precio medio: ${cat_stats['Median_Price']:,.0f}
            - Descuento promedio: {cat_stats['Avg_Discount']:.1f}%
            """)

    with col2:
        # Price input
        price = st.number_input(
            "💰 Precio de venta ($)",
            min_value=10.0,
            max_value=100000.0,
            value=299.0,
            step=10.0,
            help="El precio al que venderás tu producto"
        )
        
        # Discount input
        discount_pct = st.slider(
            "🏷️ Porcentaje de descuento (%)",
            min_value=0,
            max_value=90,
            value=50,
            step=5,
            help="Descuento que ofrecerás. Recomendado: 40-60%"
        )
        
        # Calculate original price
        if discount_pct > 0:
            original_price = price / (1 - discount_pct/100)
            st.markdown(f"**💵 Precio original calculado:** ${original_price:,.0f}")

    submitted = st.form_submit_button("🔍 Analizar Probabilidad de Éxito", use_container_width=True)

# ================================
# PREDICCIÓN Y RESULTADOS
# ================================
# Initialize session state to store results
if 'results' not in st.session_state:
    st.session_state.results = None
    st.session_state.category = None
    st.session_state.price = None
    st.session_state.discount_pct = None

# Add clear button if results exist
if st.session_state.results is not None:
    col1, col2, col3 = st.columns([1, 1, 3])
    with col1:
        if st.button("🔄 Nuevo Análisis", use_container_width=True):
            st.session_state.results = None
            st.session_state.category = None
            st.session_state.price = None
            st.session_state.discount_pct = None
            st.rerun()

if submitted:
    with st.spinner("Analizando productos similares en el mercado..."):
        results = predict_success(category, price, discount_pct, df)
        
        # Store results in session state
        st.session_state.results = results
        st.session_state.category = category
        st.session_state.price = price
        st.session_state.discount_pct = discount_pct
        
        if results is None:
            st.error("❌ No se encontraron datos suficientes para esta categoría")

# Display results if they exist in session state
if st.session_state.results is not None:
    results = st.session_state.results
    category = st.session_state.category
    price = st.session_state.price
    discount_pct = st.session_state.discount_pct
    
    if True:  # This replaces the 'else' from the original if statement
            # Get verdict
            verdict, explanation, card_type = get_verdict(results['success_rate'])
            
            # Display main result
            st.write("---")
            st.subheader("📊 Resultado del Análisis")
            
            # Result card
            if card_type == "success":
                st.markdown('<div class="success-card">', unsafe_allow_html=True)
            elif card_type == "warning":
                st.markdown('<div class="warning-card">', unsafe_allow_html=True)
            else:
                st.markdown('<div class="danger-card">', unsafe_allow_html=True)
            
            st.markdown(f"### {verdict}")
            st.write(explanation)
            
            # Progress bar for success rate
            st.write("**Probabilidad de Éxito:**")
            st.progress(results['success_rate'])
            st.markdown(f"### {results['success_rate']*100:.1f}%")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Detailed metrics
            st.write("---")
            st.subheader("📈 Análisis Detallado")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                st.metric(
                    "Rating Esperado",
                    f"{results['avg_rating']:.2f}/5.0",
                    help="Rating promedio de productos similares"
                )
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                st.metric(
                    "Reseñas Esperadas",
                    f"{results['avg_reviews']:,.0f}",
                    help="Número promedio de reseñas de productos similares"
                )
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col3:
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                st.metric(
                    "Competidores Directos",
                    f"{results['num_competitors']}",
                    help="Productos con precio similar (±20%)"
                )
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Competition analysis
            st.write("---")
            st.subheader("🏪 Análisis de Competencia")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Tu Perfil de Producto:**")
                st.info(f"""
                - **Categoría:** {category}
                - **Precio de venta:** ${price:,.0f}
                - **Descuento:** {discount_pct}%
                - **Precio original:** ${price/(1-discount_pct/100):,.0f}
                """)
            
            with col2:
                st.write("**Competencia en tu Rango de Precio:**")
                if results['num_competitors'] > 0:
                    st.warning(f"""
                    - **Número de competidores:** {results['num_competitors']}
                    - **Rating promedio competidores:** {results['competitor_avg_rating']:.2f}/5.0
                    - **Análisis basado en:** {results['sample_size']} productos similares
                    """)
                else:
                    st.success("¡Poca competencia directa en este rango de precio!")
            
            # Recommendations
            st.write("---")
            st.subheader("💡 Recomendaciones Personalizadas")
            
            if results['success_rate'] >= 0.6:
                st.success("""
                **✅ Este producto tiene buen potencial. Enfócate en:**
                - Asegurar excelente calidad del producto
                - Ofrecer precio competitivo o mejor
                - Proporcionar servicio al cliente excepcional
                - Solicitar reseñas de los primeros clientes
                - Mantener inventario disponible
                """)
            else:
                st.warning("""
                **⚠️ Considera estas mejoras antes de lanzar:**
                """)
                
                recommendations = []
                if discount_pct < 40:
                    recommendations.append("- 🏷️ Aumenta tu descuento (objetivo: 40-60%)")
                if price > 2000:
                    recommendations.append("- 💰 Considera un punto de precio más bajo inicialmente")
                if results['num_competitors'] > 100:
                    recommendations.append("- 🎯 Esta categoría es muy competitiva - diferencia tu producto")
                if results['success_rate'] < 0.4:
                    recommendations.append("- 📂 Explora una categoría diferente con mayores tasas de éxito")
                
                if recommendations:
                    for rec in recommendations:
                        st.write(rec)
                else:
                    st.write("- 🔍 Investiga más sobre tu mercado objetivo")
                    st.write("- 💡 Considera un enfoque de nicho único")
            
            # Profit calculator
            st.write("---")
            st.subheader("💵 Calculadora de Ganancias Estimadas")
            
            with st.expander("📊 Ver proyección de ganancias", expanded=True):
                st.write("**Paso 1: Costos del Producto**")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    cost_per_unit = st.number_input(
                        "Costo de fabricación/compra ($)", 
                        min_value=1.0, 
                        value=float(price*0.35), 
                        step=10.0,
                        help="Costo de producción o compra del producto"
                    )
                
                with col2:
                    # Amazon fees vary by category
                    category_fees = {
                        'Electronics': 8,
                        'Computers&Accessories': 8,
                        'Home&Kitchen': 15,
                        'OfficeProducts': 15
                    }
                    default_fee = category_fees.get(category, 15)
                    
                    amazon_fee_pct = st.number_input(
                        "Comisión Amazon (%)", 
                        min_value=6.0, 
                        max_value=45.0, 
                        value=float(default_fee),
                        step=0.5,
                        help=f"Comisión típica para {category}: {default_fee}%"
                    )
                
                with col3:
                    shipping_cost = st.number_input(
                        "Costo de envío/logística ($)", 
                        min_value=0.0, 
                        value=20.0, 
                        step=5.0,
                        help="Incluye empaque, envío a Amazon, etc."
                    )
                
                st.write("---")
                st.write("**Paso 2: Costos Adicionales (Opcional)**")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    marketing_cost_per_unit = st.number_input(
                        "Marketing por unidad ($)", 
                        min_value=0.0, 
                        value=15.0, 
                        step=5.0,
                        help="PPC, anuncios, promociones por producto"
                    )
                
                with col2:
                    storage_fee = st.number_input(
                        "Tarifa de almacenamiento ($)", 
                        min_value=0.0, 
                        value=5.0, 
                        step=1.0,
                        help="Costo mensual de almacenamiento FBA"
                    )
                
                with col3:
                    other_costs = st.number_input(
                        "Otros costos ($)", 
                        min_value=0.0, 
                        value=5.0, 
                        step=5.0,
                        help="Empaque premium, etiquetas, etc."
                    )
                
                st.write("---")
                st.write("**Paso 3: Análisis de Rentabilidad**")
                
                # Calculate all costs
                amazon_fee = price * (amazon_fee_pct / 100)
                total_costs = cost_per_unit + amazon_fee + shipping_cost + marketing_cost_per_unit + storage_fee + other_costs
                profit_per_unit = price - total_costs
                margin_pct = (profit_per_unit / price) * 100 if price > 0 else 0
                
                # Cost breakdown visualization
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.write("**Desglose de Costos por Unidad:**")
                    
                    # Create cost breakdown data
                    costs_data = {
                        'Concepto': ['Precio de Venta', 'Costo Producto', 'Comisión Amazon', 
                                   'Envío/Logística', 'Marketing', 'Almacenamiento', 'Otros'],
                        'Monto ($)': [price, -cost_per_unit, -amazon_fee, -shipping_cost, 
                                     -marketing_cost_per_unit, -storage_fee, -other_costs],
                        'Porcentaje (%)': [
                            100,
                            -(cost_per_unit/price*100) if price > 0 else 0,
                            -(amazon_fee/price*100) if price > 0 else 0,
                            -(shipping_cost/price*100) if price > 0 else 0,
                            -(marketing_cost_per_unit/price*100) if price > 0 else 0,
                            -(storage_fee/price*100) if price > 0 else 0,
                            -(other_costs/price*100) if price > 0 else 0
                        ]
                    }
                    
                    costs_df = pd.DataFrame(costs_data)
                    
                    # Display with color coding
                    for idx, row in costs_df.iterrows():
                        if idx == 0:
                            st.success(f"💰 {row['Concepto']}: **${row['Monto ($)']:,.2f}** ({row['Porcentaje (%)']:.1f}%)")
                        elif row['Monto ($)'] < 0:
                            st.error(f"➖ {row['Concepto']}: **${abs(row['Monto ($)']):,.2f}** ({abs(row['Porcentaje (%)']):.1f}%)")
                    
                    # Profit line
                    if profit_per_unit > 0:
                        st.success(f"✅ **Ganancia Neta: ${profit_per_unit:.2f}** ({margin_pct:.1f}%)")
                    else:
                        st.error(f"❌ **Pérdida: ${profit_per_unit:.2f}** ({margin_pct:.1f}%)")
                
                with col2:
                    st.write("**Métricas Clave:**")
                    
                    # Profit metrics
                    if profit_per_unit > 0:
                        st.metric("💰 Ganancia/Unidad", f"${profit_per_unit:.2f}")
                        st.metric("📊 Margen", f"{margin_pct:.1f}%")
                        
                        # ROI
                        roi = (profit_per_unit / total_costs * 100) if total_costs > 0 else 0
                        st.metric("📈 ROI", f"{roi:.1f}%")
                        
                        # Break-even
                        break_even = total_costs / profit_per_unit if profit_per_unit > 0 else float('inf')
                        if break_even < 1000:
                            st.metric("⚖️ Punto de equilibrio", f"{break_even:.0f} unidades")
                    else:
                        st.error("⚠️ **Producto no rentable**")
                        st.write(f"Pérdida: ${abs(profit_per_unit):.2f}/unidad")
                        adjustment_needed = abs(profit_per_unit)
                        st.write(f"Necesitas reducir costos o aumentar precio en ${adjustment_needed:.2f}")
                
                # Monthly and annual projections
                if profit_per_unit > 0:
                    st.write("---")
                    st.write("**Proyecciones de Ventas:**")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    # Estimate sales based on success rate
                    if results['success_rate'] >= 0.75:
                        monthly_units_low = 60
                        monthly_units_mid = 100
                        monthly_units_high = 150
                        scenario = "Optimista"
                    elif results['success_rate'] >= 0.60:
                        monthly_units_low = 40
                        monthly_units_mid = 70
                        monthly_units_high = 100
                        scenario = "Bueno"
                    elif results['success_rate'] >= 0.45:
                        monthly_units_low = 20
                        monthly_units_mid = 40
                        monthly_units_high = 60
                        scenario = "Moderado"
                    elif results['success_rate'] >= 0.30:
                        monthly_units_low = 10
                        monthly_units_mid = 20
                        monthly_units_high = 35
                        scenario = "Conservador"
                    else:
                        monthly_units_low = 5
                        monthly_units_mid = 10
                        monthly_units_high = 20
                        scenario = "Muy Conservador"
                    
                    with col1:
                        st.info(f"""
                        **Escenario Bajo**
                        - Ventas/mes: {monthly_units_low}
                        - Ganancia/mes: ${profit_per_unit * monthly_units_low:,.2f}
                        - Ganancia/año: ${profit_per_unit * monthly_units_low * 12:,.2f}
                        """)
                    
                    with col2:
                        st.success(f"""
                        **Escenario Medio** ({scenario})
                        - Ventas/mes: {monthly_units_mid}
                        - Ganancia/mes: ${profit_per_unit * monthly_units_mid:,.2f}
                        - Ganancia/año: ${profit_per_unit * monthly_units_mid * 12:,.2f}
                        """)
                    
                    with col3:
                        st.info(f"""
                        **Escenario Alto**
                        - Ventas/mes: {monthly_units_high}
                        - Ganancia/mes: ${profit_per_unit * monthly_units_high:,.2f}
                        - Ganancia/año: ${profit_per_unit * monthly_units_high * 12:,.2f}
                        """)
                    
                    # Investment analysis
                    st.write("---")
                    st.write("**Análisis de Inversión Inicial:**")
                    
                    initial_units = st.slider(
                        "Unidades en primer pedido:", 
                        min_value=50, 
                        max_value=1000, 
                        value=200, 
                        step=50
                    )
                    
                    initial_investment = (cost_per_unit + shipping_cost + other_costs) * initial_units
                    setup_costs = st.number_input(
                        "Costos de setup (diseño, registro, muestras) ($):", 
                        min_value=0.0, 
                        value=500.0, 
                        step=100.0
                    )
                    total_investment = initial_investment + setup_costs
                    
                    # Time to recover investment
                    monthly_profit_mid = profit_per_unit * monthly_units_mid
                    months_to_recover = total_investment / monthly_profit_mid if monthly_profit_mid > 0 else float('inf')
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("💼 Inversión Inicial", f"${total_investment:,.2f}")
                    
                    with col2:
                        st.metric("📅 Recuperación (meses)", f"{months_to_recover:.1f}" if months_to_recover < 100 else "N/A")
                    
                    with col3:
                        annual_roi = (monthly_profit_mid * 12 / total_investment * 100) if total_investment > 0 else 0
                        st.metric("💹 ROI Anual Esperado", f"{annual_roi:.0f}%")
                    
                    # Recommendations
                    st.write("---")
                    st.write("**💡 Recomendaciones Financieras:**")
                    
                    if margin_pct >= 30:
                        st.success("✅ Excelente margen de ganancia. Este producto es financieramente atractivo.")
                    elif margin_pct >= 20:
                        st.success("✅ Buen margen de ganancia. El producto es viable.")
                    elif margin_pct >= 15:
                        st.warning("⚠️ Margen aceptable pero ajustado. Considera optimizar costos.")
                    else:
                        st.error("❌ Margen muy bajo. Riesgoso para un emprendedor nuevo.")
                    
                    if months_to_recover <= 3:
                        st.success("✅ Recuperación rápida de inversión (≤3 meses)")
                    elif months_to_recover <= 6:
                        st.info("ℹ️ Recuperación moderada de inversión (3-6 meses)")
                    elif months_to_recover <= 12:
                        st.warning("⚠️ Recuperación lenta de inversión (6-12 meses)")
                    else:
                        st.error("❌ Recuperación muy lenta. Considera revisar el modelo de negocio.")
                
                else:
                    st.error("""
                    ⚠️ **Este producto no es rentable con los costos actuales.**
                    
                    Opciones para mejorar:
                    - Reducir costos de producción
                    - Negociar mejores precios con proveedores
                    - Aumentar el precio de venta
                    - Reducir costos de marketing
                    - Optimizar logística
                    """)

# ================================
# INFORMACIÓN ADICIONAL
# ================================
st.write("---")
st.subheader("📚 Recursos Adicionales")

col1, col2 = st.columns(2)

with col1:
    st.info("""
    **📖 Guías Disponibles:**
    - `QUICK_GUIDE.md` - Guía rápida de decisión
    - `ENTREPRENEUR_GUIDE.md` - Guía completa paso a paso
    """)

with col2:
    st.info("""
    **🔧 Herramientas:**
    - `market_analysis_report.py` - Análisis completo del mercado
    - `entrepreneur_advisor.py` - Versión de consola
    """)

# ================================
# FOOTER
# ================================
st.markdown('<p class="footer-text">🚀 Desarrollado para emprendedores • Basado en datos reales de Amazon • Actualizado 2025</p>', unsafe_allow_html=True)
