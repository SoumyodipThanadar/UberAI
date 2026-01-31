import pandas as pd
import numpy as np
from typing import Dict, List, Any

class OpportunityRules:
    """
    Comprehensive business rules for identifying expansion opportunities
    """
    
    def __init__(self, thresholds: Dict[str, Any] = None):
        """
        Initialize opportunity rules with custom thresholds
        
        Parameters:
        thresholds: Dictionary containing threshold values for various metrics
        """
        self.thresholds = thresholds or {
            'growth_index_high': 0.7,
            'growth_index_medium': 0.4,
            'volume_high': 0.7,
            'volume_medium': 0.4,
            'growth_rate_high': 15,  # percentage
            'growth_rate_medium': 5,  # percentage
            'market_share_high': 15,  # percentage
            'market_share_medium': 5,  # percentage
            'revenue_high': 1000000,  # absolute value
            'revenue_medium': 500000,  # absolute value
            'competition_low': 0.3,
            'competition_high': 0.7,
            'volatility_high': 25,  # percentage
            'consistency_high': 0.7,  # ratio
            'distance_long': 15,  # kilometers
            'distance_short': 3,   # kilometers
        }
        
    def apply_rules(self, row: pd.Series) -> Dict[str, Any]:
        """
        Apply all business rules to a single row/zone
        
        Returns:
        Dictionary containing all rule evaluations and final recommendations
        """
        evaluations = {}
        
        # Rule 1: Growth Index Analysis
        evaluations['growth_index_evaluation'] = self.evaluate_growth_index(row)
        
        # Rule 2: Volume Analysis
        evaluations['volume_evaluation'] = self.evaluate_volume(row)
        
        # Rule 3: Growth Rate Analysis
        evaluations['growth_rate_evaluation'] = self.evaluate_growth_rate(row)
        
        # Rule 4: Market Share Analysis
        evaluations['market_share_evaluation'] = self.evaluate_market_share(row)
        
        # Rule 5: Revenue Analysis
        evaluations['revenue_evaluation'] = self.evaluate_revenue(row)
        
        # Rule 6: Competition Analysis
        evaluations['competition_evaluation'] = self.evaluate_competition(row)
        
        # Rule 7: Risk Assessment
        evaluations['risk_assessment'] = self.assess_risk(row)
        
        # Rule 8: Seasonality Analysis
        evaluations['seasonality_evaluation'] = self.evaluate_seasonality(row)
        
        # Rule 9: Distance Analysis
        evaluations['distance_evaluation'] = self.evaluate_distance(row)
        
        # Rule 10: Time Pattern Analysis
        evaluations['time_pattern_evaluation'] = self.evaluate_time_patterns(row)
        
        # Generate final recommendations
        evaluations['final_recommendation'] = self.generate_final_recommendation(evaluations, row)
        evaluations['priority_level'] = self.calculate_priority_level(evaluations)
        evaluations['expected_impact'] = self.calculate_expected_impact(evaluations, row)
        evaluations['implementation_timeline'] = self.determine_timeline(evaluations)
        
        return evaluations
    
    def evaluate_growth_index(self, row: pd.Series) -> Dict[str, Any]:
        """Evaluate growth index metrics"""
        growth_index = row.get('growth_index', 0)
        
        if growth_index >= self.thresholds['growth_index_high']:
            return {
                'category': 'High Growth',
                'score': 5,
                'message': 'Exceptional growth potential',
                'confidence': 'High',
                'threshold_met': True
            }
        elif growth_index >= self.thresholds['growth_index_medium']:
            return {
                'category': 'Moderate Growth',
                'score': 3,
                'message': 'Steady growth observed',
                'confidence': 'Medium',
                'threshold_met': True
            }
        else:
            return {
                'category': 'Low Growth',
                'score': 1,
                'message': 'Limited growth potential',
                'confidence': 'Low',
                'threshold_met': False
            }
    
    def evaluate_volume(self, row: pd.Series) -> Dict[str, Any]:
        """Evaluate volume/scale metrics"""
        volume_index = row.get('volume_index', 0)
        
        if volume_index >= self.thresholds['volume_high']:
            return {
                'category': 'High Volume',
                'score': 5,
                'message': 'Large market size with significant demand',
                'confidence': 'High',
                'threshold_met': True
            }
        elif volume_index >= self.thresholds['volume_medium']:
            return {
                'category': 'Medium Volume',
                'score': 3,
                'message': 'Moderate market size',
                'confidence': 'Medium',
                'threshold_met': True
            }
        else:
            return {
                'category': 'Low Volume',
                'score': 1,
                'message': 'Small market size',
                'confidence': 'Low',
                'threshold_met': False
            }
    
    def evaluate_growth_rate(self, row: pd.Series) -> Dict[str, Any]:
        """Evaluate growth rate metrics"""
        growth_rate = row.get('recent_ride_growth_rate', 0)
        
        if growth_rate >= self.thresholds['growth_rate_high']:
            return {
                'category': 'High Growth Rate',
                'score': 5,
                'message': f'Rapid growth at {growth_rate:.1f}%',
                'confidence': 'High',
                'threshold_met': True
            }
        elif growth_rate >= self.thresholds['growth_rate_medium']:
            return {
                'category': 'Moderate Growth Rate',
                'score': 3,
                'message': f'Steady growth at {growth_rate:.1f}%',
                'confidence': 'Medium',
                'threshold_met': True
            }
        elif growth_rate > 0:
            return {
                'category': 'Low Growth Rate',
                'score': 2,
                'message': f'Minimal growth at {growth_rate:.1f}%',
                'confidence': 'Low',
                'threshold_met': True
            }
        else:
            return {
                'category': 'Negative Growth',
                'score': 0,
                'message': f'Declining at {abs(growth_rate):.1f}%',
                'confidence': 'Medium',
                'threshold_met': False
            }
    
    def evaluate_market_share(self, row: pd.Series) -> Dict[str, Any]:
        """Evaluate market share metrics"""
        market_share = row.get('market_share_percent', 0)
        
        if market_share >= self.thresholds['market_share_high']:
            return {
                'category': 'Market Leader',
                'score': 5,
                'message': f'Strong market position ({market_share:.1f}% share)',
                'confidence': 'High',
                'threshold_met': True
            }
        elif market_share >= self.thresholds['market_share_medium']:
            return {
                'category': 'Significant Player',
                'score': 3,
                'message': f'Substantial market presence ({market_share:.1f}% share)',
                'confidence': 'Medium',
                'threshold_met': True
            }
        else:
            return {
                'category': 'Small Player',
                'score': 1,
                'message': f'Limited market presence ({market_share:.1f}% share)',
                'confidence': 'Low',
                'threshold_met': False
            }
    
    def evaluate_revenue(self, row: pd.Series) -> Dict[str, Any]:
        """Evaluate revenue metrics"""
        revenue = row.get('total_revenue', 0)
        
        if revenue >= self.thresholds['revenue_high']:
            return {
                'category': 'High Revenue',
                'score': 5,
                'message': f'High revenue zone (₹{revenue:,.0f})',
                'confidence': 'High',
                'threshold_met': True
            }
        elif revenue >= self.thresholds['revenue_medium']:
            return {
                'category': 'Medium Revenue',
                'score': 3,
                'message': f'Moderate revenue zone (₹{revenue:,.0f})',
                'confidence': 'Medium',
                'threshold_met': True
            }
        else:
            return {
                'category': 'Low Revenue',
                'score': 1,
                'message': f'Low revenue zone (₹{revenue:,.0f})',
                'confidence': 'Low',
                'threshold_met': False
            }
    
    def evaluate_competition(self, row: pd.Series) -> Dict[str, Any]:
        """Evaluate competition metrics"""
        competition = row.get('competitor_density', 0.5)  # Default to medium
        
        if isinstance(competition, str):
            if 'low' in competition.lower():
                competition_score = 0.2
            elif 'high' in competition.lower():
                competition_score = 0.8
            else:
                competition_score = 0.5
        else:
            competition_score = competition
        
        if competition_score <= self.thresholds['competition_low']:
            return {
                'category': 'Low Competition',
                'score': 5,
                'message': 'Favorable competitive landscape',
                'confidence': 'High',
                'threshold_met': True
            }
        elif competition_score >= self.thresholds['competition_high']:
            return {
                'category': 'High Competition',
                'score': 1,
                'message': 'Highly competitive market',
                'confidence': 'High',
                'threshold_met': False
            }
        else:
            return {
                'category': 'Medium Competition',
                'score': 3,
                'message': 'Moderate competition',
                'confidence': 'Medium',
                'threshold_met': True
            }
    
    def assess_risk(self, row: pd.Series) -> Dict[str, Any]:
        """Assess investment risk"""
        risk_factors = []
        risk_score = 0
        
        # Growth volatility risk
        volatility = row.get('ride_growth_volatility', 0)
        if volatility > self.thresholds['volatility_high']:
            risk_factors.append(f'High growth volatility ({volatility:.1f}%)')
            risk_score += 3
        
        # Consistency risk
        consistency = row.get('growth_consistency', 0.5)
        if consistency < 0.3:
            risk_factors.append(f'Low growth consistency ({consistency:.2f})')
            risk_score += 2
        elif consistency > self.thresholds['consistency_high']:
            risk_score -= 1  # Lower risk for high consistency
        
        # Negative growth risk
        if row.get('recent_ride_growth_rate', 0) < 0:
            risk_factors.append('Negative recent growth')
            risk_score += 2
        
        # Small market share risk
        if row.get('market_share_percent', 0) < 5:
            risk_factors.append('Low market share')
            risk_score += 1
        
        # Determine overall risk level
        if risk_score >= 4:
            risk_level = 'High Risk'
        elif risk_score >= 2:
            risk_level = 'Medium Risk'
        else:
            risk_level = 'Low Risk'
        
        return {
            'risk_level': risk_level,
            'risk_score': risk_score,
            'risk_factors': risk_factors,
            'message': f'{risk_level} with {len(risk_factors)} major risk factors'
        }
    
    def evaluate_seasonality(self, row: pd.Series) -> Dict[str, Any]:
        """Evaluate seasonality patterns"""
        # This would typically use seasonality analysis results
        # For now, using available columns
        seasonality_score = row.get('seasonality_score', 0.5)
        
        if seasonality_score > 0.7:
            return {
                'category': 'High Seasonality',
                'score': 4,
                'message': 'Strong seasonal patterns detected',
                'confidence': 'High',
                'threshold_met': True
            }
        elif seasonality_score > 0.3:
            return {
                'category': 'Moderate Seasonality',
                'score': 2,
                'message': 'Some seasonal variation',
                'confidence': 'Medium',
                'threshold_met': True
            }
        else:
            return {
                'category': 'Low Seasonality',
                'score': 1,
                'message': 'Stable demand throughout year',
                'confidence': 'High',
                'threshold_met': False
            }
    
    def evaluate_distance(self, row: pd.Series) -> Dict[str, Any]:
        """Evaluate distance patterns"""
        avg_distance = row.get('avg_ride_distance', 0)
        
        if avg_distance >= self.thresholds['distance_long']:
            return {
                'category': 'Long Distance',
                'score': 4,
                'message': f'Long average trip distance ({avg_distance:.1f} km)',
                'confidence': 'High',
                'threshold_met': True
            }
        elif avg_distance <= self.thresholds['distance_short']:
            return {
                'category': 'Short Distance',
                'score': 3,
                'message': f'Short average trip distance ({avg_distance:.1f} km)',
                'confidence': 'High',
                'threshold_met': True
            }
        else:
            return {
                'category': 'Medium Distance',
                'score': 2,
                'message': f'Average trip distance ({avg_distance:.1f} km)',
                'confidence': 'Medium',
                'threshold_met': False
            }
    
    def evaluate_time_patterns(self, row: pd.Series) -> Dict[str, Any]:
        """Evaluate time-based patterns"""
        peak_hour = row.get('peak_hour_demand', 1.0)
        
        if peak_hour > 1.5:
            return {
                'category': 'High Peak Demand',
                'score': 4,
                'message': f'Significant peak hour demand ({peak_hour:.1f}x average)',
                'confidence': 'High',
                'threshold_met': True
            }
        elif peak_hour > 1.2:
            return {
                'category': 'Moderate Peak Demand',
                'score': 2,
                'message': f'Some peak hour concentration ({peak_hour:.1f}x average)',
                'confidence': 'Medium',
                'threshold_met': True
            }
        else:
            return {
                'category': 'Even Demand',
                'score': 1,
                'message': 'Relatively even demand distribution',
                'confidence': 'Medium',
                'threshold_met': False
            }
    
    def generate_final_recommendation(self, evaluations: Dict[str, Any], row: pd.Series) -> Dict[str, Any]:
        """Generate final recommendation based on all evaluations"""
        # Calculate overall score
        scores = [
            evaluations['growth_index_evaluation']['score'],
            evaluations['volume_evaluation']['score'],
            evaluations['growth_rate_evaluation']['score'],
            evaluations['market_share_evaluation']['score'],
            evaluations['revenue_evaluation']['score'],
            evaluations['competition_evaluation']['score'],
        ]
        
        overall_score = sum(scores) / len(scores)
        
        # Get risk level
        risk_level = evaluations['risk_assessment']['risk_level']
        
        # Generate recommendation based on score and risk
        if overall_score >= 4 and risk_level == 'Low Risk':
            recommendation = "AGGRESSIVE EXPANSION - High potential with low risk"
            action_items = [
                "Increase driver allocation by 30%",
                "Implement marketing campaigns",
                "Consider premium service options",
                "Monitor competition closely"
            ]
        elif overall_score >= 3.5:
            if risk_level == 'Low Risk':
                recommendation = "MODERATE EXPANSION - Good potential with manageable risk"
                action_items = [
                    "Increase driver allocation by 15-20%",
                    "Run targeted promotions",
                    "Improve service quality",
                    "Expand service hours"
                ]
            else:
                recommendation = "CAUTIOUS EXPANSION - Good potential but higher risk"
                action_items = [
                    "Gradual driver increase (10%)",
                    "Test new services in limited capacity",
                    "Focus on risk mitigation",
                    "Close performance monitoring"
                ]
        elif overall_score >= 2.5:
            recommendation = "MAINTENANCE & OPTIMIZATION - Focus on efficiency"
            action_items = [
                "Maintain current operations",
                "Optimize existing processes",
                "Improve customer experience",
                "Reduce operational costs"
            ]
        else:
            recommendation = "MONITOR & RESEARCH - Limited immediate potential"
            action_items = [
                "Continue monitoring market trends",
                "Research competitor strategies",
                "Identify niche opportunities",
                "Prepare contingency plans"
            ]
        
        # Add specific recommendations based on evaluations
        specific_recommendations = []
        
        if evaluations['growth_rate_evaluation']['category'] == 'High Growth Rate':
            specific_recommendations.append("Capitalize on rapid growth momentum")
        
        if evaluations['competition_evaluation']['category'] == 'Low Competition':
            specific_recommendations.append("Leverage competitive advantage")
        
        if evaluations['distance_evaluation']['category'] == 'Long Distance':
            specific_recommendations.append("Consider long-distance service optimization")
        
        if evaluations['time_pattern_evaluation']['category'] == 'High Peak Demand':
            specific_recommendations.append("Implement surge pricing during peak hours")
        
        return {
            'overall_score': overall_score,
            'recommendation': recommendation,
            'action_items': action_items,
            'specific_recommendations': specific_recommendations,
            'risk_level': risk_level,
            'summary': f"Overall score: {overall_score:.2f}/5.0, Risk: {risk_level}"
        }
    
    def calculate_priority_level(self, evaluations: Dict[str, Any]) -> str:
        """Calculate priority level based on evaluations"""
        overall_score = evaluations['final_recommendation']['overall_score']
        risk_level = evaluations['final_recommendation']['risk_level']
        
        if overall_score >= 4 and risk_level == 'Low Risk':
            return "Critical Priority"
        elif overall_score >= 3.5:
            return "High Priority"
        elif overall_score >= 3:
            return "Medium-High Priority"
        elif overall_score >= 2.5:
            return "Medium Priority"
        elif overall_score >= 2:
            return "Low-Medium Priority"
        else:
            return "Low Priority"
    
    def calculate_expected_impact(self, evaluations: Dict[str, Any], row: pd.Series) -> Dict[str, Any]:
        """Calculate expected impact of following recommendations"""
        overall_score = evaluations['final_recommendation']['overall_score']
        revenue = row.get('total_revenue', 100000)
        
        # Estimate impact based on overall score
        if overall_score >= 4:
            revenue_increase = 0.30  # 30%
            market_share_increase = 0.15  # 15%
            timeline = "3-6 months"
        elif overall_score >= 3.5:
            revenue_increase = 0.20  # 20%
            market_share_increase = 0.10  # 10%
            timeline = "6-9 months"
        elif overall_score >= 3:
            revenue_increase = 0.10  # 10%
            market_share_increase = 0.05  # 5%
            timeline = "9-12 months"
        else:
            revenue_increase = 0.05  # 5%
            market_share_increase = 0.02  # 2%
            timeline = "12+ months"
        
        estimated_new_revenue = revenue * (1 + revenue_increase)
        
        return {
            'estimated_revenue_increase_percent': revenue_increase * 100,
            'estimated_market_share_increase_percent': market_share_increase * 100,
            'estimated_new_revenue': estimated_new_revenue,
            'timeline_for_impact': timeline,
            'confidence': 'High' if overall_score >= 3.5 else 'Medium'
        }
    
    def determine_timeline(self, evaluations: Dict[str, Any]) -> Dict[str, Any]:
        """Determine implementation timeline"""
        priority = evaluations['priority_level']
        risk = evaluations['final_recommendation']['risk_level']
        
        if priority in ['Critical Priority', 'High Priority'] and risk == 'Low Risk':
            return {
                'start': 'Immediate',
                'duration': '1-3 months',
                'phase': 'Rapid Implementation',
                'milestones': ['Planning', 'Resource Allocation', 'Execution', 'Review']
            }
        elif priority in ['High Priority', 'Medium-High Priority']:
            return {
                'start': 'Within 1 month',
                'duration': '3-6 months',
                'phase': 'Strategic Implementation',
                'milestones': ['Feasibility Study', 'Planning', 'Pilot', 'Full Rollout']
            }
        elif priority == 'Medium Priority':
            return {
                'start': 'Within 3 months',
                'duration': '6-12 months',
                'phase': 'Gradual Implementation',
                'milestones': ['Research', 'Planning', 'Phased Implementation', 'Evaluation']
            }
        else:
            return {
                'start': 'When resources permit',
                'duration': '12+ months',
                'phase': 'Long-term Planning',
                'milestones': ['Continuous Monitoring', 'Opportunity Assessment', 'Resource Planning']
            }

