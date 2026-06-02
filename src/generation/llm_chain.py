"""
LangChain RAG Chain for Legal Question Answering
Orchestrates the complete RAG pipeline: query → retrieval → prompt → LLM → response
"""

import logging
from typing import List, Dict, Optional, Any, Generator
from dataclasses import dataclass

# Updated imports for newer LangChain
import os

try:
    from langchain_groq import ChatGroq
except ImportError:
    ChatGroq = None

try:
    from langchain_google_genai import ChatGoogleGenerativeAI
except ImportError:
    ChatGoogleGenerativeAI = None

try:
    from langchain_openai import ChatOpenAI
except ImportError:
    ChatOpenAI = None

try:
    from langchain.memory import ConversationBufferMemory, ConversationSummaryMemory
except ImportError:
    try:
        from langchain_community.memory import ConversationBufferMemory, ConversationSummaryMemory
    except ImportError:
        # Fallback: Create dummy memory classes if not available
        class ConversationBufferMemory:
            def __init__(self, *args, **kwargs):
                self.buffer = ""
            def load_memory_variables(self, inputs):
                return {"history": self.buffer}
            def save_context(self, inputs, outputs):
                self.buffer += f"\nInput: {inputs}\nOutput: {outputs}"

        class ConversationSummaryMemory:
            def __init__(self, *args, **kwargs):
                self.buffer = ""
            def load_memory_variables(self, inputs):
                return {"history": self.buffer}
            def save_context(self, inputs, outputs):
                self.buffer += f"\nInput: {inputs}\nOutput: {outputs}"

try:
    from langchain.schema import Document
except ImportError:
    from langchain_core.documents import Document

from src.generation.prompt_templates import LegalPromptTemplates, LegalPromptBuilder
from src.retrieval.vector_store import RetrievalResult

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class LegalAnswer:
    """Structured response from legal QA system"""
    question: str
    answer: str
    sources: List[Dict]  # Retrieved documents
    citations: List[str]  # Extracted citations from answer
    confidence_score: float
    model: str
    tokens_used: Dict  # input/output token counts


