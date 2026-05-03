from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Dict
from agents import ResearchAgent, VerificationAgent, RelevanceChecker
from langchain_core.documents import Document
from langchain_classic.retrievers import EnsembleRetriever
from config import settings
from utils import logger

class AgentState(TypedDict):
    question: str
    documents: List[Document]
    draft_answer: str
    verification_report: str
    raw_report: Dict
    is_relevant: bool
    retriever: EnsembleRetriever
    retries: int # Safeguard against infinite loops

class AgentWorkflow:
    def __init__(self):
        self.researcher = ResearchAgent()
        self.verifier = VerificationAgent()
        self.relevance_checker = RelevanceChecker()
        self.compiled_workflow = self.build_workflow()  # Compile once during initialization
        
    def build_workflow(self):
        """Create and compile the multi-agent workflow."""
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("check_relevance", self._check_relevance_step)
        workflow.add_node("research", self._research_step)
        workflow.add_node("verify", self._verification_step)
        
        # Define edges
        workflow.set_entry_point("check_relevance")
        workflow.add_conditional_edges(
            "check_relevance",
            self._decide_after_relevance_check,
            {
                "relevant": "research",
                "irrelevant": END
            }
        )
        workflow.add_edge("research", "verify")
        workflow.add_conditional_edges(
            "verify",
            self._decide_next_step,
            {
                "re_research": "research",
                "end": END
            }
        )
        return workflow.compile()
    
    def _check_relevance_step(self, state: AgentState) -> Dict:
        retriever = state["retriever"]
        classification = self.relevance_checker.check(
            question=state["question"], 
            retriever=state["retriever"], 
            k=settings.RETRIEVAL.VECTOR_SEARCH_K
        )

        is_relevant = classification in ["CAN_ANSWER", "PARTIAL"]

        update = {"is_relevant": is_relevant}
        
        if not is_relevant:
            update["draft_answer"] = "This question isn't related to the uploaded document(s)."

        return update

    def _decide_after_relevance_check(self, state: AgentState) -> str:
        decision = "relevant" if state["is_relevant"] else "irrelevant"
        print(f"[DEBUG] _decide_after_relevance_check -> {decision}")
        return decision
    
    def _research_step(self, state: AgentState) -> Dict:
        print(f"[DEBUG] Entered _research_step with question='{state['question']}'")
        logger.info(f"Researching attempt: {state.get('retries', 0) + 1}...")
        draft = self.researcher.generate(state["question"], state["documents"])
        print("[DEBUG] Researcher returned draft answer.")
        return {"draft_answer": draft}

    def _verification_step(self, state: AgentState) -> Dict:
        print("[DEBUG] Entered _verification_step. Verifying the draft answer...")

        result = self.verifier.check(state["draft_answer"], state["documents"])
        raw = result["raw_report"]
        print("[DEBUG] VerificationAgent returned a verification report.")
        # Determine if we need to increment the counter
        new_retries = state.get("retries", 0)
        if not raw.get("is_supported") or not raw.get("is_relevant"):
            new_retries += 1
            logger.warning(f"Verification failed. New retry cound: {new_retries}")
        return {
            "verification_report": result['verification_report'],
            "raw_report": raw,
            "retries": new_retries # State is updated by returning the new value
        }

    def _decide_next_step(self, state: AgentState) -> str:
        verification_report = state.get("verification_report")
        raw = state.get("raw_report", {})
        retries = state.get("retries", 0)
        
        # Safeguard 1: Max Retries
        print(f"[DEBUG] _decide_next_step actual safeguard: Stop after 3 failed attempts, retries='{retries}'")
        if retries >= 3:
            logger.error("Max retries (3) reached. Stopping to avoid infinite loop.")
            return "end"

        # Safeguard 2: Logic-based Routing
        print(f"[DEBUG] _decide_next_step with verification_report='{verification_report}'")
        if not raw.get("is_supported") or not raw.get("is_relevant"):
            print("[DEBUG] Verification indicates re-research needed.")
            return "re_research"
        print("[DEBUG] Verification successful, ending workflow.")
        return "end"

    def full_pipeline(self, question: str, retriever: EnsembleRetriever):
        try:
            print(f"[DEBUG] Starting full_pipeline with question='{question}'")
            documents = retriever.invoke(question)
            logger.info(f"Retrieved {len(documents)} relevant documents (from .invoke)")

            initial_state = AgentState(
                question=question,
                documents=documents,
                draft_answer="",
                verification_report="",
                raw_report={},
                is_relevant=False,
                retriever=retriever,
                retries=0
            )
            
            return self.compiled_workflow.invoke(initial_state)
            
        except Exception as e:
            logger.error(f"Workflow execution failed: {e}")
            raise