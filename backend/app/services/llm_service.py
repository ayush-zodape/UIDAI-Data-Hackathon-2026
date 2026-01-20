import httpx
from typing import Dict, Any, List
import pandas as pd
from app.models.schemas import ChatResponse
from app.services.data_processor import BLIProcessor

class LLMService:
    """
    Service for handling AI chatbot queries about the data using Ollama (local LLM)
    """
    
    def __init__(self, df_enrollment: pd.DataFrame, df_biometric: pd.DataFrame):
        self.ollama_url = "http://localhost:11434/api/generate"
        self.model = "llama3.2:1b"
        self.processor = BLIProcessor(df_enrollment, df_biometric)
        self._prepare_context()
    
    def _prepare_context(self):
        """Prepare a comprehensive summary of the data for the LLM"""
        analysis = self.processor.compute_district_bli()
        
        # Get all districts data for detailed context
        all_districts_info = self._format_all_districts(analysis.top_problem_districts)
        state_info = self._format_states(analysis.state_summary)
        
        self.data_context = f"""You are an AI assistant analyzing UIDAI Aadhaar biometric data for the "Digital Continuity" project.

=== DATA SUMMARY ===
- Total records analyzed: {analysis.total_records:,}
- Date range: {analysis.date_range['start']} to {analysis.date_range['end']}
- Overall Biometric Lag Index (BLI): {analysis.overall_bli}

=== BLI FORMULA ===
BLI = (Total Enrollments for age 5-17) - (Total Biometric Updates for age 5-17)) / (Total Enrollments for age 5-17)

=== RISK LEVEL THRESHOLDS ===
- BLI < 0.1: Low Risk (Green) - Acceptable levels
- BLI 0.1-0.3: Medium Risk (Yellow) - Needs monitoring  
- BLI 0.3-0.5: High Risk (Orange) - Needs attention
- BLI > 0.5: Critical Risk (Red) - Immediate intervention required

=== ALL DISTRICT DATA (Sorted by BLI - Highest First) ===
{all_districts_info}

=== STATE SUMMARY (Sorted by BLI - Highest First) ===
{state_info}

=== WHAT BLI MEANS ===
The Biometric Lag Index measures children (age 5-17) who have enrolled in Aadhaar but have NOT updated their biometrics. High BLI means many children risk service disruption when their biometrics become outdated.

=== YOUR ROLE ===
Answer questions about this data accurately. Use specific numbers from the data above. If asked about trends, districts, states, or interventions, reference the actual data provided."""
        
        self.analysis = analysis
        
        # Store detailed data for specific queries
        self.districts_data = {d.district.lower(): d for d in analysis.top_problem_districts}
        self.states_data = {s['state'].lower(): s for s in analysis.state_summary}
    
    def _format_all_districts(self, districts) -> str:
        lines = []
        for i, d in enumerate(districts, 1):
            lines.append(f"{i}. {d.district}, {d.state}: BLI={d.bli_score}, Gap={d.child_update_gap:,} children, Risk={d.risk_level}")
        return "\n".join(lines)
    
    def _format_states(self, states) -> str:
        lines = []
        for i, s in enumerate(states, 1):
            risk = self._get_risk_level(s['bli_score'])
            lines.append(f"{i}. {s['state']}: BLI={round(s['bli_score'], 4)}, Risk={risk}")
        return "\n".join(lines)
    
    def _get_risk_level(self, bli: float) -> str:
        if bli < 0.1:
            return "Low"
        elif bli < 0.3:
            return "Medium"
        elif bli < 0.5:
            return "High"
        else:
            return "Critical"
    
    async def answer_question(self, question: str) -> ChatResponse:
        """
        Answer a user question about the data using Ollama (local LLM)
        """
        prompt = f"""{self.data_context}

USER QUESTION: {question}

INSTRUCTIONS:
1. Answer ONLY based on the data provided above
2. Use specific numbers, district names, and states from the data
3. If the question is about a specific district or state, look it up in the data above
4. Keep your response concise but informative (2-4 sentences)
5. If the data doesn't contain the answer, say so clearly

YOUR ANSWER:"""
        
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    self.ollama_url,
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "stream": False,
                        "options": {
                            "temperature": 0.3,
                            "num_predict": 300,
                            "top_p": 0.9
                        }
                    }
                )
                
                if response.status_code == 200:
                    result = response.json()
                    answer = result.get("response", "").strip()
                    
                    # Clean up the response
                    if answer:
                        # Remove any repetitive content
                        answer = self._clean_response(answer)
                        
                        # Generate context-aware suggested questions
                        suggested = self._generate_suggestions(question)
                        
                        return ChatResponse(
                            response=answer,
                            suggested_questions=suggested
                        )
                
                # If Ollama fails, use fallback
                return self._fallback_response(question)
                
        except Exception as e:
            print(f"Ollama error: {e}")
            # Fallback to rule-based responses if Ollama fails
            return self._fallback_response(question)
    
    def _clean_response(self, response: str) -> str:
        """Clean up LLM response"""
        # Remove common artifacts
        response = response.strip()
        
        # Limit to reasonable length
        sentences = response.split('.')
        if len(sentences) > 6:
            response = '.'.join(sentences[:5]) + '.'
        
        return response
    
    def _generate_suggestions(self, asked_question: str) -> List[str]:
        """Generate relevant follow-up questions based on what was asked"""
        asked_lower = asked_question.lower()
        
        suggestions = []
        
        if "highest" in asked_lower or "worst" in asked_lower:
            suggestions = [
                "What is the overall BLI across all districts?",
                "Which state has the most critical districts?",
                "What interventions do you recommend?"
            ]
        elif "state" in asked_lower:
            suggestions = [
                "Which district in this state needs the most attention?",
                "What is the overall BLI?",
                "How many districts are at critical risk?"
            ]
        elif "bli" in asked_lower and ("what" in asked_lower or "explain" in asked_lower):
            suggestions = [
                "Which district has the highest BLI?",
                "How many children are affected overall?",
                "What does critical risk mean?"
            ]
        elif "risk" in asked_lower or "critical" in asked_lower:
            suggestions = [
                "List all critical risk districts",
                "What actions should be taken?",
                "Which state has the most problems?"
            ]
        else:
            suggestions = [
                "Which district has the highest BLI?",
                "What is the BLI formula?",
                "How many districts are at critical risk?",
                "Which state needs the most attention?"
            ]
        
        return suggestions[:4]
    
    def _fallback_response(self, question: str) -> ChatResponse:
        """Comprehensive fallback responses when Ollama is unavailable"""
        question_lower = question.lower()
        
        analysis = self.analysis
        
        # Question about highest BLI district
        if any(word in question_lower for word in ["highest", "worst", "top", "problem"]) and \
           any(word in question_lower for word in ["bli", "lag", "district", "risk"]):
            top = analysis.top_problem_districts[0]
            return ChatResponse(
                response=f"The district with the highest BLI is **{top.district}** in **{top.state}** with a BLI of **{top.bli_score}** ({top.risk_level} risk). This means **{top.child_update_gap:,}** children have enrolled but not yet updated their biometrics, putting them at risk of service disruption.",
                suggested_questions=["Why is this district's BLI so high?", "What is the overall BLI?", "Which districts need immediate intervention?"]
            )
        
        # Question about what BLI is
        if "what is bli" in question_lower or "biometric lag" in question_lower or "explain bli" in question_lower:
            return ChatResponse(
                response=f"The **Biometric Lag Index (BLI)** measures the gap between child enrollments (age 5-17) and their biometric updates. **Formula:** BLI = (Enrollments - Updates) / Enrollments. A higher BLI indicates more children who have enrolled but haven't updated their biometrics. Currently, the overall BLI is **{analysis.overall_bli}**.",
                suggested_questions=["Which districts have critical BLI?", "What is the overall BLI?", "What do the risk levels mean?"]
            )
        
        # Question about overall/total
        if any(word in question_lower for word in ["overall", "total", "average", "summary"]):
            critical_count = len([d for d in analysis.top_problem_districts if d.risk_level == "Critical"])
            high_count = len([d for d in analysis.top_problem_districts if d.risk_level == "High"])
            return ChatResponse(
                response=f"**Overall Summary:** The BLI across all districts is **{analysis.overall_bli}**. Total records analyzed: **{analysis.total_records:,}** spanning from {analysis.date_range['start']} to {analysis.date_range['end']}. Currently, **{critical_count}** districts are at Critical risk and **{high_count}** are at High risk.",
                suggested_questions=["Which district has the highest BLI?", "How many districts are at critical risk?", "Which state needs intervention?"]
            )
        
        # Question about critical/risk
        if any(word in question_lower for word in ["critical", "risk", "danger", "urgent"]):
            critical_districts = [d for d in analysis.top_problem_districts if d.risk_level == "Critical"]
            high_districts = [d for d in analysis.top_problem_districts if d.risk_level == "High"]
            
            if critical_districts:
                names = ", ".join([f"{d.district} ({d.state})" for d in critical_districts[:5]])
                return ChatResponse(
                    response=f"**{len(critical_districts)} districts** are at Critical risk level (BLI > 0.5). Top critical districts: **{names}**. Additionally, **{len(high_districts)}** districts are at High risk. These need immediate biometric update camps.",
                    suggested_questions=["What actions should be taken?", "Show me the gap widening trend", "Which state has the most critical districts?"]
                )
            else:
                return ChatResponse(
                    response=f"Good news! No districts are currently at Critical risk. However, **{len(high_districts)}** districts are at High risk and should be monitored closely.",
                    suggested_questions=["Which districts are at high risk?", "What is the overall BLI?"]
                )
        
        # Question about specific state
        if "state" in question_lower:
            if analysis.state_summary:
                top_state = analysis.state_summary[0]
                bottom_state = analysis.state_summary[-1] if len(analysis.state_summary) > 1 else None
                response = f"**State with highest BLI:** {top_state['state']} with BLI of **{round(top_state['bli_score'], 4)}**."
                if bottom_state:
                    response += f" **Best performing state:** {bottom_state['state']} with BLI of **{round(bottom_state['bli_score'], 4)}**."
                response += f" Total **{len(analysis.state_summary)}** states analyzed."
                return ChatResponse(
                    response=response,
                    suggested_questions=["Which districts in this state need attention?", "What is the overall BLI?"]
                )
        
        # Question about intervention/action/recommendation
        if any(word in question_lower for word in ["intervention", "action", "recommend", "solution", "help", "fix"]):
            critical_districts = [d for d in analysis.top_problem_districts if d.risk_level == "Critical"]
            return ChatResponse(
                response=f"**Recommended Actions:** 1) Organize biometric update camps in **{len(critical_districts)}** critical districts, prioritizing {analysis.top_problem_districts[0].district}. 2) Deploy mobile enrollment units to schools. 3) Run awareness campaigns for parents about the importance of updating children's biometrics. 4) Set up monitoring dashboards to track progress weekly.",
                suggested_questions=["Which districts are most critical?", "How many children are affected?", "What is the BLI formula?"]
            )
        
        # Question about children/affected
        if any(word in question_lower for word in ["children", "kids", "affected", "gap", "how many"]):
            total_gap = sum(d.child_update_gap for d in analysis.top_problem_districts)
            return ChatResponse(
                response=f"Based on the analyzed data, approximately **{total_gap:,}** children (age 5-17) have enrolled but not updated their biometrics across all districts. The district with the largest gap is **{analysis.top_problem_districts[0].district}** with **{analysis.top_problem_districts[0].child_update_gap:,}** children affected.",
                suggested_questions=["Which district has the highest BLI?", "What interventions do you recommend?"]
            )
        
        # Question about list/all districts
        if any(word in question_lower for word in ["list", "all", "show"]) and "district" in question_lower:
            district_list = "\n".join([f"• {d.district} ({d.state}): BLI={d.bli_score}, {d.risk_level} risk" 
                                        for d in analysis.top_problem_districts[:10]])
            return ChatResponse(
                response=f"**Top 10 Districts by BLI:**\n{district_list}",
                suggested_questions=["What is the overall BLI?", "Which state has the most problems?"]
            )
        
        # Default response with helpful context
        top = analysis.top_problem_districts[0]
        return ChatResponse(
            response=f"Based on the uploaded data: **Overall BLI is {analysis.overall_bli}**. The district needing most attention is **{top.district}** in **{top.state}** with BLI of **{top.bli_score}** ({top.risk_level} risk). Total **{analysis.total_records:,}** records analyzed. Ask me about specific districts, states, risk levels, or recommendations!",
            suggested_questions=["What is the BLI formula?", "Which districts need intervention?", "What does Critical risk mean?", "Which state has the highest BLI?"]
        )