class LegalRAGChain:
    """
    Main RAG chain combining retriever, prompts, and LLM.
    Handles both single queries and multi-turn conversations.
    """

    def __init__(
        self,
        retriever,
        llm_provider: str = "groq",
        model_name: str = None,
        temperature: float = 0.1,
        max_tokens: int = 1500,
        use_conversation_memory: bool = True,
        memory_type: str = "buffer"  # "buffer" or "summary"
    ):
        """
        Initialize RAG chain.

        Args:
            retriever: HybridRetriever instance
            llm_provider: "groq" (default), "google", "openai"
            model_name: Model ID (e.g., "llama-3.3-70b-versatile", "gemini-2.0-flash", "gpt-4")
            temperature: LLM temperature (0.0-1.0)
            max_tokens: Maximum response tokens
            use_conversation_memory: Enable multi-turn conversation
            memory_type: "buffer" for full history, "summary" for summarized
        """
        self.retriever = retriever
        self.llm_provider = llm_provider
        self.temperature = temperature
        self.max_tokens = max_tokens

        # Initialize LLM
        self.llm = self._init_llm(
            llm_provider,
            model_name or self._get_default_model(llm_provider),
            temperature,
            max_tokens
        )

        # Initialize memory for conversation
        self.memory = None
        if use_conversation_memory:
            if memory_type == "summary":
                self.memory = ConversationSummaryMemory(
                    llm=self.llm,
                    buffer="",
                    input_key="input",
                    output_key="output"
                )
            else:
                self.memory = ConversationBufferMemory(
                    input_key="input",
                    output_key="output",
                    return_messages=True
                )

        # Initialize prompt builder
        self.prompt_builder = LegalPromptBuilder(llm_provider)
        self.templates = LegalPromptTemplates()

        logger.info(f"LegalRAGChain initialized with {llm_provider} ({model_name})")

    def _init_llm(
        self,
        provider: str,
        model_name: str,
        temperature: float,
        max_tokens: int
    ):
        """Initialize LLM based on provider."""
        if provider == "groq":
            if ChatGroq is None:
                raise ImportError(
                    "langchain_groq not installed. "
                    "Install with: pip install langchain-groq"
                )
            groq_api_key = os.getenv("GROQ_API_KEY")
            if not groq_api_key:
                raise ValueError(
                    "GROQ_API_KEY not found in environment. "
                    "Please set it in your .env file."
                )
            return ChatGroq(
                model=model_name,
                groq_api_key=groq_api_key,
                temperature=temperature,
                max_tokens=max_tokens,
            )
        elif provider == "google":
            if ChatGoogleGenerativeAI is None:
                raise ImportError(
                    "langchain_google_genai not installed. "
                    "Install with: pip install langchain-google-genai google-generativeai"
                )
            gemini_api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
            if not gemini_api_key:
                raise ValueError(
                    "GEMINI_API_KEY not found in environment. "
                    "Please set it in your .env file."
                )
            return ChatGoogleGenerativeAI(
                model=model_name,
                google_api_key=gemini_api_key,
                temperature=temperature,
                max_output_tokens=max_tokens,
                convert_system_message_to_human=True
            )
        elif provider == "openai":
            if ChatOpenAI is None:
                raise ImportError(
                    "langchain_openai not installed. "
                    "Install with: pip install langchain-openai"
                )
            return ChatOpenAI(
                model_name=model_name,
                temperature=temperature,
                max_tokens=max_tokens,
                streaming=False
            )
        else:
            raise ValueError(
                f"Unsupported LLM provider: '{provider}'. "
                "Supported: 'groq', 'google', 'openai'"
            )

    def _get_default_model(self, provider: str) -> str:
        """Get default model for provider."""
        defaults = {
            "groq": "llama-3.3-70b-versatile",
            "google": "gemini-2.0-flash",
            "openai": "gpt-4-turbo-preview",
        }
        return defaults.get(provider, "llama-3.3-70b-versatile")

    def query(
        self,
        question: str,
        top_k: int = 5,
        use_memory: bool = True,
        stream: bool = False
    ) -> LegalAnswer:
        """
        Process a legal question and return answer with citations.
        
        Args:
            question: User's legal question
            top_k: Number of documents to retrieve
            use_memory: Use conversation memory if available
            stream: Stream response token by token (if supported)
        
        Returns:
            LegalAnswer object with question, answer, sources, and citations
        """
        logger.info(f"Processing query: {question[:100]}...")

        # Step 1: Retrieve relevant documents
        retrieved = self.retriever.hybrid_search(
            query=question,
            top_k=top_k
        )

        # Convert to documents for prompt
        context_docs = [
            {
                "text": r.text,
                "case_name": r.case_name,
                "court_name": r.court_name,
                "case_citations": r.case_citations,
                "ipc_sections": r.ipc_sections,
                "page_numbers": r.page_numbers
            }
            for r in retrieved
        ]

        # Step 2: Build prompt
        if use_memory and self.memory:
            # Multi-turn conversation
            chat_history = self._format_memory_to_history()
            prompt_text = self.prompt_builder.build_multi_turn_prompt(
                question=question,
                context_docs=context_docs,
                chat_history=chat_history
            )
        else:
            # Single query
            prompt_text = self.prompt_builder.build_rag_prompt_with_context(
                question=question,
                context_docs=context_docs
            )

        # Step 3: Get LLM response
        logger.info("Generating response...")
        
        if stream:
            answer = self._query_streaming(prompt_text)
        else:
            answer = self._query_sync(prompt_text)

        # Step 4: Extract citations from answer
        citations = self._extract_citations_from_answer(answer)

        # Step 5: Update memory if enabled
        if use_memory and self.memory:
            self.memory.save_context(
                {"input": question},
                {"output": answer}
            )

        # Calculate confidence (simple heuristic based on retrieved docs)
        if retrieved:
            confidence = min(1.0, max(retrieved, key=lambda x: x.similarity_score).similarity_score)
        else:
            confidence = 0.0

        # Resolve model name across different LLM provider objects
        model_name = (
            getattr(self.llm, 'model_name', None)
            or getattr(self.llm, 'model', 'unknown')
        )

        return LegalAnswer(
            question=question,
            answer=answer,
            sources=context_docs,
            citations=citations,
            confidence_score=confidence,
            model=model_name,
            tokens_used={
                "input": len(prompt_text.split()),
                "output": len(answer.split())
            }
        )

    def _query_sync(self, prompt_text: str) -> str:
        """Synchronous LLM query via LangChain."""
        try:
            response = self.llm.invoke(prompt_text)
            # invoke() returns an AIMessage; extract the text content
            if hasattr(response, 'content'):
                return response.content
            return str(response)
        except Exception as e:
            logger.error(f"LLM query error: {str(e)}")
            return f"Error generating response: {str(e)}"

    def _query_streaming(self, prompt_text: str) -> str:
        """Streaming LLM query (falls back to sync for Gemini)."""
        # Gemini via LangChain uses sync invoke; streaming is not required
        return self._query_sync(prompt_text)

    def _extract_citations_from_answer(self, answer: str) -> List[str]:
        """
        Extract citations from LLM response.
        Looks for patterns like [YYYY] SCC 45, Section 302 IPC, etc.
        """
        import re
        
        citations = []
        
        # IPC sections: "Section 302 IPC", "S. 420 IPC", "§ 302"
        ipc_pattern = r"(?:Section|§|S\.)\s+(\d+[A-Z]?)\s+(?:IPC|of the Indian Penal Code)"
        ipc_matches = re.findall(ipc_pattern, answer, re.IGNORECASE)
        citations.extend([f"Section {m} IPC" for m in ipc_matches])
        
        # Case citations: "[2021] SCC 45", "AIR 2021 SC 123"
        case_pattern = r"\[(\d{4})\]\s+(?:SCC|SC|HC|AIR|SCR)\s+\d+"
        case_matches = re.findall(case_pattern, answer)
        
        cite_pattern = r"(?:\[(\d{4})\]\s+)?(?:(SCC|SC|HC|AIR|SCR)\s+\d+)"
        cites = re.finditer(cite_pattern, answer)
        citations.extend([m.group(0) for m in cites])
        
        return list(set(citations))  # Remove duplicates

    def _format_memory_to_history(self) -> List[Dict]:
        """Convert memory to chat history format."""
        if not self.memory:
            return []
        
        # Extract from memory buffer
        history = []
        if hasattr(self.memory, 'buffer'):
            # BufferMemory
            buffer_text = str(self.memory.buffer)
            # Simple parsing - in production, would need better extraction
            lines = buffer_text.split("\n")
            for line in lines:
                if ":" in line:
                    role, content = line.split(":", 1)
                    history.append({
                        "role": role.lower().strip(),
                        "content": content.strip()
                    })
        
        return history[-4:]  # Return last 4 turns to keep context manageable

    def clear_memory(self):
        """Clear conversation memory."""
        if self.memory:
            self.memory.clear()
            logger.info("Conversation memory cleared")

    def get_memory_summary(self) -> Dict:
        """Get summary of conversation memory as a dict."""
        if not self.memory:
            return {"total_turns": 0, "summary": "No memory enabled"}
        
        if hasattr(self.memory, 'buffer'):
            buffer_text = str(self.memory.buffer)
            # Count turns: each user input is one turn
            turns = buffer_text.count("Input:") if buffer_text else 0
            return {"total_turns": turns, "summary": buffer_text[:200]}
        
        return {"total_turns": 0, "summary": "Memory available but format unknown"}


