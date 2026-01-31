import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

def analyze_investment_opportunities(df):
    """
    Analyze investment opportunities across different zones
    """
    if df.empty:
        print("Error: No data to analyze")
        return None
    
    print(f"Analyzing investment opportunities for {len(df)} zones...")
    
    # Initialize investment analysis columns
    investment_data = []
    
    for idx, row in df.iterrows():
        zone = row.get('zone', f'Zone_{idx}')
        
        # Extract key metrics
        growth_index = row.get('overall_growth_index', 0)
        volume_index = row.get('volume_index', 0)
        growth_rate = row.get('recent_ride_growth_rate', 0)
        total_revenue = row.get('total_revenue', 0)
        market_share = row.get('market_share_percent', 0)
        
        # Investment priority calculation
        priority_score = calculate_investment_priority(row)
        
        # Investment type determination
        investment_type = determine_investment_type(row, priority_score)
        
        # Estimated investment amount
        investment_amount = calculate_investment_amount(row)
        
        # Expected ROI
        expected_roi = calculate_expected_roi(row, investment_amount)
        
        # Investment timeline
        timeline = determine_investment_timeline(priority_score, investment_type)
        
        # Risk assessment
        risk_level = assess_investment_risk(row)
        
        # Key performance indicators to track
        kpis = determine_key_kpis(row)
        
        # Success metrics
        success_metrics = define_success_metrics(row, investment_type)
        
        investment_data.append({
            'zone': zone,
            'investment_priority_score': priority_score,
            'investment_priority': get_priority_label(priority_score),
            'investment_type': investment_type,
            'recommended_action': row.get('recommendation', ''),
            'estimated_investment_amount': investment_amount,
            'expected_roi_percent': expected_roi,
            'expected_payback_months': calculate_payback_period(row, investment_amount),
            'investment_timeline': timeline,
            'risk_level': risk_level,
            'risk_factors': identify_risk_factors(row),
            'key_performance_indicators': kpis,
            'success_metrics': success_metrics,
            'required_resources': identify_required_resources(investment_type),
            'growth_category': row.get('growth_category', 'Unknown'),
            'current_metrics': {
                'growth_index': growth_index,
                'volume_index': volume_index,
                'revenue': total_revenue,
                'market_share': market_share
            }
        })
    
    return pd.DataFrame(investment_data)

def calculate_investment_priority(row):
    """
    Calculate investment priority score (0-100)
    """
    score = 0
    
    # Growth potential (35%)
    growth_category = row.get('growth_category', '')
    if growth_category == 'High Growth':
        score += 35
    elif growth_category == 'Medium Growth':
        score += 25
    elif growth_category == 'Stable':
        score += 15
    else:
        score += 5
    
    # Market size (25%)
    volume_index = row.get('volume_index', 0)
    if volume_index > 80:
        score += 25
    elif volume_index > 60:
        score += 18
    elif volume_index > 40:
        score += 10
    else:
        score += 5
    
    # Revenue generation (20%)
    revenue = row.get('total_revenue', 0)
    if revenue > 1000000:  # 1 million
        score += 20
    elif revenue > 500000:
        score += 15
    elif revenue > 100000:
        score += 10
    else:
        score += 5
    
    # Growth consistency (15%)
    consistency = row.get('growth_consistency', 0.5)
    score += consistency * 15
    
    # Competition advantage (5%)
    if row.get('competitor_density', 'Medium') == 'Low':
        score += 5
    elif row.get('competitor_density', 'Medium') == 'Medium':
        score += 3
    else:
        score += 1
    
    return min(100, score)

def determine_investment_type(row, priority_score):
    """
    Determine the type of investment needed
    """
    growth_category = row.get('growth_category', '')
    volume_index = row.get('volume_index', 0)
    
    if priority_score >= 80:
        if growth_category == 'High Growth' and volume_index > 70:
            return "Aggressive Expansion"
        elif growth_category == 'High Growth':
            return "Growth Capital Investment"
        else:
            return "Strategic Investment"
    
    elif priority_score >= 60:
        if growth_category == 'Medium Growth':
            return "Moderate Growth Investment"
        else:
            return "Optimization Investment"
    
    elif priority_score >= 40:
        if row.get('growth_rate_index', 0) > 60:
            return "Selective Growth Investment"
        else:
            return "Maintenance & Improvement"
    
    else:
        return "Minimal Investment - Monitor Only"

