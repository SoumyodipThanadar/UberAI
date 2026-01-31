import pandas as pd
import numpy as np
from datetime import datetime

def opportunity_rules(row):
    """
    Apply business rules to generate expansion recommendations
    """
    recommendations = []
    
    # Rule 1: High Growth Zones
    if row.get('growth_category') == 'High Growth':
        if row.get('overall_growth_index', 0) >= 80:
            if row.get('recent_ride_growth_rate', 0) > 20:
                recommendations.append("Aggressive expansion - add 30% more drivers")
            else:
                recommendations.append("Steady expansion - add 15% more drivers")
    
    # Rule 2: High Volume, Stable Growth
    elif row.get('volume_index', 0) > 70 and row.get('growth_category') == 'Stable':
        if row.get('market_share_percent', 0) > 10:
            recommendations.append("Market leader - focus on retention and premium services")
        else:
            recommendations.append("Strong presence - optimize pricing and improve service quality")
    
    # Rule 3: Emerging Markets (Low volume, high growth)
    elif row.get('volume_index', 0) < 30 and row.get('growth_rate_index', 0) > 70:
        recommendations.append("Emerging market - invest in marketing and driver incentives")
    
    # Rule 4: Declining Zones
    elif row.get('growth_category') == 'Declining':
        if row.get('recent_ride_growth_rate', 0) < -10:
            recommendations.append("Urgent intervention required - analyze root causes")
        else:
            recommendations.append("Monitor closely - consider promotional offers")
    
    # Rule 5: High Growth Volatility
    if row.get('ride_growth_volatility', 0) > 30:
        recommendations.append("High volatility - implement risk mitigation strategies")
    
    # Rule 6: Seasonality Opportunities
    if 'seasonality_peak' in row and row['seasonality_peak']:
        recommendations.append("Seasonal peak expected - prepare surge capacity")
    
    # Rule 7: Competitor Analysis
    if 'competitor_density' in row:
        if row['competitor_density'] == 'High':
            recommendations.append("High competition - differentiate through service quality")
        elif row['competitor_density'] == 'Low':
            recommendations.append("Low competition - capitalize on market gap")
    
    # Rule 8: Revenue Optimization
    if 'avg_booking_value' in row:
        if row['avg_booking_value'] < row.get('city_avg_booking_value', 0) * 0.8:
            recommendations.append("Low average fare - consider upselling strategies")
        elif row['avg_booking_value'] > row.get('city_avg_booking_value', 0) * 1.2:
            recommendations.append("Premium market - focus on luxury services")
    
    # Rule 9: Distance-Based Opportunities
    if 'avg_ride_distance' in row:
        if row['avg_ride_distance'] > 15:
            recommendations.append("Long-distance trips common - consider inter-city expansion")
        elif row['avg_ride_distance'] < 3:
            recommendations.append("Short trips dominant - optimize for quick turnarounds")
    
    # Rule 10: Time-Based Opportunities
    if 'peak_hour_demand' in row:
        if row['peak_hour_demand'] > 1.5:
            recommendations.append("High peak hour demand - implement surge pricing")
    
    # If no specific recommendations, provide general guidance
    if not recommendations:
        if row.get('overall_growth_index', 0) > 50:
            recommendations.append("Moderate growth - maintain current operations with minor optimizations")
        else:
            recommendations.append("Limited growth - focus on cost optimization and market research")
    
    return "; ".join(recommendations)

