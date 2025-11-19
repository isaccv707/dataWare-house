"""
Amazon Market Analysis for Entrepreneurs
This script analyzes the Amazon dataset to provide insights for sellers
who don't have reviews yet, focusing on price and category analysis.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

# Load and prepare data
def load_data():
    df = pd.read_csv('data/amazon.csv')
    
    # Clean numeric columns
    df['discounted_price'] = df['discounted_price'].str.replace('$', '').str.replace(',', '')
    df['discounted_price'] = pd.to_numeric(df['discounted_price'], errors='coerce')
    
    df['actual_price'] = df['actual_price'].str.replace('$', '').str.replace(',', '')
    df['actual_price'] = pd.to_numeric(df['actual_price'], errors='coerce')
    
    df['discount_percentage'] = df['discount_percentage'].str.replace('%', '')
    df['discount_percentage'] = pd.to_numeric(df['discount_percentage'], errors='coerce')
    
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
    
    df['rating_count'] = df['rating_count'].str.replace(',', '')
    df['rating_count'] = pd.to_numeric(df['rating_count'], errors='coerce').fillna(0).astype(int)
    
    # Extract main category
    df['main_category'] = df['category'].str.split('|').str[0]
    
    # Define success criteria
    df['is_successful'] = ((df['rating'] >= 4.0) & (df['rating_count'] >= 50)).astype(int)
    
    return df


def analyze_categories(df):
    """Analyze which categories have highest success rates"""
    print("\n" + "="*80)
    print("📊 CATEGORY ANALYSIS")
    print("="*80)
    
    category_stats = df.groupby('main_category').agg({
        'is_successful': 'mean',
        'product_id': 'count',
        'discounted_price': ['mean', 'median'],
        'rating': 'mean',
        'rating_count': 'mean'
    }).round(2)
    
    category_stats.columns = ['Success_Rate', 'Product_Count', 'Avg_Price', 'Median_Price', 'Avg_Rating', 'Avg_Reviews']
    category_stats = category_stats.sort_values('Success_Rate', ascending=False)
    
    print("\n🏆 TOP 10 CATEGORIES BY SUCCESS RATE:")
    print(category_stats.head(10))
    
    return category_stats


def analyze_price_ranges(df):
    """Analyze success rates by price ranges"""
    print("\n" + "="*80)
    print("💰 PRICE RANGE ANALYSIS")
    print("="*80)
    
    # Define price ranges
    df['price_range'] = pd.cut(df['discounted_price'], 
                                bins=[0, 200, 500, 1000, 2000, 5000, float('inf')],
                                labels=['Under $200', '$200-500', '$500-1000', 
                                       '$1000-2000', '$2000-5000', 'Over $5000'])
    
    price_analysis = df.groupby('price_range').agg({
        'is_successful': ['mean', 'count'],
        'rating': 'mean',
        'rating_count': 'mean',
        'discount_percentage': 'mean'
    }).round(2)
    
    price_analysis.columns = ['Success_Rate', 'Product_Count', 'Avg_Rating', 'Avg_Reviews', 'Avg_Discount']
    
    print("\n📈 SUCCESS BY PRICE RANGE:")
    print(price_analysis)
    
    return price_analysis


def analyze_discount_impact(df):
    """Analyze how discount percentage affects success"""
    print("\n" + "="*80)
    print("🎯 DISCOUNT STRATEGY ANALYSIS")
    print("="*80)
    
    df['discount_range'] = pd.cut(df['discount_percentage'], 
                                   bins=[0, 20, 40, 60, 80, 100],
                                   labels=['0-20%', '20-40%', '40-60%', '60-80%', '80-100%'])
    
    discount_analysis = df.groupby('discount_range').agg({
        'is_successful': ['mean', 'count'],
        'rating': 'mean',
        'rating_count': 'mean',
        'discounted_price': 'mean'
    }).round(2)
    
    discount_analysis.columns = ['Success_Rate', 'Product_Count', 'Avg_Rating', 'Avg_Reviews', 'Avg_Price']
    
    print("\n💸 SUCCESS BY DISCOUNT RANGE:")
    print(discount_analysis)
    
    return discount_analysis


def get_recommendations(df):
    """Provide actionable recommendations for new sellers"""
    print("\n" + "="*80)
    print("🎯 RECOMMENDATIONS FOR NEW SELLERS (NO REVIEWS YET)")
    print("="*80)
    
    # Best categories for new sellers
    category_stats = df.groupby('main_category').agg({
        'is_successful': 'mean',
        'product_id': 'count',
        'discounted_price': 'median',
        'discount_percentage': 'mean'
    }).round(2)
    
    category_stats.columns = ['Success_Rate', 'Competition', 'Median_Price', 'Avg_Discount']
    
    # Filter for categories with reasonable competition and good success rate
    good_categories = category_stats[
        (category_stats['Success_Rate'] > 0.5) & 
        (category_stats['Competition'] > 10)
    ].sort_values('Success_Rate', ascending=False)
    
    print("\n✅ RECOMMENDED CATEGORIES:")
    print("(High success rate with manageable competition)\n")
    print(good_categories.head(10))
    
    # Optimal price ranges
    print("\n💰 OPTIMAL PRICE RANGES:")
    successful_products = df[df['is_successful'] == 1]
    price_percentiles = successful_products['discounted_price'].describe()
    print(f"\n  • 25th Percentile (Lower bound): ${price_percentiles['25%']:.0f}")
    print(f"  • 50th Percentile (Sweet spot): ${price_percentiles['50%']:.0f}")
    print(f"  • 75th Percentile (Upper bound): ${price_percentiles['75%']:.0f}")
    
    # Optimal discount strategy
    print("\n🎯 OPTIMAL DISCOUNT STRATEGY:")
    successful_discount = successful_products['discount_percentage'].describe()
    print(f"\n  • Average discount of successful products: {successful_discount['mean']:.1f}%")
    print(f"  • Recommended discount range: {successful_discount['25%']:.0f}% - {successful_discount['75%']:.0f}%")
    
    return good_categories


def predict_success_probability(category, price, discount_pct, df):
    """
    Predict success probability for a new product without reviews
    Based on similar products in the category
    """
    print("\n" + "="*80)
    print("🔮 SUCCESS PROBABILITY CALCULATOR")
    print("="*80)
    
    # Filter similar products
    similar_products = df[df['main_category'] == category].copy()
    
    if len(similar_products) == 0:
        print(f"\n❌ No data available for category: {category}")
        return None
    
    # Calculate price and discount similarity scores
    similar_products['price_diff'] = abs(similar_products['discounted_price'] - price)
    similar_products['discount_diff'] = abs(similar_products['discount_percentage'] - discount_pct)
    
    # Find top 50 most similar products
    similar_products['similarity_score'] = (
        1 / (1 + similar_products['price_diff'] / price) * 0.6 +
        1 / (1 + similar_products['discount_diff'] / 10) * 0.4
    )
    
    top_similar = similar_products.nlargest(50, 'similarity_score')
    
    success_rate = top_similar['is_successful'].mean()
    
    print(f"\n📦 Your Product Profile:")
    print(f"  • Category: {category}")
    print(f"  • Price: ${price:,.0f}")
    print(f"  • Discount: {discount_pct:.1f}%")
    
    print(f"\n📊 Analysis based on {len(top_similar)} similar products:")
    print(f"  • Success Rate: {success_rate*100:.1f}%")
    print(f"  • Average Rating: {top_similar['rating'].mean():.2f}")
    print(f"  • Average Reviews: {top_similar['rating_count'].mean():.0f}")
    
    if success_rate >= 0.7:
        verdict = "🟢 EXCELLENT - Highly recommended!"
    elif success_rate >= 0.5:
        verdict = "🟡 GOOD - Solid opportunity with proper marketing"
    elif success_rate >= 0.3:
        verdict = "🟠 MODERATE - Challenging but possible"
    else:
        verdict = "🔴 LOW - Consider different category or pricing"
    
    print(f"\n{verdict}")
    
    return success_rate


def main():
    """Main analysis workflow"""
    print("\n" + "="*80)
    print("🚀 AMAZON MARKET ANALYSIS FOR ENTREPRENEURS")
    print("="*80)
    print("\nAnalyzing market data to help you make informed decisions...")
    
    # Load data
    df = load_data()
    print(f"\n✅ Loaded {len(df)} products from Amazon dataset")
    
    # Run analyses
    category_stats = analyze_categories(df)
    price_analysis = analyze_price_ranges(df)
    discount_analysis = analyze_discount_impact(df)
    recommendations = get_recommendations(df)
    
    # Example prediction
    print("\n" + "="*80)
    print("💡 EXAMPLE: Predicting Success for a New Product")
    print("="*80)
    
    # Example: USB Cable in Computers&Accessories category
    example_category = "Computers&Accessories"
    example_price = 299
    example_discount = 50
    
    predict_success_probability(example_category, example_price, example_discount, df)
    
    print("\n" + "="*80)
    print("📋 SUMMARY & ACTION ITEMS")
    print("="*80)
    print("""
    1. ✅ Choose a category with >50% success rate
    2. ✅ Price your product in the $200-$1,000 range (sweet spot)
    3. ✅ Offer 40-60% discount to be competitive
    4. ✅ Focus on product quality to eventually get good ratings
    5. ✅ Use the calculator above to test different scenarios
    
    💡 Pro Tip: Even in competitive categories, proper pricing and
       quality can lead to success. Start with a strong discount
       to attract initial customers and build reviews!
    """)


if __name__ == "__main__":
    main()