class LegalCitationTracker:
    """
    Tracks and formats citations within legal documents and responses.
    """

    @staticmethod
    def extract_all_citations(text: str) -> Dict[str, List[str]]:
        """
        Extract all types of citations from text.
        
        Returns:
            Dictionary with 'ipc_sections', 'case_citations', 'acts', 'articles'
        """
        import re
        
        citations = {
            "ipc_sections": [],
            "case_citations": [],
            "acts": [],
            "articles": [],
            "rules": []
        }

        # IPC sections
        ipc_pattern = r"(?:Section|§|S\.)\s+(\d+[A-Z]?)\s+(?:IPC|of the Indian Penal Code)"
        citations["ipc_sections"] = list(set(re.findall(ipc_pattern, text, re.IGNORECASE)))

        # Case citations
        # Format: [YYYY] Reporter Page
        cite_pattern = r"\[(\d{4})\]\s+(?:SCC|SCR|SCJ|AIR|HC|ALJ)\s+(\d+)"
        citations["case_citations"] = list(set(re.findall(cite_pattern, text)))

        # Acts/Laws
        acts_pattern = r"(?:the\s+)?([A-Z][a-zA-Z]+(?:\s+[A-Z])?(?:\s+Act)?),?\s+(?:\d{4}|Act)"
        citations["acts"] = list(set(re.findall(acts_pattern, text)))

        # Constitutional Articles
        article_pattern = r"Article\s+(\d+)"
        citations["articles"] = list(set(re.findall(article_pattern, text)))

        # Rules
        rule_pattern = r"Rule\s+(\d+)"
        citations["rules"] = list(set(re.findall(rule_pattern, text)))

        return citations

    @staticmethod
    def format_citations(citations: Dict[str, List[str]]) -> str:
        """
        Format extracted citations for display.
        """
        formatted = []

        if citations.get("ipc_sections"):
            formatted.append(f"IPC Sections: {', '.join([f'§{s}' for s in citations['ipc_sections']])}")

        if citations.get("case_citations"):
            formatted.append(f"Cases: {', '.join([f'[{c[0]}] {c[1]}' for c in citations['case_citations']])}")

        if citations.get("acts"):
            formatted.append(f"Laws/Acts: {', '.join(citations['acts'])}")

        if citations.get("articles"):
            formatted.append(f"Articles: {', '.join([f'Art. {a}' for a in citations['articles']])}")

        if citations.get("rules"):
            formatted.append(f"Rules: {', '.join(citations['rules'])}")

        return "\n".join(formatted) if formatted else "No citations found"