def calculate_investment_amount(row):
    """
    Calculate recommended investment amount
    """
    base_revenue = row.get('total_revenue', 0)
    growth_category = row.get('growth_category', '')
    
    # Investment as percentage of revenue
    if growth_category == 'High Growth':
        investment_percentage = 0.15  # 15%
    elif growth_category == 'Medium Growth':
        investment_percentage = 0.10  # 10%
    elif growth_category == 'Stable':
        investment_percentage = 0.05  # 5%
    else:
        investment_percentage = 0.02  # 2%
    
    # Minimum and maximum caps
    min_investment = 50000  # 50,000 minimum
    max_investment = 5000000  # 5 million maximum
    
    investment = base_revenue * investment_percentage
    return max(min_investment, min(max_investment, investment))

def calculate_expected_roi(row, investment_amount):
    """
    Calculate expected return on investment
    """
    current_revenue = row.get('total_revenue', 0)
    growth_rate = max(0.01, row.get('recent_ride_growth_rate', 0) / 100)
    
    # Base growth without investment
    base_growth_factor = 1 + growth_rate
    
    # Additional growth from investment
    if investment_amount > current_revenue * 0.1:  # Large investment
        investment_boost = 0.25
    elif investment_amount > current_revenue * 0.05:  # Medium investment
        investment_boost = 0.15
    else:  # Small investment
        investment_boost = 0.08
    
    # Projected revenue
    projected_revenue = current_revenue * (base_growth_factor + investment_boost)
    
    # ROI calculation
    if investment_amount > 0:
        roi = ((projected_revenue - current_revenue - investment_amount) / investment_amount) * 100
    else:
        roi = 0
    
    return max(0, roi)  # Don't show negative ROI

def calculate_payback_period(row, investment_amount):
    """
    Calculate expected payback period in months
    """
    current_revenue = row.get('total_revenue', 0)
    expected_roi = calculate_expected_roi(row, investment_amount)
    
    if investment_amount > 0 and expected_roi > 0:
        additional_revenue_per_year = investment_amount * (expected_roi / 100)
        if additional_revenue_per_year > 0:
            payback_months = (investment_amount / additional_revenue_per_year) * 12
        else:
            payback_months = 999  # Very long payback
    else:
        payback_months = 999
    
    return min(999, payback_months)

def determine_investment_timeline(priority_score, investment_type):
    """
    Determine investment timeline
    """
    if priority_score >= 80:
        return "Immediate (1-3 months)"
    elif priority_score >= 60:
        return "Short-term (3-6 months)"
    elif priority_score >= 40:
        return "Medium-term (6-12 months)"
    else:
        return "Long-term (12+ months) or Monitor"

def assess_investment_risk(row):
    """
    Assess investment risk level
    """
    risk_score = 0
    
    # Growth volatility
    volatility = row.get('ride_growth_volatility', 0)
    if volatility > 30:
        risk_score += 3
    elif volatility > 20:
        risk_score += 2
    elif volatility > 10:
        risk_score += 1
    
    # Market share
    market_share = row.get('market_share_percent', 0)
    if market_share < 5:
        risk_score += 2
    elif market_share < 10:
        risk_score += 1
    
    # Growth consistency
    consistency = row.get('growth_consistency', 0.5)
    if consistency < 0.3:
        risk_score += 3
    elif consistency < 0.5:
        risk_score += 2
    elif consistency < 0.7:
        risk_score += 1
    
    # Competition
    if row.get('competitor_density', 'Medium') == 'High':
        risk_score += 2
    elif row.get('competitor_density', 'Medium') == 'Medium':
        risk_score += 1
    
    # Determine risk level
    if risk_score >= 6:
        return "High Risk"
    elif risk_score >= 4:
        return "Medium Risk"
    elif risk_score >= 2:
        return "Low Risk"
    else:
        return "Very Low Risk"

