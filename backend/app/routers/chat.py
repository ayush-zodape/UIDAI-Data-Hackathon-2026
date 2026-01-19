from fastapi import APIRouter, HTTPException
from app.models.schemas import ChatRequest, ChatResponse
from app.services.llm_service import LLMService
from app.routers.upload import uploaded_data

router = APIRouter()

@router.post("/ask", response_model=ChatResponse)
async def ask_question(request: ChatRequest):
    """
    AI Chatbot endpoint - answers questions about the uploaded data
    """
    if 'enrollment' not in uploaded_data or 'biometric' not in uploaded_data:
        raise HTTPException(
            status_code=400, 
            detail="Please upload data files first before asking questions"
        )
    
    llm_service = LLMService(
        df_enrollment=uploaded_data['enrollment'],
        df_biometric=uploaded_data['biometric']
    )
    
    response = await llm_service.answer_question(request.message)
    return response
