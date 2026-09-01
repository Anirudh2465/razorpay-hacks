from openai import AsyncOpenAI
from pydantic import BaseModel
from typing import List, Optional
from app.config import settings

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

class InvestigationResult(BaseModel):
    is_anomaly: bool
    confidence_score: float
    root_cause: str
    recommended_action: str
    affected_nodes: List[str]

class InvestigationAgent:
    @staticmethod
    async def investigate_discrepancy(case_data: dict, graph_context: str) -> InvestigationResult:
        if not settings.OPENAI_API_KEY:
            # Fallback for hackathon demo if key is missing
            return InvestigationResult(
                is_anomaly=True,
                confidence_score=0.85,
                root_cause="Mocked missing key: Fee mismatch between Payment and Settlement",
                recommended_action="Create fee adjustment entry",
                affected_nodes=["PAY-001", "SET-001"]
            )
            
        system_prompt = """
        You are an AI Finance Controller. Your job is to investigate reconciliation discrepancies.
        Analyze the provided case data and the relevant subgraph context to determine the root cause.
        Return the structured analysis.
        """
        
        user_prompt = f"Case Data:\n{case_data}\n\nGraph Context:\n{graph_context}"
        
        response = await client.beta.chat.completions.parse(
            model="gpt-4o-2024-08-06",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format=InvestigationResult
        )
        
        return response.choices[0].message.parsed

class QAAgent:
    @staticmethod
    async def answer_question(question: str, context: str) -> str:
        if not settings.OPENAI_API_KEY:
            return "Mock response: The OpenAI API key is not configured. Please set it in .env."
            
        system_prompt = """
        You are a conversational AI Finance Assistant. Answer the user's question based strictly on the provided financial graph context.
        If the context does not contain the answer, say you do not have enough information.
        """
        
        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Context: {context}\nQuestion: {question}"}
            ]
        )
        
        return response.choices[0].message.content