def identify_risk_factors(row):
    """
    Identify specific risk factors
    """
    factors = []
    
    if row.get('ride_growth_volatility', 0) > 25:
        factors.append("High growth volatility")
    
    if row.get('market_share_percent', 0) < 10:
        factors.append("Low market share")
    
    if row.get('growth_consistency', 0.5) < 0.5:
        factors.append("Inconsistent growth")
    
    if row.get('recent_ride_growth_rate', 0) < 0:
        factors.append("Negative recent growth")
    
    if row.get('competitor_density', 'Medium') == 'High':
        factors.append("High competition")
    
    return "; ".join(factors) if factors else "Minimal risks identified"

def determine_key_kpis(row):
    """
    Determine key performance indicators to track
    """
    kpis = ["Ride volume", "Revenue growth", "Customer satisfaction"]
    
    if row.get('growth_category') == 'High Growth':
        kpis.extend(["Market share growth", "Driver utilization rate"])
    
    if row.get('avg_ride_distance', 0) > 10:
        kpis.append("Average trip distance")
    
    if 'peak_hour_demand' in row and row['peak_hour_demand'] > 1.5:
        kpis.append("Peak hour service level")
    
    return "; ".join(kpis)

def define_success_metrics(row, investment_type):
    """
    Define success metrics for the investment
    """
    metrics = []
    
    if "Expansion" in investment_type:
        metrics.extend([
            "20% increase in ride volume",
            "15% revenue growth",
            "Improved market share"
        ])
    
    if "Growth" in investment_type:
        metrics.extend([
            "Sustained growth rate >15%",
            "Increased driver supply by 25%",
            "Reduced customer wait time by 20%"
        ])
    
    if "Optimization" in investment_type:
        metrics.extend([
            "10% cost reduction",
            "5% efficiency improvement",
            "Higher customer ratings"
        ])
    
    # Always include baseline metrics
    if not metrics:
        metrics = [
            "Maintain current growth rate",
            "Improve operational efficiency",
            "Enhance customer experience"
        ]
    
    return "; ".join(metrics)

def identify_required_resources(investment_type):
    """
    Identify required resources for the investment
    """
    resources = []
    
    if "Expansion" in investment_type or "Growth" in investment_type:
        resources.extend(["Additional drivers", "Marketing budget", "Management oversight"])
    
    if "Aggressive" in investment_type:
        resources.extend(["Dedicated team", "Technology investment", "Partnership development"])
    
    if "Optimization" in investment_type:
        resources.extend(["Process improvement team", "Training resources", "Technology upgrades"])
    
    return "; ".join(resources) if resources else "Standard operational resources"

def get_priority_label(priority_score):
    """
    Convert priority score to label
    """
    if priority_score >= 80:
        return "Critical Priority"
    elif priority_score >= 70:
        return "High Priority"
    elif priority_score >= 60:
        return "Medium-High Priority"
    elif priority_score >= 50:
        return "Medium Priority"
    elif priority_score >= 40:
        return "Low-Medium Priority"
    elif priority_score >= 30:
        return "Low Priority"
    else:
        return "Monitor Only"

