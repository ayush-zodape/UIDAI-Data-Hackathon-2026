import pandas as pd
from fastapi import HTTPException

def validate_csv_schema(df: pd.DataFrame, required_columns: list, file_type: str):
    """
    Validate that CSV has required columns
    """
    missing_cols = [col for col in required_columns if col not in df.columns]
    
    if missing_cols:
        raise HTTPException(
            status_code=400,
            detail=f"{file_type} CSV missing required columns: {missing_cols}. "
                   f"Found columns: {list(df.columns)}"
        )
    
    # Check for empty dataframe
    if df.empty:
        raise HTTPException(
            status_code=400,
            detail=f"{file_type} CSV is empty"
        )
    
    return True
