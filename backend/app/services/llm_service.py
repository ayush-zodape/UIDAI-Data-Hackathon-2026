import os
from openai import AsyncOpenAI
from typing import Dict, Any
import pandas as pd
from app.models.schemas import ChatResponse
from app.services.data_processor import BLIProcessor

class LLMService:
    """
    Service for handling AI chatbot queries about the data
    """
    
    def __init__(self, df_enrollment: pd.DataFrame, df_biometric: pd.DataFrame):
        self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.processor = BLIProcessor(df_enrollment, df_biometric)
        self._prepare_context()
    
    def _prepare_context(self):
        """Prepare a summary of the data for the LLM"""
        analysis = self.processor.compute_district_bli()
        
        self.data_context = f"""
        You are an AI assistant analyzing UIDAI Aadhaar data for the "Digital Continuity" project.
        
        DATA SUMMARY:
        - Total records analyzed: {analysis.total_records}
        - Date range: {analysis.date_range['start']} to {analysis.date_range['end']}
        - Overall Biometric Lag Index (BLI): {analysis.overall_bli}
        
        TOP 5 PROBLEM DISTRICTS (Highest BLI):
        {self._format_districts(analysis.top_problem_districts[:5])}
        
        BLI FORMULA: (Total Enrollments₅₋₁₇ - Total Biometric Updates₅₋₁₇) / Total Enrollments₅₋₁₇
        
        RISK LEVELS:
        - BLI < 0.1: Low Risk (Green)
        - BLI 0.1-0.3: Medium Risk (Yellow)
        - BLI 0.3-0.5: High Risk (Orange)
        - BLI > 0.5: Critical Risk (Red)
        
        STATE SUMMARY:
        {self._format_states(analysis.state_summary[:10])}
        """
        
        self.analysis = analysis
    
    def _format_districts(self, districts) -> str:
        return "\n".join([
            f"- {d.district}, {d.state}: BLI={d.bli_score}, Gap={d.child_update_gap}, Risk={d.risk_level}"
            for d in districts
        ])
    
    def _format_states(self, states) -> str:
        return "\n".join([
            f"- {s['state']}: BLI={round(s['bli_score'], 4)}"
            for s in states
        ])
    
    async def answer_question(self, question: str) -> ChatResponse:
        """
        Answer a user question about the data using GPT-4
        """
        system_prompt = f"""
        {self.data_context}
        
        INSTRUCTIONS:
        1. Only answer questions based on the data summary provided above
        2. If asked about specific numbers, use the data from the summary
        3. If you don't have the information, say so clearly
        4. Always explain what BLI means when relevant
        5. Suggest actionable insights when possible
        6. Keep responses concise but informative
        """
        
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": question}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            answer = response.choices[0].message.content
            
            # Generate suggested follow-up questions
            suggested = [
                "Which state has the highest BLI?",
                "What does a Critical risk level mean?",
                "Show me the trend for the worst district",
                "What interventions do you recommend?"
            ]
            
            return ChatResponse(
                response=answer,
                suggested_questions=suggested
            )
            
        except Exception as e:
            # Fallback to rule-based responses if OpenAI fails
            return self._fallback_response(question)
    
    def _fallback_response(self, question: str) -> ChatResponse:
        """Fallback responses when LLM is unavailable"""
        question_lower = question.lower()
        
        analysis = self.analysis
        
        if "highest" in question_lower and ("bli" in question_lower or "lag" in question_lower or "district" in question_lower):
            top = analysis.top_problem_districts[0]
            return ChatResponse(
                response=f"The district with the highest BLI is {top.district} in {top.state} with a BLI of {top.bli_score} ({top.risk_level} risk). This means {top.child_update_gap:,} children have enrolled but not yet updated their biometrics.",
                suggested_questions=["Why is this district's BLI so high?", "What is the overall BLI?", "Which districts need immediate intervention?"]
            )
        
        if "what is bli" in question_lower or "biometric lag" in question_lower:
            return ChatResponse(
                response="The Biometric Lag Index (BLI) measures the gap between child enrollments (age 5-17) and their biometric updates. Formula: BLI = (Enrollments - Updates) / Enrollments. A higher BLI indicates more children who have enrolled but haven't updated their biometrics, putting them at risk of service disruption.",
                suggested_questions=["Which districts have critical BLI?", "What is the overall BLI?"]
            )
        
        if "overall" in question_lower or "total" in question_lower:
            return ChatResponse(
                response=f"The overall BLI across all districts is {analysis.overall_bli}. This is calculated from {analysis.total_records:,} records spanning from {analysis.date_range['start']} to {analysis.date_range['end']}.",
                suggested_questions=["Which district has the highest BLI?", "How many districts are at critical risk?"]
            )
        
        if "critical" in question_lower or "risk" in question_lower:
            critical_districts = [d for d in analysis.top_problem_districts if d.risk_level == "Critical"]
            if critical_districts:
                names = ", ".join([d.district for d in critical_districts[:5]])
                return ChatResponse(
                    response=f"There are {len(critical_districts)} districts at Critical risk level (BLI > 0.5). The top ones are: {names}. These districts need immediate intervention camps to help children update their biometrics.",
                    suggested_questions=["What actions should be taken for critical districts?", "Show me the gap widening trend"]
                )
            else:
                return ChatResponse(
                    response="Good news! No districts are currently at Critical risk level. However, continue monitoring high-risk districts.",
                    suggested_questions=["Which districts are at high risk?"]
                )
        
        if "state" in question_lower:
            top_state = analysis.state_summary[0] if analysis.state_summary else None
            if top_state:
                return ChatResponse(
                    response=f"The state with the highest BLI is {top_state['state']} with a BLI of {round(top_state['bli_score'], 4)}. The state summary shows {len(analysis.state_summary)} states analyzed.",
                    suggested_questions=["Which districts in this state need attention?"]
                )
        
        # Default response
        return ChatResponse(
            response=f"Based on the uploaded data: The overall BLI is {analysis.overall_bli}. The district with the highest lag is {analysis.top_problem_districts[0].district} in {analysis.top_problem_districts[0].state}. Try asking specific questions like 'Which district has the highest BLI?' or 'What is the BLI formula?'",
            suggested_questions=["What is the BLI formula?", "Which districts need intervention?", "What does Critical risk mean?"]
        )