def visualize_investment_insights(investment_df):
    """
    Create visualizations for investment insights
    """
    if investment_df.empty:
        print("No data to visualize")
        return
    
    plt.figure(figsize=(16, 12))
    
    # 1. Investment Priority Distribution
    plt.subplot(3, 3, 1)
    priority_counts = investment_df['investment_priority'].value_counts()
    colors = plt.cm.RdYlGn(np.linspace(0.2, 0.8, len(priority_counts)))
    bars = plt.barh(priority_counts.index, priority_counts.values, color=colors)
    plt.xlabel('Number of Zones')
    plt.title('Investment Priority Distribution')
    plt.gca().invert_yaxis()
    
    # 2. Investment Type Distribution
    plt.subplot(3, 3, 2)
    type_counts = investment_df['investment_type'].value_counts()
    plt.pie(type_counts.values, labels=type_counts.index, autopct='%1.1f%%')
    plt.title('Investment Type Distribution')
    
    # 3. Risk Level Distribution
    plt.subplot(3, 3, 3)
    risk_counts = investment_df['risk_level'].value_counts()
    risk_colors = {'Very Low Risk': 'green', 'Low Risk': 'lightgreen', 
                   'Medium Risk': 'orange', 'High Risk': 'red'}
    colors_list = [risk_colors.get(risk, 'gray') for risk in risk_counts.index]
    plt.bar(risk_counts.index, risk_counts.values, color=colors_list)
    plt.xlabel('Risk Level')
    plt.ylabel('Number of Zones')
    plt.title('Investment Risk Distribution')
    plt.xticks(rotation=45)
    
    # 4. ROI vs Priority Score
    plt.subplot(3, 3, 4)
    plt.scatter(investment_df['investment_priority_score'], 
                investment_df['expected_roi_percent'],
                c=investment_df['investment_priority_score'],
                cmap='RdYlGn', s=100, alpha=0.6)
    plt.xlabel('Priority Score')
    plt.ylabel('Expected ROI (%)')
    plt.title('Priority Score vs Expected ROI')
    plt.colorbar(label='Priority Score')
    
    # 5. Top 10 Zones by Investment Amount
    plt.subplot(3, 3, 5)
    top_investments = investment_df.nlargest(10, 'estimated_investment_amount')
    bars = plt.barh(top_investments['zone'], 
                   top_investments['estimated_investment_amount'] / 1000,
                   color='skyblue')
    plt.xlabel('Investment Amount (Thousands)')
    plt.title('Top 10 Zones by Investment Amount')
    plt.gca().invert_yaxis()
    
    # 6. Expected Payback Period Distribution
    plt.subplot(3, 3, 6)
    # Filter out very long payback periods for visualization
    payback_data = investment_df[investment_df['expected_payback_months'] < 60]
    if not payback_data.empty:
        plt.hist(payback_data['expected_payback_months'], bins=10, alpha=0.7, color='purple')
        plt.xlabel('Expected Payback Period (Months)')
        plt.ylabel('Number of Zones')
        plt.title('Payback Period Distribution')
    
    # 7. Investment Matrix: Priority vs Risk
    plt.subplot(3, 3, 7)
    risk_numeric = investment_df['risk_level'].map({
        'Very Low Risk': 1, 'Low Risk': 2, 'Medium Risk': 3, 'High Risk': 4
    })
    plt.scatter(investment_df['investment_priority_score'], risk_numeric,
                s=investment_df['estimated_investment_amount'] / 5000,
                alpha=0.6, cmap='coolwarm')
    plt.xlabel('Priority Score')
    plt.ylabel('Risk Level (1=Low, 4=High)')
    plt.title('Investment Matrix: Priority vs Risk')
    plt.yticks([1, 2, 3, 4], ['Very Low', 'Low', 'Medium', 'High'])
    
    # 8. Total Investment by Growth Category
    plt.subplot(3, 3, 8)
    investment_by_category = investment_df.groupby('growth_category')['estimated_investment_amount'].sum()
    plt.pie(investment_by_category.values, labels=investment_by_category.index, autopct='%1.1f%%')
    plt.title('Total Investment by Growth Category')
    
    plt.tight_layout()
    plt.savefig('UberAI/Dataset/investment_insights_visualization.png', 
                dpi=150, bbox_inches='tight')
    plt.close()
    
    print("Visualization saved to: UberAI/Dataset/investment_insights_visualization.png")

