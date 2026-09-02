from pydantic import BaseModel
from typing import List, TypedDict, Annotated
import logging
from app.config import settings

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, START, END

logger = logging.getLogger(__name__)

class InvestigationResult(BaseModel):
    is_anomaly: bool
    confidence_score: float
    root_cause: str
    recommended_action: str
    affected_nodes: List[str]

class InvestigationState(TypedDict):
    case_data: dict
    graph_context: str
    extracted_facts: str
    analysis: str
    result: InvestigationResult

class InvestigationAgent:
    def __init__(self):
        if not settings.OPENAI_API_KEY:
            logger.warning("OPENAI_API_KEY is not set. InvestigationAgent will run in mock mode.")
            self.llm = None
        else:
            self.llm = ChatOpenAI(model="gpt-4o-2024-08-06", api_key=settings.OPENAI_API_KEY)
        self.graph = self._build_graph()

    def _build_graph(self):
        workflow = StateGraph(InvestigationState)

        workflow.add_node("extract_facts", self.node_extract_facts)
        workflow.add_node("analyze", self.node_analyze)
        workflow.add_node("formulate_conclusion", self.node_formulate_conclusion)

        workflow.add_edge(START, "extract_facts")
        workflow.add_edge("extract_facts", "analyze")
        workflow.add_edge("analyze", "formulate_conclusion")
        workflow.add_edge("formulate_conclusion", END)

        return workflow.compile()

    def node_extract_facts(self, state: InvestigationState):
        if not self.llm:
            return {"extracted_facts": "Mock facts extracted."}
            
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an AI Finance Controller. Extract key financial facts from the provided case data and graph context."),
            ("user", "Case Data: {case_data}\n\nGraph Context: {graph_context}")
        ])
        chain = prompt | self.llm
        response = chain.invoke({"case_data": state["case_data"], "graph_context": state["graph_context"]})
        return {"extracted_facts": response.content}

    def node_analyze(self, state: InvestigationState):
        if not self.llm:
            return {"analysis": "Mock analysis."}
            
        prompt = ChatPromptTemplate.from_messages([
            ("system", "Analyze the extracted financial facts to determine discrepancies or anomalies."),
            ("user", "Facts: {extracted_facts}")
        ])
        chain = prompt | self.llm
        response = chain.invoke({"extracted_facts": state["extracted_facts"]})
        return {"analysis": response.content}

    def node_formulate_conclusion(self, state: InvestigationState):
        if not self.llm:
            return {"result": InvestigationResult(
                is_anomaly=True,
                confidence_score=0.85,
                root_cause="Mocked missing key: Fee mismatch between Payment and Settlement",
                recommended_action="Create fee adjustment entry",
                affected_nodes=["PAY-001", "SET-001"]
            )}
            
        prompt = ChatPromptTemplate.from_messages([
            ("system", "Based on the analysis, formulate a structured final conclusion."),
            ("user", "Analysis: {analysis}")
        ])
        structured_llm = self.llm.with_structured_output(InvestigationResult)
        chain = prompt | structured_llm
        response = chain.invoke({"analysis": state["analysis"]})
        return {"result": response}

    async def investigate_discrepancy(self, case_data: dict, graph_context: str) -> InvestigationResult:
        inputs = {
            "case_data": case_data,
            "graph_context": graph_context,
            "extracted_facts": "",
            "analysis": "",
            "result": None
        }
        
        final_state = await self.graph.ainvoke(inputs)
        return final_state["result"]

# Singleton instance
investigation_agent = InvestigationAgent()

class QAAgent:
    @staticmethod
    async def answer_question(question: str, context: str) -> str:
        if not settings.OPENAI_API_KEY:
            return "Mock response: The OpenAI API key is not configured. Please set it in .env."
            
        llm = ChatOpenAI(model="gpt-4o", api_key=settings.OPENAI_API_KEY)
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a conversational AI Finance Assistant. Answer the user's question based strictly on the provided financial graph context. If the context does not contain the answer, say you do not have enough information."),
            ("user", "Context: {context}\nQuestion: {question}")
        ])
        
        chain = prompt | llm
        response = await chain.ainvoke({"context": context, "question": question})
        return response.content