def calculate_expansion_priority(row):
    """
    Calculate expansion priority score (0-100)
    """
    score = 0
    
    # Growth potential (40%)
    if row.get('growth_category') == 'High Growth':
        score += 40
    elif row.get('growth_category') == 'Medium Growth':
        score += 25
    elif row.get('growth_category') == 'Stable':
        score += 15
    else:
        score += 5
    
    # Market size (30%)
    if row.get('volume_index', 0) > 80:
        score += 30
    elif row.get('volume_index', 0) > 60:
        score += 20
    elif row.get('volume_index', 0) > 40:
        score += 10
    else:
        score += 5
    
    # Profitability (20%)
    if 'avg_booking_value' in row:
        if row['avg_booking_value'] > 500:
            score += 20
        elif row['avg_booking_value'] > 300:
            score += 15
        elif row['avg_booking_value'] > 200:
            score += 10
        else:
            score += 5
    else:
        score += 10  # Default
    
    # Competition (10%)
    if 'competitor_density' in row:
        if row['competitor_density'] == 'Low':
            score += 10
        elif row['competitor_density'] == 'Medium':
            score += 7
        else:
            score += 3
    else:
        score += 5  # Default
    
    return min(100, score)

def generate_expansion_plan(df):
    """
    Generate comprehensive expansion plan with budget estimates
    """
    expansion_plans = []
    
    for idx, row in df.iterrows():
        zone = row.get('zone', f'Zone_{idx}')
        priority = calculate_expansion_priority(row)
        
        # Determine expansion type based on metrics
        if row.get('growth_category') == 'High Growth' and row.get('volume_index', 0) > 70:
            expansion_type = "Aggressive Expansion"
            budget_multiplier = 1.5
            timeline = "Short-term (1-3 months)"
        elif row.get('growth_category') in ['High Growth', 'Medium Growth']:
            expansion_type = "Moderate Expansion"
            budget_multiplier = 1.0
            timeline = "Medium-term (3-6 months)"
        else:
            expansion_type = "Maintain & Optimize"
            budget_multiplier = 0.5
            timeline = "Long-term (6-12 months)"
        
        # Calculate estimated budget (simplified)
        base_budget = row.get('total_revenue', 0) * 0.1  # 10% of revenue
        estimated_budget = base_budget * budget_multiplier
        
        # Resource allocation recommendations
        resources = []
        if row.get('growth_rate_index', 0) > 70:
            resources.append("Additional drivers")
        if row.get('peak_hour_demand', 0) > 1.5:
            resources.append("Surge pricing strategy")
        if row.get('avg_ride_distance', 0) > 15:
            resources.append("Long-distance vehicle fleet")
        if row.get('ride_growth_volatility', 0) > 20:
            resources.append("Risk management team")
        
        expansion_plans.append({
            'zone': zone,
            'expansion_priority': priority,
            'expansion_type': expansion_type,
            'estimated_budget': estimated_budget,
            'timeline': timeline,
            'required_resources': ", ".join(resources) if resources else "Standard operations",
            'growth_category': row.get('growth_category', 'Unknown'),
            'current_rides': row.get('total_rides', 0),
            'current_revenue': row.get('total_revenue', 0),
            'growth_rate': row.get('recent_ride_growth_rate', 0)
        })
    
    return pd.DataFrame(expansion_plans)

def calculate_roi_metrics(df):
    """
    Calculate ROI metrics for expansion decisions
    """
    roi_data = []
    
    for idx, row in df.iterrows():
        zone = row.get('zone', f'Zone_{idx}')
        
        # Simplified ROI calculation
        current_revenue = row.get('total_revenue', 0)
        growth_rate = max(0.01, row.get('recent_ride_growth_rate', 0) / 100)  # Convert to decimal
        
        # Estimated investment
        if row.get('growth_category') == 'High Growth':
            investment = current_revenue * 0.15  # 15% of revenue
            expected_growth_boost = 0.3  # 30% boost from investment
        elif row.get('growth_category') == 'Medium Growth':
            investment = current_revenue * 0.10  # 10% of revenue
            expected_growth_boost = 0.2  # 20% boost from investment
        else:
            investment = current_revenue * 0.05  # 5% of revenue
            expected_growth_boost = 0.1  # 10% boost from investment
        
        # Projected revenue
        projected_revenue = current_revenue * (1 + growth_rate + expected_growth_boost)
        
        # ROI calculation
        roi = ((projected_revenue - current_revenue - investment) / investment) * 100
        payback_period = investment / ((projected_revenue - current_revenue) / 12)  # Months
        
        roi_data.append({
            'zone': zone,
            'current_revenue': current_revenue,
            'projected_revenue': projected_revenue,
            'required_investment': investment,
            'expected_roi_percent': roi,
            'payback_period_months': payback_period,
            'investment_risk': 'Low' if roi > 50 else 'Medium' if roi > 20 else 'High'
        })
    
    return pd.DataFrame(roi_data)

