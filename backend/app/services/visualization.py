# Visualization service placeholder
# Chart data preparation is handled in data_processor.py
# This file can be extended for additional visualization utilities

from typing import Dict, Any, List
import pandas as pd

class VisualizationService:
    """
    Service for preparing data for various visualizations.
    Currently, most visualization data is generated in BLIProcessor.
    This service can be extended for additional chart types.
    """
    
    @staticmethod
    def prepare_heatmap_data(df: pd.DataFrame, value_column: str) -> List[Dict[str, Any]]:
        """
        Prepare data for a heatmap visualization.
        """
        if df.empty:
            return []
        
        return df.to_dict('records')
    
    @staticmethod
    def prepare_pie_chart_data(districts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Prepare data for risk level distribution pie chart.
        """
        risk_counts = {"Low": 0, "Medium": 0, "High": 0, "Critical": 0}
        
        for district in districts:
            risk_level = district.get('risk_level', 'Low')
            if risk_level in risk_counts:
                risk_counts[risk_level] += 1
        
        return {
            "data": [
                {"name": "Low Risk", "value": risk_counts["Low"], "color": "#22c55e"},
                {"name": "Medium Risk", "value": risk_counts["Medium"], "color": "#eab308"},
                {"name": "High Risk", "value": risk_counts["High"], "color": "#f97316"},
                {"name": "Critical Risk", "value": risk_counts["Critical"], "color": "#ef4444"},
            ],
            "total": sum(risk_counts.values())
        }
