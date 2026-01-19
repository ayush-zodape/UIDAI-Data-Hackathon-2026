from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
import pandas as pd
import io
from app.utils.validators import validate_csv_schema

router = APIRouter()

# In-memory storage (for prototype - use Redis/DB in production)
uploaded_data = {}

@router.post("/files")
async def upload_csv_files(
    enrollment: UploadFile = File(..., description="Enrollment CSV"),
    biometric: UploadFile = File(..., description="Biometric Updates CSV"),
    demographic: UploadFile = File(None, description="Demographic Updates CSV (optional)")
):
    """
    Upload the required CSV files for analysis.
    """
    try:
        # Read enrollment data
        enrollment_content = await enrollment.read()
        df_enrollment = pd.read_csv(
            io.StringIO(enrollment_content.decode('utf-8')),
            dtype={'pincode': str}
        )
        df_enrollment.columns = df_enrollment.columns.str.strip()
        
        # Validate schema
        required_enrollment_cols = ['date', 'state', 'district', 'pincode', 'age_5_17']
        validate_csv_schema(df_enrollment, required_enrollment_cols, "Enrollment")
        
        # Read biometric data
        biometric_content = await biometric.read()
        df_biometric = pd.read_csv(
            io.StringIO(biometric_content.decode('utf-8')),
            dtype={'pincode': str}
        )
        df_biometric.columns = df_biometric.columns.str.strip()
        
        required_bio_cols = ['date', 'state', 'district', 'pincode', 'bio_age_5_17']
        validate_csv_schema(df_biometric, required_bio_cols, "Biometric")
        
        # Parse dates (Indian format)
        df_enrollment['date'] = pd.to_datetime(df_enrollment['date'], dayfirst=True)
        df_biometric['date'] = pd.to_datetime(df_biometric['date'], dayfirst=True)
        
        # Store in memory
        uploaded_data['enrollment'] = df_enrollment
        uploaded_data['biometric'] = df_biometric
        
        # Optional demographic data
        if demographic:
            demo_content = await demographic.read()
            df_demographic = pd.read_csv(
                io.StringIO(demo_content.decode('utf-8')),
                dtype={'pincode': str}
            )
            df_demographic.columns = df_demographic.columns.str.strip()
            df_demographic['date'] = pd.to_datetime(df_demographic['date'], dayfirst=True)
            uploaded_data['demographic'] = df_demographic
        
        return {
            "success": True,
            "message": "Files uploaded successfully",
            "enrollment_rows": len(df_enrollment),
            "biometric_rows": len(df_biometric),
            "columns_detected": {
                "enrollment": list(df_enrollment.columns),
                "biometric": list(df_biometric.columns)
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/status")
async def get_upload_status():
    """Check if data has been uploaded"""
    return {
        "enrollment_loaded": 'enrollment' in uploaded_data,
        "biometric_loaded": 'biometric' in uploaded_data,
        "demographic_loaded": 'demographic' in uploaded_data,
        "ready_for_analysis": 'enrollment' in uploaded_data and 'biometric' in uploaded_data
    }
