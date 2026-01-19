from fastapi import APIRouter, HTTPException
from app.services.data_processor import BLIProcessor
from app.models.schemas import AnalysisResponse, GapWideningData
from app.routers.upload import uploaded_data

router = APIRouter()

@router.get("/compute-bli", response_model=AnalysisResponse)
async def compute_biometric_lag_index():
    """
    Main endpoint: Compute BLI for all districts
    """
    if 'enrollment' not in uploaded_data or 'biometric' not in uploaded_data:
        raise HTTPException(status_code=400, detail="Please upload CSV files first")
    
    processor = BLIProcessor(
        df_enrollment=uploaded_data['enrollment'],
        df_biometric=uploaded_data['biometric']
    )
    
    result = processor.compute_district_bli()
    return result

@router.get("/gap-widening/{district}", response_model=GapWideningData)
async def get_gap_widening_curve(district: str):
    """
    Get time-series data for the Gap Widening Curve visualization
    """
    if 'enrollment' not in uploaded_data or 'biometric' not in uploaded_data:
        raise HTTPException(status_code=400, detail="Please upload CSV files first")
    
    processor = BLIProcessor(
        df_enrollment=uploaded_data['enrollment'],
        df_biometric=uploaded_data['biometric']
    )
    
    result = processor.get_gap_widening_data(district)
    if result is None:
        raise HTTPException(status_code=404, detail=f"District '{district}' not found")
    
    return result

@router.get("/seasonality")
async def get_seasonality_data():
    """
    Get monthly aggregated data for seasonality heatmap
    """
    if 'biometric' not in uploaded_data:
        raise HTTPException(status_code=400, detail="Please upload CSV files first")
    
    processor = BLIProcessor(
        df_enrollment=uploaded_data.get('enrollment'),
        df_biometric=uploaded_data['biometric']
    )
    
    return processor.get_seasonality_data()

@router.get("/state-summary")
async def get_state_summary():
    """
    Get state-level BLI aggregation
    """
    if 'enrollment' not in uploaded_data or 'biometric' not in uploaded_data:
        raise HTTPException(status_code=400, detail="Please upload CSV files first")
    
    processor = BLIProcessor(
        df_enrollment=uploaded_data['enrollment'],
        df_biometric=uploaded_data['biometric']
    )
    
    return processor.get_state_summary()