def opportunity_rules(row, rules_engine=None):
    """
    Main function to apply opportunity rules (backward compatible)
    
    Parameters:
    row: pandas Series containing zone data
    rules_engine: Optional OpportunityRules instance
    
    Returns:
    Dictionary or string with recommendations
    """
    if rules_engine is None:
        rules_engine = OpportunityRules()
    
    # Apply all rules
    result = rules_engine.apply_rules(row)
    
    # For backward compatibility, also return a simple string
    simple_recommendation = result['final_recommendation']['recommendation']
    
    return {
        'detailed_analysis': result,
        'simple_recommendation': simple_recommendation,
        'priority': result['priority_level'],
        'expected_impact': result['expected_impact']
    }

def process_dataframe(df, rules_engine=None):
    """
    Process entire dataframe with opportunity rules
    
    Parameters:
    df: pandas DataFrame containing zone data
    rules_engine: Optional OpportunityRules instance
    
    Returns:
    DataFrame with added opportunity analysis columns
    """
    if rules_engine is None:
        rules_engine = OpportunityRules()
    
    results = []
    
    for idx, row in df.iterrows():
        analysis = opportunity_rules(row, rules_engine)
        
        # Extract key information for DataFrame
        result_row = {
            'zone': row.get('zone', f'Zone_{idx}'),
            'simple_recommendation': analysis['simple_recommendation'],
            'priority': analysis['priority'],
            'overall_score': analysis['detailed_analysis']['final_recommendation']['overall_score'],
            'risk_level': analysis['detailed_analysis']['final_recommendation']['risk_level'],
            'growth_index_category': analysis['detailed_analysis']['growth_index_evaluation']['category'],
            'volume_category': analysis['detailed_analysis']['volume_evaluation']['category'],
            'growth_rate_category': analysis['detailed_analysis']['growth_rate_evaluation']['category'],
            'competition_category': analysis['detailed_analysis']['competition_evaluation']['category'],
            'expected_revenue_increase_percent': analysis['expected_impact']['estimated_revenue_increase_percent'],
            'implementation_timeline': analysis['detailed_analysis']['implementation_timeline']['phase'],
            'detailed_analysis': str(analysis['detailed_analysis'])  # Store as string for reference
        }
        
        results.append(result_row)
    
    return pd.DataFrame(results)

