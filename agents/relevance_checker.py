from langchain_ibm import ChatWatsonx
from pydantic import BaseModel, Field
from typing import Literal
from config import settings
from utils import logger

class RelevanceGrade(BaseModel):
    """Structured output for relevance check."""
    # We keep the 3 labels for better evaluation data later
    classification: Literal["CAN_ANSWER", "PARTIAL", "NO_MATCH"] = Field(
        description="The relevance classification of the document relative to the question."
    )

class RelevanceChecker:
    def __init__(self, model: Optional[ChatWatsonx] = None):
        if model:
            self.model=model
        else:
            self.model = ChatWatsonx(
                model_id="ibm/granite-3-3-8b-instruct",
                url=settings.WATSONX.URL,
                apikey=settings.WATSONX.APIKEY,
                project_id=settings.WATSONX.PROJECT_ID,
                params={"temperature": 0, "max_new_tokens": 10}
            )

        self.structured_llm=self.model.with_structured_output(RelevanceGrade)

    def check(self, question: str, retriever, k:int) -> str:
        """
        1. Retrieve the top-k document chunks from the global retriever.
        2. Combine them into a single text string.
        3. Pass that text + question to the LLM for classification.
        4. Grades document relevance using structured output.

        Returns: "CAN_ANSWER", "PARTIAL", or "NO_MATCH".
        """

        logger.debug(f"RelevanceChecker.check called with question='{question}' and k={k}")

        # Retrieve doc chunks from the ensemble retriever
        top_docs = retriever.invoke(question)
        if not top_docs:
            logger.debug("No documents returned from retriever.invoke(). Classifying as NO_MATCH.")
            return "NO_MATCH"

        # Combine the top k chunk texts into one string
        document_content = "\n\n".join(doc.page_content for doc in top_docs[:k])

        # Create a prompt for the LLM to classify relevance
        prompt = f"""
        You are an AI relevance checker between a user's question and provided document content.

        **Instructions:**
        - Classify how well the document content addresses the user's question.

        **Labels:**
        1) "CAN_ANSWER": The passages contain enough explicit information to fully answer the question.
        2) "PARTIAL": The passages mention or discuss the question's topic but do not provide all the details needed for a complete answer.
        3) "NO_MATCH": The passages do not discuss or mention the question's topic at all.

        **Important:** If the passages mention or reference the topic or timeframe of the question in any way, even if incomplete, respond with "PARTIAL" instead of "NO_MATCH".

        **Question:** {question}
        **Passages:** {document_content}
        """

        # Call the LLM
        try:
            result = self.structured_llm.invoke(prompt)
            logger.info(f"Relevance Classification: {result.classification}")
            print(f"Checker response: {result.classification}")
            return result.classification

        except Exception as e:
            logger.error(f"Relevance check failed: {e}")
            return "NO_MATCH"