def visualize_recommendations(df):
    """
    Create visualizations for expansion recommendations
    """
    import matplotlib.pyplot as plt
    
    if df.empty:
        print("No data to visualize")
        return
    
    # Create a priority matrix
    plt.figure(figsize=(12, 8))
    
    # Scatter plot: Growth vs Volume with priority color coding
    if 'volume_index' in df.columns and 'growth_rate_index' in df.columns:
        plt.subplot(2, 2, 1)
        
        # Create color map based on priority
        colors = []
        for _, row in df.iterrows():
            priority = calculate_expansion_priority(row)
            if priority >= 80:
                colors.append('green')
            elif priority >= 60:
                colors.append('yellow')
            elif priority >= 40:
                colors.append('orange')
            else:
                colors.append('red')
        
        scatter = plt.scatter(df['volume_index'], df['growth_rate_index'],
                            c=colors, s=100, alpha=0.6)
        
        plt.xlabel('Volume Index')
        plt.ylabel('Growth Rate Index')
        plt.title('Expansion Priority Matrix')
        plt.grid(True, alpha=0.3)
        
        # Add quadrant lines
        plt.axhline(y=50, color='gray', linestyle='--', alpha=0.5)
        plt.axvline(x=50, color='gray', linestyle='--', alpha=0.5)
        
        # Add legend
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='green', alpha=0.6, label='High Priority (80+)'),
            Patch(facecolor='yellow', alpha=0.6, label='Medium Priority (60-79)'),
            Patch(facecolor='orange', alpha=0.6, label='Low Priority (40-59)'),
            Patch(facecolor='red', alpha=0.6, label='No Priority (<40)')
        ]
        plt.legend(handles=legend_elements, loc='upper right')
    
    # Bar chart: Top 10 zones by priority
    plt.subplot(2, 2, 2)
    df['expansion_priority'] = df.apply(calculate_expansion_priority, axis=1)
    top_zones = df.nlargest(10, 'expansion_priority')
    bars = plt.barh(top_zones['zone'], top_zones['expansion_priority'], color='skyblue')
    plt.xlabel('Expansion Priority Score')
    plt.title('Top 10 Zones for Expansion')
    plt.gca().invert_yaxis()
    
    # Add value labels
    for bar in bars:
        width = bar.get_width()
        plt.text(width, bar.get_y() + bar.get_height()/2, 
                f'{width:.0f}', ha='left', va='center')
    
    # Pie chart: Expansion type distribution
    plt.subplot(2, 2, 3)
    expansion_plans = generate_expansion_plan(df)
    expansion_counts = expansion_plans['expansion_type'].value_counts()
    plt.pie(expansion_counts.values, labels=expansion_counts.index, autopct='%1.1f%%')
    plt.title('Distribution of Expansion Types')
    
    # ROI distribution
    plt.subplot(2, 2, 4)
    roi_df = calculate_roi_metrics(df)
    risk_counts = roi_df['investment_risk'].value_counts()
    plt.bar(risk_counts.index, risk_counts.values, color=['green', 'orange', 'red'])
    plt.xlabel('Investment Risk Level')
    plt.ylabel('Number of Zones')
    plt.title('Investment Risk Distribution')
    
    plt.tight_layout()
    plt.savefig('UberAI/Dataset/expansion_recommendations_visualization.png', 
                dpi=150, bbox_inches='tight')
    plt.close()
    
    print("Visualization saved to: UberAI/Dataset/expansion_recommendations_visualization.png")