def generate_investment_summary(investment_df):
    """
    Generate comprehensive investment summary
    """
    if investment_df.empty:
        print("No investment data to summarize")
        return
    
    print("\n" + "="*70)
    print("INVESTMENT INSIGHTS SUMMARY")
    print("="*70)
    
    total_investment = investment_df['estimated_investment_amount'].sum()
    avg_roi = investment_df['expected_roi_percent'].mean()
    total_zones = len(investment_df)
    
    print(f"\nTotal Zones Analyzed: {total_zones}")
    print(f"Total Recommended Investment: ₹{total_investment:,.2f}")
    print(f"Average Expected ROI: {avg_roi:.1f}%")
    
    # Breakdown by priority
    print(f"\nInvestment Breakdown by Priority:")
    for priority in ['Critical Priority', 'High Priority', 'Medium-High Priority',
                     'Medium Priority', 'Low-Medium Priority', 'Low Priority', 'Monitor Only']:
        zones = investment_df[investment_df['investment_priority'] == priority]
        if not zones.empty:
            investment = zones['estimated_investment_amount'].sum()
            print(f"  {priority}: {len(zones)} zones, ₹{investment:,.2f}")
    
    # Top investment opportunities
    print(f"\nTop 5 Investment Opportunities:")
    top_opportunities = investment_df.nlargest(5, 'investment_priority_score')
    for idx, row in top_opportunities.iterrows():
        print(f"  {idx+1}. {row['zone']}")
        print(f"     Priority: {row['investment_priority']} ({row['investment_priority_score']:.0f})")
        print(f"     Type: {row['investment_type']}")
        print(f"     Investment: ₹{row['estimated_investment_amount']:,.2f}")
        print(f"     Expected ROI: {row['expected_roi_percent']:.1f}%")
        print(f"     Risk: {row['risk_level']}")
    
    # Risk analysis
    print(f"\nRisk Analysis:")
    risk_summary = investment_df['risk_level'].value_counts()
    for risk, count in risk_summary.items():
        percentage = (count / total_zones) * 100
        print(f"  {risk}: {count} zones ({percentage:.1f}%)")
    
    # Quick recommendations
    print(f"\nQuick Recommendations:")
    high_priority = investment_df[investment_df['investment_priority'].isin(['Critical Priority', 'High Priority'])]
    if not high_priority.empty:
        print(f"  1. Focus on {len(high_priority)} high-priority zones first")
        print(f"  2. Allocate ₹{high_priority['estimated_investment_amount'].sum():,.2f} for immediate investments")
    
    high_roi = investment_df[investment_df['expected_roi_percent'] > 50]
    if not high_roi.empty:
        print(f"  3. {len(high_roi)} zones offer >50% ROI potential")

def main():
    """
    Main function to generate investment insights
    """
    try:
        # Load business recommendations
        file_path = "UberAI/Dataset/business_recommendations.csv"
        print(f"Loading data from: {file_path}")
        
        df = pd.read_csv(file_path)
        print(f"Data loaded successfully. Shape: {df.shape}")
        
        # Check if we have required columns
        if 'zone' not in df.columns:
            # Try to find a zone column
            zone_cols = [col for col in df.columns if 'zone' in col.lower() or 'location' in col.lower()]
            if zone_cols:
                df = df.rename(columns={zone_cols[0]: 'zone'})
            else:
                df['zone'] = [f'Zone_{i+1}' for i in range(len(df))]
        
        # Generate investment insights
        print("\nGenerating investment insights...")
        investment_df = analyze_investment_opportunities(df)
        
        if investment_df is not None:
            # Save investment insights
            output_path = "UberAI/Dataset/investment_insights.csv"
            investment_df.to_csv(output_path, index=False)
            print(f"\nInvestment insights saved to: {output_path}")
            
            # Create visualizations
            print("\nCreating visualizations...")
            visualize_investment_insights(investment_df)
            
            # Generate summary
            generate_investment_summary(investment_df)
            
            # Save a simplified version for quick reference
            simplified_cols = ['zone', 'investment_priority', 'investment_type', 
                              'estimated_investment_amount', 'expected_roi_percent',
                              'risk_level', 'investment_timeline']
            simplified_df = investment_df[simplified_cols]
            simplified_path = "UberAI/Dataset/investment_quick_reference.csv"
            simplified_df.to_csv(simplified_path, index=False)
            print(f"\nQuick reference saved to: {simplified_path}")
        
        else:
            print("Failed to generate investment insights")
            
    except FileNotFoundError as e:
        print(f"Error: File not found at path: {file_path}")
        print("Please ensure business_recommendations.csv exists.")
        print("You may need to run expansion_recommendation.py first.")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