def build_rag_chain(retriever, llm_provider: str = "groq") -> LegalRAGChain:
    """
    Factory function to build and return a ready-to-use RAG chain.

    Args:
        retriever: HybridRetriever instance
        llm_provider: "groq" (default), "google", or "openai"

    Returns:
        Initialized LegalRAGChain
    """
    return LegalRAGChain(
        retriever=retriever,
        llm_provider=llm_provider,
        use_conversation_memory=True,
        memory_type="buffer"
    )


if __name__ == "__main__":
    # Demo usage would require actual retriever instance
    print("\n" + "="*60)
    print("LegalRAGChain Demo")
    print("="*60)
    print("\nTo use:")
    print("1. Setup embedder and vector store (see STEP 3)")
    print("2. Create retriever: retriever = HybridRetriever(...)")
    print("3. Initialize chain: chain = LegalRAGChain(retriever)")
    print("4. Query: answer = chain.query('Your legal question')")
    print("5. Access: answer.answer, answer.sources, answer.citations")
    
    # Test citation extraction
    sample_text = """
    The Supreme Court in [2021] SCC 45 held that Section 302 IPC prescribes life imprisonment.
    This was followed by the High Court in [2022] SC 123. Additionally, Article 21 of the 
    Constitution provides protection. Rule 5 of Criminal Procedure Code also applies.
    """
    
    print("\n" + "="*60)
    print("Testing Citation Extraction:")
    print("="*60)
    
    citations = LegalCitationTracker.extract_all_citations(sample_text)
    print(LegalCitationTracker.format_citations(citations))