def main():
    """
    Main function to generate expansion recommendations
    """
    try:
        # Load growth index data
        file_path = "UberAI/Dataset/growth_index.csv"
        print(f"Loading data from: {file_path}")
        
        df = pd.read_csv(file_path)
        print(f"Data loaded successfully. Shape: {df.shape}")
        
        # Check required columns
        required_columns = ['zone', 'growth_category', 'overall_growth_index']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            print(f"Warning: Missing required columns: {missing_columns}")
            print("Available columns:", df.columns.tolist())
            
            # Try to find alternative column names
            if 'zone' not in df.columns:
                zone_cols = [col for col in df.columns if 'zone' in col.lower() or 'location' in col.lower()]
                if zone_cols:
                    df = df.rename(columns={zone_cols[0]: 'zone'})
                    print(f"Renamed '{zone_cols[0]}' to 'zone'")
        
        # Apply opportunity rules
        print("\nApplying business rules to generate recommendations...")
        df['recommendation'] = df.apply(opportunity_rules, axis=1)
        
        # Calculate expansion priority
        df['expansion_priority'] = df.apply(calculate_expansion_priority, axis=1)
        
        # Generate expansion plan
        print("Generating expansion plans...")
        expansion_plan = generate_expansion_plan(df)
        
        # Calculate ROI metrics
        print("Calculating ROI metrics...")
        roi_metrics = calculate_roi_metrics(df)
        
        # Save all outputs
        # 1. Main recommendations
        output_path = "UberAI/Dataset/business_recommendations.csv"
        df.to_csv(output_path, index=False)
        print(f"\nBusiness recommendations saved to: {output_path}")
        
        # 2. Expansion plan
        plan_path = "UberAI/Dataset/expansion_plan.csv"
        expansion_plan.to_csv(plan_path, index=False)
        print(f"Expansion plan saved to: {plan_path}")
        
        # 3. ROI metrics
        roi_path = "UberAI/Dataset/roi_metrics.csv"
        roi_metrics.to_csv(roi_path, index=False)
        print(f"ROI metrics saved to: {roi_path}")
        
        # Create visualizations
        print("\nCreating visualizations...")
        visualize_recommendations(df)
        
        # Print summary
        print("\n" + "="*60)
        print("EXPANSION RECOMMENDATIONS SUMMARY")
        print("="*60)
        
        print(f"\nTotal zones analyzed: {len(df)}")
        
        # Top recommendations
        print(f"\nTop 5 High Priority Zones:")
        top_priority = df.nlargest(5, 'expansion_priority')
        for idx, row in top_priority.iterrows():
            print(f"{idx+1}. {row.get('zone', 'Unknown')}: "
                  f"Priority {row['expansion_priority']:.0f} - {row['recommendation']}")
        
        # Investment summary
        print(f"\nInvestment Summary:")
        total_investment = roi_metrics['required_investment'].sum()
        avg_roi = roi_metrics['expected_roi_percent'].mean()
        print(f"Total recommended investment: ₹{total_investment:,.0f}")
        print(f"Average expected ROI: {avg_roi:.1f}%")
        
        # Save a quick reference file
        summary_df = pd.merge(
            df[['zone', 'recommendation', 'expansion_priority']],
            expansion_plan[['zone', 'expansion_type', 'timeline', 'estimated_budget']],
            on='zone'
        )
        summary_df = pd.merge(
            summary_df,
            roi_metrics[['zone', 'expected_roi_percent', 'investment_risk']],
            on='zone'
        )
        summary_path = "UberAI/Dataset/expansion_summary.csv"
        summary_df.to_csv(summary_path, index=False)
        print(f"\nQuick reference summary saved to: {summary_path}")
        
    except FileNotFoundError as e:
        print(f"Error: File not found at path: {file_path}")
        print("Please ensure growth_index.csv exists in the Dataset folder.")
        print("You may need to run growth_index.py first.")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()