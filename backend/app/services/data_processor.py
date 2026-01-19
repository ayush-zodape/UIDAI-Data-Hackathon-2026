import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
from app.models.schemas import DistrictBLI, AnalysisResponse, GapWideningData, TimeSeriesPoint

class BLIProcessor:
    """
    Core processor for Biometric Lag Index calculations.
    DO NOT MODIFY THE METHODOLOGY.
    """
    
    def __init__(self, df_enrollment: pd.DataFrame, df_biometric: pd.DataFrame):
        self.df_enrollment = df_enrollment.copy()
        self.df_biometric = df_biometric.copy()
        self.df_merged = None
        self._merge_datasets()
    
    def _merge_datasets(self):
        """Merge enrollment and biometric data on location and date"""
        merge_keys = ['date', 'state', 'district', 'pincode']
        
        self.df_merged = pd.merge(
            self.df_enrollment,
            self.df_biometric,
            on=merge_keys,
            how='outer',
            suffixes=('_enr', '_bio')
        )
        
        # Fill NaN with 0 for numeric columns
        numeric_cols = self.df_merged.select_dtypes(include=[np.number]).columns
        self.df_merged[numeric_cols] = self.df_merged[numeric_cols].fillna(0)
        
        # Calculate the child update gap
        self.df_merged['child_update_gap'] = (
            self.df_merged['age_5_17'] - self.df_merged['bio_age_5_17']
        )
    
    def _get_risk_level(self, bli: float) -> tuple:
        """Determine risk level and color code from BLI score"""
        if bli < 0.1:
            return "Low", "#22c55e"
        elif bli < 0.3:
            return "Medium", "#eab308"
        elif bli < 0.5:
            return "High", "#f97316"
        else:
            return "Critical", "#ef4444"
    
    def compute_district_bli(self) -> AnalysisResponse:
        """
        Main computation: Calculate BLI for each district
        
        Formula: BLI = (Enrollments - Updates) / Enrollments
        """
        # Group by district
        district_summary = self.df_merged.groupby(['state', 'district']).agg({
            'age_5_17': 'sum',
            'bio_age_5_17': 'sum',
            'child_update_gap': 'sum'
        }).reset_index()
        
        # Calculate BLI (add epsilon to avoid division by zero)
        district_summary['bli_score'] = (
            district_summary['child_update_gap'] / 
            (district_summary['age_5_17'] + 1e-6)
        )
        
        # Add risk levels
        district_summary[['risk_level', 'color_code']] = district_summary['bli_score'].apply(
            lambda x: pd.Series(self._get_risk_level(x))
        )
        
        # Sort by BLI (descending) to get problem districts first
        district_summary = district_summary.sort_values('bli_score', ascending=False)
        
        # Create response objects
        top_districts = []
        for _, row in district_summary.head(10).iterrows():
            top_districts.append(DistrictBLI(
                state=row['state'],
                district=row['district'],
                total_enrollments=int(row['age_5_17']),
                total_updates=int(row['bio_age_5_17']),
                child_update_gap=int(row['child_update_gap']),
                bli_score=round(row['bli_score'], 4),
                risk_level=row['risk_level'],
                color_code=row['color_code']
            ))
        
        # Overall BLI
        total_enrollments = district_summary['age_5_17'].sum()
        total_updates = district_summary['bio_age_5_17'].sum()
        overall_bli = (total_enrollments - total_updates) / (total_enrollments + 1e-6)
        
        # Date range
        min_date = self.df_merged['date'].min()
        max_date = self.df_merged['date'].max()
        
        # State summary
        state_summary = self.df_merged.groupby('state').agg({
            'age_5_17': 'sum',
            'bio_age_5_17': 'sum',
            'child_update_gap': 'sum'
        }).reset_index()
        state_summary['bli_score'] = (
            state_summary['child_update_gap'] / 
            (state_summary['age_5_17'] + 1e-6)
        )
        
        return AnalysisResponse(
            success=True,
            total_records=len(self.df_merged),
            date_range={
                "start": min_date.strftime('%Y-%m-%d') if pd.notna(min_date) else "N/A",
                "end": max_date.strftime('%Y-%m-%d') if pd.notna(max_date) else "N/A"
            },
            top_problem_districts=top_districts,
            state_summary=state_summary.to_dict('records'),
            overall_bli=round(overall_bli, 4)
        )
    
    def get_gap_widening_data(self, district: str) -> Optional[GapWideningData]:
        """
        Generate time-series data for the Gap Widening Curve
        """
        district_data = self.df_merged[
            self.df_merged['district'].str.lower() == district.lower()
        ].sort_values('date')
        
        if district_data.empty:
            return None
        
        # Get state
        state = district_data['state'].iloc[0]
        
        # Group by date and sum
        daily_data = district_data.groupby('date').agg({
            'age_5_17': 'sum',
            'bio_age_5_17': 'sum'
        }).reset_index()
        
        # Calculate cumulative sums
        daily_data['cum_enrollments'] = daily_data['age_5_17'].cumsum()
        daily_data['cum_updates'] = daily_data['bio_age_5_17'].cumsum()
        daily_data['gap'] = daily_data['cum_enrollments'] - daily_data['cum_updates']
        
        # Create data points
        data_points = []
        for _, row in daily_data.iterrows():
            data_points.append(TimeSeriesPoint(
                date=row['date'].strftime('%Y-%m-%d'),
                cumulative_enrollments=int(row['cum_enrollments']),
                cumulative_updates=int(row['cum_updates']),
                gap=int(row['gap'])
            ))
        
        return GapWideningData(
            district=district,
            state=state,
            data_points=data_points
        )
    
    def get_seasonality_data(self) -> Dict[str, Any]:
        """
        Generate monthly aggregated data for seasonality analysis
        """
        df = self.df_merged.copy()
        df['month'] = df['date'].dt.month
        df['year'] = df['date'].dt.year
        df['month_name'] = df['date'].dt.strftime('%B')
        
        monthly = df.groupby(['year', 'month', 'month_name']).agg({
            'bio_age_5_17': 'sum',
            'age_5_17': 'sum'
        }).reset_index()
        
        monthly['update_rate'] = monthly['bio_age_5_17'] / (monthly['age_5_17'] + 1e-6)
        
        return {
            "monthly_data": monthly.to_dict('records'),
            "peak_month": monthly.loc[monthly['bio_age_5_17'].idxmax(), 'month_name'],
            "low_month": monthly.loc[monthly['bio_age_5_17'].idxmin(), 'month_name']
        }
    
    def get_state_summary(self) -> List[Dict[str, Any]]:
        """Get state-level aggregation for choropleth map"""
        state_data = self.df_merged.groupby('state').agg({
            'age_5_17': 'sum',
            'bio_age_5_17': 'sum',
            'child_update_gap': 'sum'
        }).reset_index()
        
        state_data['bli_score'] = (
            state_data['child_update_gap'] / 
            (state_data['age_5_17'] + 1e-6)
        )
        
        state_data[['risk_level', 'color_code']] = state_data['bli_score'].apply(
            lambda x: pd.Series(self._get_risk_level(x))
        )
        
        return state_data.sort_values('bli_score', ascending=False).to_dict('records')
