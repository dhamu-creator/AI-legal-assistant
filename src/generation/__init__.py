"""LLM generation and RAG chain orchestration"""

try:
    from .prompt_templates import LegalPromptTemplates, LegalPromptBuilder
except Exception:
    LegalPromptTemplates = None
    LegalPromptBuilder = None

try:
    from .llm_chain import LegalRAGChain, LegalCitationTracker, LegalAnswer, build_rag_chain
except Exception:
    LegalRAGChain = None
    LegalCitationTracker = None
    LegalAnswer = None
    build_rag_chain = None

__all__ = [
    "LegalPromptTemplates",
    "LegalPromptBuilder",
    "LegalRAGChain",
    "LegalCitationTracker",
    "LegalAnswer",
    "build_rag_chain",
]
