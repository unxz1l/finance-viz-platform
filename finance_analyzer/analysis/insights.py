"""
Financial insights generation module.

This module provides functions for generating insights from financial indicators
and helping users understand financial performance trends.
"""

from typing import Dict, List, Any, Union
import pandas as pd


class InsightGenerator:
    """Class for generating insights from financial data and indicators."""
    
    @staticmethod
    def generate_roe_insights(current_roe: float, previous_roe: float) -> List[str]:
        """
        Generate insights about ROE trends.
        
        Parameters
        ----------
        current_roe : float
            Current period ROE
        previous_roe : float
            Previous period ROE
            
        Returns
        -------
        List[str]
            List of insights about ROE
        """
        insights = []
        
        # Calculate change
        change = current_roe - previous_roe
        percent_change = (change / abs(previous_roe)) * 100 if previous_roe != 0 else float('inf')
        
        # Generate insights
        if change > 0:
            insights.append(f"ROE上升了{abs(change):.2f}個百分點 (增加{abs(percent_change):.1f}%)，表示公司資金運用效率提升。")
            
            if current_roe > 15:
                insights.append("ROE高於15%，屬於良好的資本回報率。")
        elif change < 0:
            insights.append(f"ROE下降了{abs(change):.2f}個百分點 (減少{abs(percent_change):.1f}%)，表示公司資金運用效率下降。")
            
            if current_roe < 5:
                insights.append("ROE低於5%，可能需關注公司獲利能力。")
        else:
            insights.append("ROE維持不變，資金運用效率穩定。")
            
        return insights
    
    @staticmethod
    def generate_rd_insights(current_rd: float, previous_rd: float, revenue: float) -> List[str]:
        """
        Generate insights about R&D expense trends.
        
        Parameters
        ----------
        current_rd : float
            Current period R&D expense
        previous_rd : float
            Previous period R&D expense
        revenue : float
            Current period revenue
            
        Returns
        -------
        List[str]
            List of insights about R&D
        """
        insights = []
        
        # Calculate change
        change = current_rd - previous_rd
        percent_change = (change / previous_rd) * 100 if previous_rd != 0 else float('inf')
        rd_to_revenue = (current_rd / revenue) * 100 if revenue != 0 else 0
        
        # Generate insights
        if change > 0:
            insights.append(f"研發支出增加{abs(percent_change):.1f}%，表示公司增加未來競爭力投資。")
            
            if rd_to_revenue > 10:
                insights.append(f"研發費用佔營收{rd_to_revenue:.1f}%，高於產業平均，表示積極投入創新。")
        elif change < 0:
            insights.append(f"研發支出減少{abs(percent_change):.1f}%，可能影響未來競爭力。")
        else:
            insights.append("研發支出維持不變。")
            
        return insights
    
    @staticmethod
    def generate_debt_insights(debt_ratio: float, previous_debt_ratio: float) -> List[str]:
        """
        Generate insights about debt ratio trends.
        
        Parameters
        ----------
        debt_ratio : float
            Current period debt ratio
        previous_debt_ratio : float
            Previous period debt ratio
            
        Returns
        -------
        List[str]
            List of insights about debt
        """
        insights = []
        
        # Calculate change
        change = debt_ratio - previous_debt_ratio
        
        # Generate insights
        if change > 5:
            insights.append(f"負債比率上升{abs(change):.1f}個百分點，財務槓桿增加。")
            
            if debt_ratio > 70:
                insights.append("負債比率高於70%，財務風險增加。")
        elif change < -5:
            insights.append(f"負債比率下降{abs(change):.1f}個百分點，財務結構改善。")
        else:
            insights.append("負債結構相對穩定。")
            
        return insights
    
    @staticmethod
    def generate_profit_margin_insights(current_margin: float, previous_margin: float) -> List[str]:
        """
        Generate insights about profit margin trends.
        
        Parameters
        ----------
        current_margin : float
            Current period profit margin
        previous_margin : float
            Previous period profit margin
            
        Returns
        -------
        List[str]
            List of insights about profit margin
        """
        insights = []
        
        # Calculate change
        change = current_margin - previous_margin
        
        # Generate insights
        if change > 2:
            insights.append(f"淨利率上升{abs(change):.1f}個百分點，營運效率或產品定價能力提升。")
        elif change < -2:
            insights.append(f"淨利率下降{abs(change):.1f}個百分點，可能面臨成本壓力或競爭加劇。")
        else:
            insights.append("淨利率相對穩定。")
            
        return insights


