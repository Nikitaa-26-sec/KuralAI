"""Backward-compatible import; answer generation lives in rag.llm."""
from rag.llm import LLMServiceError, generate_answer

__all__ = ["LLMServiceError", "generate_answer"]
