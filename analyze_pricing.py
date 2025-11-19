"""
Análisis de Estrategias de Precio para Nuevos Productos
Ayuda a entender qué combinaciones de precio/categoría funcionan mejor
"""

import pandas as pd
import sys
sys.path.insert(0, 'src')

from preprocessing import load_dataset, clean_dataset, add_target

def analyze_pricing_strategies():
    print("="*70)
    print("📊 ANÁLISIS DE ESTRATEGIAS DE PRECIO POR CATEGORÍA")
    print("="*70)
    
    # Cargar datos
    df = load_dataset("data/amazon.csv")
    df = clean_dataset(df)
    df = add_target(df)
    
    # Filtrar solo productos exitosos
    successful = df[df['is_success'] == 1].copy()
    failed = df[df['is_success'] == 0].copy()
    
    print(f"\n✅ Productos exitosos: {len(successful)}")
    print(f"❌ Productos no exitosos: {len(failed)}")
    print(f"📊 Tasa de éxito general: {len(successful)/len(df)*100:.1f}%")
    
    # Análisis por categoría
    print("\n" + "="*70)
    print("📂 ANÁLISIS POR CATEGORÍA")
    print("="*70)
    
    for category in sorted(df['category'].unique()):
        cat_data = df[df['category'] == category]
        cat_success = cat_data[cat_data['is_success'] == 1]
        
        if len(cat_data) < 10:  # Skip categories with too few products
            continue
            
        success_rate = len(cat_success) / len(cat_data) * 100
        
        print(f"\n🏷️  {category}")
        print(f"   Total productos: {len(cat_data)}")
        print(f"   Tasa de éxito: {success_rate:.1f}%")
        
        if len(cat_success) > 0:
            print(f"   💰 Precio promedio exitoso: ₹{cat_success['discounted_price'].mean():.0f}")
            print(f"   🔻 Descuento promedio: {cat_success['discount_percentage'].mean():.1f}%")
            print(f"   💵 Rango de precio: ₹{cat_success['discounted_price'].min():.0f} - ₹{cat_success['discounted_price'].max():.0f}")
    
    # Análisis de rangos de descuento
    print("\n" + "="*70)
    print("🔻 ANÁLISIS POR RANGO DE DESCUENTO")
    print("="*70)
    
    discount_ranges = [
        (0, 20, "Bajo (0-20%)"),
        (20, 40, "Moderado (20-40%)"),
        (40, 60, "Alto (40-60%)"),
        (60, 100, "Muy Alto (60%+)")
    ]
    
    for min_disc, max_disc, label in discount_ranges:
        range_data = df[(df['discount_percentage'] >= min_disc) & (df['discount_percentage'] < max_disc)]
        range_success = range_data[range_data['is_success'] == 1]
        
        if len(range_data) > 0:
            success_rate = len(range_success) / len(range_data) * 100
            print(f"\n📊 {label}")
            print(f"   Total productos: {len(range_data)}")
            print(f"   Tasa de éxito: {success_rate:.1f}%")
    
    # Top 10 combinaciones exitosas
    print("\n" + "="*70)
    print("🏆 TOP ESTRATEGIAS EXITOSAS (Categoría + Rango de Precio)")
    print("="*70)
    
    successful['price_range'] = pd.cut(
        successful['discounted_price'], 
        bins=[0, 500, 1000, 2000, 5000, 100000],
        labels=['<500', '500-1K', '1K-2K', '2K-5K', '5K+']
    )
    
    top_combos = successful.groupby(['category', 'price_range']).size().sort_values(ascending=False).head(10)
    
    for i, ((cat, price_range), count) in enumerate(top_combos.items(), 1):
        combo_data = successful[(successful['category'] == cat) & (successful['price_range'] == price_range)]
        avg_discount = combo_data['discount_percentage'].mean()
        print(f"\n{i}. {cat} - Precio: ₹{price_range}")
        print(f"   Productos exitosos: {count}")
        print(f"   Descuento promedio: {avg_discount:.1f}%")
    
    # Recomendaciones finales
    print("\n" + "="*70)
    print("💡 RECOMENDACIONES CLAVE PARA NUEVOS VENDEDORES")
    print("="*70)
    
    # Calculate optimal discount
    optimal_discount = successful['discount_percentage'].median()
    optimal_price = successful['discounted_price'].median()
    
    print(f"""
1. 🎯 Descuento óptimo: {optimal_discount:.0f}%
2. 💰 Precio medio exitoso: ₹{optimal_price:.0f}
3. 🏆 Mejores categorías: {', '.join(df.groupby('category')['is_success'].mean().nlargest(3).index.tolist())}
4. 📊 Evita: Descuentos extremos (<20% o >80%)
5. ✅ Usa: Estrategia de descuento 30-60% en categorías populares
    """)

if __name__ == "__main__":
    analyze_pricing_strategies()
