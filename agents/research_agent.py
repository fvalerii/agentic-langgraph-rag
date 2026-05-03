from typing import List, Dict
from langchain_ibm import ChatWatsonx
from langchain_core.documents import Document
from pydantic import BaseModel, Field
from config import settings
from utils import logger


class ResearchAgent:
    def __init__(self, model: ChatWatsonx = None):
        logger.info("Initializing ResearchAgent with IBM ChatWatsonx...")
        self.model = model or ChatWatsonx(
            model_id="meta-llama/llama-4-maverick-17b-128e-instruct-fp8", 
            url=settings.WATSONX.URL,
            apikey=settings.WATSONX.APIKEY, 
            project_id=settings.WATSONX.PROJECT_ID,
            params={
                "max_new_tokens": 600,            # Adjust based on desired response length
                "temperature": 0.3,           # Controls randomness; lower values make output more deterministic
            }
        )
        logger.info("ChatModel initialized successfully.")

    def generate_prompt(self, question: str, context: str) -> str:
        """
        Generate a structured prompt for the LLM to generate a precise and factual answer.
        """
        prompt = f"""
        You are an AI assistant designed to provide precise and factual answers based on the given context.

        **Instructions:**
        - Answer the following question using ONLY the provided context.
        - Be clear, concise, and factual.
        - If the context does not contain the answer, state that you cannot answer based on the documents.
        - Extract as much relevant detail as possible from the context.

        **Question:** {question}
        **Context:** {context}

        **Answer:**
        """
        return prompt

    def generate(self, question: str, documents: List[Document]) -> Dict:
        """
        Generate the draft answer using the provided document chunks.
        """
        logger.info(f"ResearchAgent called with question='{question}' and {len(documents)} documents.")

        # Combine document contents
        context = "\n\n".join([doc.page_content for doc in documents])
        logger.debug(f"Context size for generation: {len(context)} characters.")

        # Create a prompt for the LLM
        prompt = self.generate_prompt(question, context)
        logger.info("Prompt created for the LLM.")

        # Call the LLM to generate the answer
        try:
            logger.info("Sending prompt to the model...")
            response = self.model.invoke(prompt)
            logger.info("LLM response received.")

            draft_answer = response.content.strip() if response.content else "No response generated."
            logger.info(f"Generated answer: {draft_answer}")

            return draft_answer

        except Exception as e:
            logger.error(f"Error during model inference: {e}")
            raise RuntimeError("Failed to generate answer due to a model error.") from e