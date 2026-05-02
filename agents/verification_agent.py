from typing import List, Dict
from langchain_ibm import ChatWatsonx
from langchain_core.documents import Document
from pydantic import BaseModel, Field
from config import settings
from utils import logger

class VerificationReport(BaseModel):
    """Detailed audit of the generated answer against the context."""
    is_supported: bool = Field(description="Direct or indirect factual support.")
    unsupported_claims: List[str] = Field(description="List of any claims not found in the context.")
    contradictions: List[str] = Field(description="List any claims that contradict the context.")
    is_relevant: bool = Field(description="Is the answer relevant to the user's question?")
    additional_details: str = Field(description="Any extra information or explanation.")

class VerificationAgent:
    def __init__(self, model: ChatWatsonx = None):
        logger.info("Initializing VerificationAgent with IBM ChatWatsonx...")
        self.model = model or ChatWatsonx(
            model_id="ibm/granite-4-h-small", 
            url=settings.WATSONX.URL,
            apikey=settings.WATSONX.APIKEY, 
            project_id=settings.WATSONX.PROJECT_ID,
            params={
                "max_new_tokens": 400,        # Adjust based on desired response length
                "temperature": 0.0,           # Remove randomness for consistency
            }
        )
        self.structured_llm = self.model.with_structured_output(VerificationReport)
        print("ChatModel initialized successfully.")

    def generate_prompt(self, answer: str, context: str) -> str:
        return f"""
        You are an AI assistant designed to verify the accuracy and relevance of answers based on the provided context.

        **Instructions:**
        - Verify the following answer against the provided context.
        - Check for: factual support, unsupported claims, contradictions, relevance, and additional details or explanations where relevant.

        **Answer:** {answer}
        **Context:** {context}
        """

    def format_verification_report(self, report: VerificationReport) -> str:
        """
        Format the Pydantic report object into a readable string.
        """
        res = [
            f"**Supported:** {'YES' if report.is_supported else 'NO'}",
            f"**Relevant:** {'YES' if report.is_relevant else 'NO'}",
            f"**Unsupported Claims:** {', '.join(report.unsupported_claims) if report.unsupported_claims else 'None'}",
            f"**Contradictions:** {', '.join(report.contradictions) if report.contradictions else 'None'}",
            f"**Details:** {report.additional_details or 'None'}"
        ]

        return "\n".join(res)

    def check(self, answer: str, documents: List[Document]) -> Dict:
        logger.info(f"VerificationAgent.check called with answer='{answer}' and {len(documents)} documents.")

        # Combine all document contents into one string without truncation
        context = "\n\n".join([doc.page_content for doc in documents])
        logger.info(f"Combined context length: {len(context)} characters.")

        # Create a prompt for the LLM to verify the answer
        prompt = self.generate_prompt(answer, context)
        logger.info("Prompt created for the LLM.")

        try:
            logger.info("Sending prompt to the model...")
            report_obj = self.structured_llm.invoke(prompt)
            logger.info("LLM response received.")
            formatted_text = self.format_verification_report(report_obj)
            logger.info(f"Verification report:\n{formatted_text}")
            logger.info(f"Context used:\n{context}")

            return {
                "verification_report": formatted_text,
                "raw_report": report_obj.model_dump(),
                "context_used": context
            }

        except Exception as e:
            logger.error(f"Error during verification: {e}")
            raise RuntimeError("Failed to verify answer.") from e