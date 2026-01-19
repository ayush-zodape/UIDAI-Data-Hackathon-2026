from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import date

class DistrictBLI(BaseModel):
    state: str
    district: str
    total_enrollments: int
    total_updates: int
    child_update_gap: int
    bli_score: float
    risk_level: str
    color_code: str

class AnalysisResponse(BaseModel):
    success: bool
    total_records: int
    date_range: Dict[str, str]
    top_problem_districts: List[DistrictBLI]
    state_summary: List[Dict[str, Any]]
    overall_bli: float

class TimeSeriesPoint(BaseModel):
    date: str
    cumulative_enrollments: int
    cumulative_updates: int
    gap: int

class GapWideningData(BaseModel):
    district: str
    state: str
    data_points: List[TimeSeriesPoint]

class ChatRequest(BaseModel):
    message: str
    context: Optional[Dict[str, Any]] = None

class ChatResponse(BaseModel):
    response: str
    suggested_questions: List[str]