# For backward compatibility
def simple_opportunity_rules(row):
    """Simple version for backward compatibility"""
    if 'growth_index' in row:
        if row['growth_index'] > 0.7:
            return "High expansion priority"
        elif row['growth_index'] > 0.4:
            return "Moderate growth zone"
        else:
            return "Low demand zone"
    else:
        return "Insufficient data"

def main():
    """
    Example usage and testing
    """
    # Example data
    example_data = {
        'zone': ['Zone_A', 'Zone_B', 'Zone_C'],
        'growth_index': [0.85, 0.55, 0.35],
        'volume_index': [0.8, 0.6, 0.3],
        'recent_ride_growth_rate': [20, 8, -5],
        'total_revenue': [1200000, 600000, 200000],
        'market_share_percent': [18, 8, 3],
        'competitor_density': [0.2, 0.5, 0.8]
    }
    
    df = pd.DataFrame(example_data)
    
    # Process with comprehensive rules
    print("Processing with comprehensive rules:")
    rules_engine = OpportunityRules()
    processed_df = process_dataframe(df, rules_engine)
    
    print("\nResults:")
    print(processed_df[['zone', 'simple_recommendation', 'priority', 'overall_score']])
    
    # Individual row example
    print("\n\nDetailed analysis for Zone_A:")
    zone_a_analysis = opportunity_rules(df.iloc[0], rules_engine)
    print(f"Recommendation: {zone_a_analysis['simple_recommendation']}")
    print(f"Priority: {zone_a_analysis['priority']}")
    print(f"Expected Revenue Increase: {zone_a_analysis['expected_impact']['estimated_revenue_increase_percent']:.1f}%")

if __name__ == "__main__":
    main()