def generate_comprehensive_insights(current_data: Dict[str, Any], 
                                   previous_data: Dict[str, Any]) -> List[str]:
    """
    Generate comprehensive insights by analyzing multiple financial indicators.
    
    Parameters
    ----------
    current_data : Dict[str, Any]
        Current period financial data and indicators
    previous_data : Dict[str, Any]
        Previous period financial data and indicators
        
    Returns
    -------
    List[str]
        List of comprehensive insights
    """
    generator = InsightGenerator()
    insights = []
    
    # Generate ROE insights
    if "ROE" in current_data and "ROE" in previous_data:
        roe_insights = generator.generate_roe_insights(
            current_data["ROE"], previous_data["ROE"]
        )
        insights.extend(roe_insights)
    
    # Generate R&D insights
    if ("R&D Expense" in current_data and "R&D Expense" in previous_data 
            and "Revenue" in current_data):
        rd_insights = generator.generate_rd_insights(
            current_data["R&D Expense"], 
            previous_data["R&D Expense"],
            current_data["Revenue"]
        )
        insights.extend(rd_insights)
    
    # Generate debt insights
    if "Debt Ratio" in current_data and "Debt Ratio" in previous_data:
        debt_insights = generator.generate_debt_insights(
            current_data["Debt Ratio"], previous_data["Debt Ratio"]
        )
        insights.extend(debt_insights)
    
    # Generate profit margin insights
    if "Profit Margin" in current_data and "Profit Margin" in previous_data:
        profit_insights = generator.generate_profit_margin_insights(
            current_data["Profit Margin"], previous_data["Profit Margin"]
        )
        insights.extend(profit_insights)
    
    # Summary insight
    overall_trend = _determine_overall_trend(current_data, previous_data)
    insights.append(overall_trend)
    
    return insights


def _determine_overall_trend(current: Dict[str, Any], previous: Dict[str, Any]) -> str:
    """
    Determine the overall financial trend based on multiple indicators.
    
    Parameters
    ----------
    current : Dict[str, Any]
        Current period indicators
    previous : Dict[str, Any]
        Previous period indicators
        
    Returns
    -------
    str
        Overall trend summary
    """
    # Count improvements
    improvements = 0
    total_indicators = 0
    
    key_indicators = ["ROE", "Profit Margin", "Revenue Growth"]
    
    for indicator in key_indicators:
        if indicator in current and indicator in previous:
            total_indicators += 1
            if current[indicator] > previous[indicator]:
                improvements += 1
    
    # Generate summary
    if total_indicators == 0:
        return "資料不足，無法評估整體趨勢。"
    
    improvement_ratio = improvements / total_indicators
    
    if improvement_ratio > 0.7:
        return "整體財務表現顯著改善，多數指標呈現正向發展。"
    elif improvement_ratio > 0.3:
        return "整體財務表現有所改善，但仍有部分指標需要關注。"
    else:
        return "整體財務表現面臨挑戰，多數指標呈現下滑趨勢。"


if __name__ == "__main__":
    # Example usage
    current_data = {
        "ROE": 15.5,
        "R&D Expense": 120,
        "Revenue": 1000,
        "Debt Ratio": 45,
        "Profit Margin": 12
    }
    
    previous_data = {
        "ROE": 14.2,
        "R&D Expense": 100,
        "Revenue": 900,
        "Debt Ratio": 48,
        "Profit Margin": 10.5
    }
    
    insights = generate_comprehensive_insights(current_data, previous_data)
    
    print("=== Financial Insights ===")
    for i, insight in enumerate(insights, 1):
        print(f"{i}. {insight}")