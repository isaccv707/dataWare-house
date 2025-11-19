"""
Interactive Amazon Market Advisor for Entrepreneurs
Test your product ideas and get instant success predictions!
"""

import pandas as pd
import sys


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


def get_available_categories(df):
    """Get list of available categories sorted by success rate"""
    category_stats = df.groupby('main_category').agg({
        'is_successful': 'mean',
        'product_id': 'count'
    }).round(2)
    
    category_stats.columns = ['Success_Rate', 'Product_Count']
    category_stats = category_stats[category_stats['Product_Count'] >= 10]
    category_stats = category_stats.sort_values('Success_Rate', ascending=False)
    
    return category_stats


def predict_success(category, price, discount_pct, df):
    """Predict success probability based on similar products"""
    
    # Filter for the category
    similar_products = df[df['main_category'] == category].copy()
    
    if len(similar_products) == 0:
        return None, "Category not found in database"
    
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
    competitor_avg_rating = price_competitors['rating'].mean()
    
    results = {
        'success_rate': success_rate,
        'avg_rating': avg_rating,
        'avg_reviews': avg_reviews,
        'num_competitors': num_competitors,
        'competitor_avg_rating': competitor_avg_rating,
        'sample_size': len(top_similar)
    }
    
    return results, None


def get_verdict(success_rate):
    """Get recommendation based on success rate"""
    if success_rate >= 0.75:
        return "🟢 EXCELLENT", "This is a highly promising opportunity! Similar products have a very high success rate."
    elif success_rate >= 0.60:
        return "🟢 GOOD", "Strong opportunity with good potential. Focus on quality and customer service."
    elif success_rate >= 0.45:
        return "🟡 MODERATE", "Decent opportunity but competitive. You'll need strong marketing and excellent product quality."
    elif success_rate >= 0.30:
        return "🟠 CHALLENGING", "Difficult market segment. Consider adjusting your price or choosing a different category."
    else:
        return "🔴 HIGH RISK", "Very challenging market. We recommend exploring other categories or significantly adjusting your strategy."


def print_analysis(category, price, discount_pct, results):
    """Print detailed analysis results"""
    print("\n" + "="*80)
    print("📊 SUCCESS PREDICTION REPORT")
    print("="*80)
    
    print(f"\n📦 YOUR PRODUCT PROFILE:")
    print(f"  • Category: {category}")
    print(f"  • Selling Price: ${price:,.0f}")
    print(f"  • Discount: {discount_pct:.1f}%")
    
    if discount_pct > 0:
        original_price = price / (1 - discount_pct/100)
        print(f"  • Original Price (implied): ${original_price:,.0f}")
    
    print(f"\n📈 MARKET ANALYSIS (Based on {results['sample_size']} similar products):")
    print(f"  • Success Probability: {results['success_rate']*100:.1f}%")
    print(f"  • Expected Average Rating: {results['avg_rating']:.2f}/5.0")
    print(f"  • Expected Average Reviews: {results['avg_reviews']:,.0f}")
    
    print(f"\n🏪 COMPETITION ANALYSIS:")
    print(f"  • Direct Competitors (±20% price): {results['num_competitors']}")
    if results['num_competitors'] > 0:
        print(f"  • Competitors' Average Rating: {results['competitor_avg_rating']:.2f}/5.0")
    
    verdict, explanation = get_verdict(results['success_rate'])
    
    print(f"\n{verdict}")
    print(f"  {explanation}")
    
    print("\n" + "="*80)
    print("💡 RECOMMENDATIONS:")
    print("="*80)
    
    if results['success_rate'] >= 0.6:
        print("  ✅ This looks promising! Here's what to focus on:")
        print("     • Ensure excellent product quality")
        print("     • Offer competitive or better pricing")
        print("     • Provide outstanding customer service")
        print("     • Request reviews from early customers")
    else:
        print("  ⚠️  Consider these improvements:")
        if discount_pct < 40:
            print("     • Increase your discount (aim for 40-60%)")
        if price > 2000:
            print("     • Consider a lower price point initially")
        if results['num_competitors'] > 100:
            print("     • This category is very competitive - differentiate your product")
        print("     • Or explore a different category with higher success rates")
    
    print("\n")


def interactive_mode(df):
    """Interactive consultation mode"""
    print("\n" + "="*80)
    print("🎯 AMAZON ENTREPRENEUR ADVISOR")
    print("="*80)
    print("\nWelcome! I'll help you determine if your product idea is a good fit for Amazon.")
    print("Since you don't have reviews yet, I'll analyze similar products to predict your success.\n")
    
    # Show available categories
    category_stats = get_available_categories(df)
    
    print("📋 AVAILABLE CATEGORIES (with success rates):")
    print("-" * 80)
    for idx, (cat, row) in enumerate(category_stats.head(10).iterrows(), 1):
        print(f"  {idx}. {cat:30s} - Success Rate: {row['Success_Rate']*100:5.1f}% ({int(row['Product_Count'])} products)")
    
    print(f"\n  Total categories available: {len(category_stats)}")
    print("\n" + "-"*80)
    
    while True:
        try:
            # Get category
            print("\n" + "="*80)
            category = input("Enter the category name (or 'quit' to exit): ").strip()
            
            if category.lower() == 'quit':
                print("\nThank you for using Amazon Entrepreneur Advisor! Good luck with your business! 🚀\n")
                break
            
            if category not in df['main_category'].values:
                print(f"\n❌ Category '{category}' not found. Please choose from the list above.")
                continue
            
            # Get price
            price = float(input("Enter your selling price ($): ").strip())
            if price <= 0:
                print("\n❌ Price must be greater than 0")
                continue
            
            # Get discount
            discount = float(input("Enter discount percentage (0-100): ").strip())
            if discount < 0 or discount > 100:
                print("\n❌ Discount must be between 0 and 100")
                continue
            
            # Make prediction
            results, error = predict_success(category, price, discount, df)
            
            if error:
                print(f"\n❌ Error: {error}")
                continue
            
            # Show results
            print_analysis(category, price, discount, results)
            
            # Ask if they want to try another
            again = input("Would you like to analyze another product? (yes/no): ").strip().lower()
            if again not in ['yes', 'y']:
                print("\nThank you for using Amazon Entrepreneur Advisor! Good luck with your business! 🚀\n")
                break
                
        except ValueError:
            print("\n❌ Invalid input. Please enter valid numbers.")
        except KeyboardInterrupt:
            print("\n\nGoodbye! 👋\n")
            break
        except Exception as e:
            print(f"\n❌ An error occurred: {e}")


def main():
    """Main entry point"""
    print("\n")
    print("="*80)
    print("  🚀 AMAZON ENTREPRENEUR ADVISOR")
    print("  Helping you make data-driven decisions about selling on Amazon")
    print("="*80)
    print("\nLoading market data...")
    
    df = load_data()
    print(f"✅ Loaded {len(df)} products from Amazon marketplace\n")
    
    interactive_mode(df)


if __name__ == "__main__":
    main()
