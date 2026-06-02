"""
Prompt Templates for Legal Domain
Specialized prompts designed for accurate legal question answering with citations.
"""

from typing import List, Dict, Optional

# Try newer import paths first, fallback to older ones
try:
    from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
    from langchain_core.prompts.few_shot import FewShotChatMessagePromptTemplate
except ImportError:
    try:
        from langchain.prompts import PromptTemplate, ChatPromptTemplate
        from langchain.prompts.few_shot import FewShotChatMessagePromptTemplate
    except ImportError:
        # Fallback - define minimal templates
        class PromptTemplate:
            def __init__(self, template, input_variables):
                self.template = template
                self.input_variables = input_variables
        
        class ChatPromptTemplate:
            def __init__(self, messages):
                self.messages = messages
        
        class FewShotChatMessagePromptTemplate:
            pass


class LegalPromptTemplates:
    """
    Collection of prompt templates optimized for legal question answering.
    Ensures responses are grounded in retrieved context and properly cited.
    """

    @staticmethod
    def get_system_prompt() -> str:
        """
        System prompt for legal assistant.
        Sets context and guardrails for the LLM.
        """
        return """You are an expert Indian legal assistant specializing in:
- Indian Penal Code (IPC) sections and their application
- Supreme Court and High Court judgments
- Legal precedents and case law analysis
- Constitutional law and statutory provisions

Your role is to:
1. Answer legal questions based ONLY on the provided context
2. Always cite specific sections, cases, and years
3. Use official legal terminology and proper citations
4. Clearly distinguish between law and legal interpretation
5. Highlight uncertainties and legal complexities

CRITICAL RULES:
- NEVER make up case names, years, or section numbers
- ALWAYS cite the source: case name, year, court, and section
- If unsure about information, explicitly state: "Based on available information..."
- When citing IPC sections, use format: "Section XXX IPC"
- When citing cases, use format: "[YYYY] Reporter Page" (e.g., [2021] SCC 45, AIR 2022 SC 123)
- Explain implications clearly in simple language
- Add disclaimer: "This is for educational purposes only, not legal advice"

OUTPUT FORMAT:
1. Direct answer to the question
2. Legal basis with citations
3. Relevant case law references
4. Important legal principles involved
5. Limitations and considerations"""

    @staticmethod
    def get_rag_prompt() -> ChatPromptTemplate:
        """
        RAG prompt template combining context and query.
        Used for retrieval-augmented generation queries.
        """
        prompt_text = """You are an expert Indian legal assistant. Answer the following question based ONLY on the provided legal context.

LEGAL CONTEXT (from case law and IPC):
{context}

QUESTION: {question}

INSTRUCTIONS:
1. Answer based only on the context provided above
2. Always cite specific sections, cases, and years
3. Format case citations as: [YYYY] Court Reporter PageNo (e.g., [2021] SCC 45)
4. Format IPC citations as: Section XXX IPC
5. If information is not in context, state clearly: "The provided documents do not contain information about..."
6. Explain legal concepts in clear, understandable language
7. Highlight important case precedents and their relevance

RESPONSE:
"""
        
        return ChatPromptTemplate.from_template(prompt_text)

    @staticmethod
    def get_multi_turn_prompt() -> ChatPromptTemplate:
        """
        Prompt template for multi-turn conversations with conversation history.
        """
        prompt_text = """You are an expert Indian legal assistant in a conversation about legal matters.

CONVERSATION HISTORY:
{chat_history}

NEW LEGAL CONTEXT (for this question):
{context}

USER QUESTION: {question}

Remember:
- Reference previous conversation if relevant
- Cite all legal authorities (cases, sections)
- Maintain consistency with earlier responses
- Only use information from provided context
- State disclaimers clearly

RESPONSE:
"""
        
        return ChatPromptTemplate.from_template(prompt_text)

    @staticmethod
    def get_citation_extraction_prompt() -> str:
        """
        Prompt to extract citations from legal text.
        Used for post-processing LLM responses.
        """
        return """Extract all legal citations from the following text. Format them as:
- IPC: Section XXX IPC
- Cases: [YYYY] Reporter PageNo (e.g., [2021] SCC 45)
- Acts/Laws: Act Name, Section YYY

Text:
{text}

Citations found:"""

    @staticmethod
    def get_case_analysis_prompt() -> str:
        """
        Detailed case analysis prompt.
        """
        return """Analyze the following legal case based on the provided context:

CASE DETAILS:
{context}

Provide analysis in this structure:
1. Case Name and Citation
2. Court and Judgment Date
3. Key Facts
4. Legal Issues Involved
5. Court's Ruling
6. Key Precedents Cited
7. Relevance to Current Legal Framework
8. Important Principles Established

Ensure all citations are accurate and properly formatted."""

    @staticmethod
    def get_ipc_section_prompt() -> str:
        """
        Prompt for explaining specific IPC sections.
        """
        return """Explain the following IPC section comprehensively:

SECTION: {section}

CONTEXT FROM JUDGMENTS:
{context}

Provide:
1. Section Number and Full Text
2. Ingredients/Essential Elements (if applicable)
3. Punishment/Consequences
4. Related Sections
5. Key Supreme Court Interpretations
6. Landmark Judgments citing this section
7. Common Applications and Examples
8. When This Section Does NOT Apply

Format all citations properly and use official legal language."""

    @staticmethod
    def get_comparison_prompt() -> str:
        """
        Prompt for comparing legal provisions or cases.
        """
        return """Compare the following legal concepts/provisions based on provided context:

ITEM 1: {item1}
ITEM 2: {item2}

RELEVANT CONTEXT:
{context}

Provide:
1. Similarities
2. Key Differences
3. When Each Applies
4. Case Examples for Each
5. Which is More Stringent/Favorable
6. Related Provisions
7. Legal Implications of Differences

Include proper citations throughout."""

    @staticmethod
    def get_practical_advice_prompt() -> str:
        """
        Prompt for practical legal advice based on fact scenario.
        """
        return """Based on the following legal situation and provided case law, provide guidance:

SITUATION:
{situation}

APPLICABLE LAW (from provided context):
{context}

Provide:
1. Applicable Laws/Sections
2. Legal Position/Analysis
3. Rights and Obligations
4. Potential Outcomes (citing relevant cases)
5. Recommended Actions
6. Important Considerations

DISCLAIMER: This is general legal information based on case law, not specific legal advice. Consult a lawyer for case-specific advice."""

    @staticmethod
    def get_legal_research_prompt() -> str:
        """
        Prompt for comprehensive legal research on a topic.
        """
        return """Conduct comprehensive legal research on: {topic}

AVAILABLE SOURCES:
{context}

Provide:
1. Legal Framework (relevant laws and sections)
2. Key Supreme Court Judgments
3. High Court Precedents
4. Evolution of Legal Interpretation
5. Current Legal Position
6. Areas of Ambiguity/Dispute
7. Recent Developments
8. Practical Implications

Cite all sources properly with case names, years, and page numbers."""


class LegalPromptBuilder:
    """
    Helper class to build customized prompts for different scenarios.
    """

    def __init__(self, llm_provider: str = "google"):
        """
        Initialize prompt builder.

        Args:
            llm_provider: "google" (Gemini) or "openai" (GPT)
        """
        self.llm_provider = llm_provider
        self.templates = LegalPromptTemplates()

    def build_rag_prompt_with_context(
        self,
        question: str,
        context_docs: List[Dict],
        use_chat_format: bool = True
    ) -> str:
        """
        Build a complete RAG prompt with formatted context.
        
        Args:
            question: User question
            context_docs: Retrieved documents with metadata
            use_chat_format: Use chat format (True) or text format (False)
        
        Returns:
            Formatted prompt string
        """
        # Format context documents
        formatted_context = self._format_context_docs(context_docs)
        
        prompt = self.templates.get_rag_prompt()
        return prompt.format(
            context=formatted_context,
            question=question
        )

    def build_multi_turn_prompt(
        self,
        question: str,
        context_docs: List[Dict],
        chat_history: List[Dict]
    ) -> str:
        """
        Build prompt for multi-turn conversation.
        
        Args:
            question: Current user question
            context_docs: Retrieved context for this question
            chat_history: Previous conversation turns
        
        Returns:
            Formatted prompt string
        """
        formatted_context = self._format_context_docs(context_docs)
        formatted_history = self._format_chat_history(chat_history)
        
        prompt = self.templates.get_multi_turn_prompt()
        return prompt.format(
            context=formatted_context,
            question=question,
            chat_history=formatted_history
        )

    def build_case_analysis_prompt(
        self,
        case_docs: List[Dict]
    ) -> str:
        """
        Build prompt for case analysis.
        
        Args:
            case_docs: Case law documents
        
        Returns:
            Formatted prompt string
        """
        formatted_context = self._format_context_docs(case_docs)
        return self.templates.get_case_analysis_prompt().format(
            context=formatted_context
        )

    def build_ipc_section_prompt(
        self,
        section_num: str,
        context_docs: List[Dict]
    ) -> str:
        """
        Build prompt for explaining IPC section.
        
        Args:
            section_num: IPC section number (e.g., "302")
            context_docs: Related case law
        
        Returns:
            Formatted prompt string
        """
        formatted_context = self._format_context_docs(context_docs)
        return self.templates.get_ipc_section_prompt().format(
            section=f"Section {section_num} IPC",
            context=formatted_context
        )

    def _format_context_docs(self, docs: List[Dict]) -> str:
        """
        Format retrieved documents for inclusion in prompt.
        
        Args:
            docs: List of document dictionaries
        
        Returns:
            Formatted context string
        """
        formatted = []
        
        for i, doc in enumerate(docs, 1):
            # Extract key information
            text = doc.get("text", "")
            case_name = doc.get("case_name", "Unknown")
            court = doc.get("court_name", "Unknown Court")
            citations = doc.get("case_citations", [])
            ipc_sections = doc.get("ipc_sections", [])
            
            # Build formatted entry
            entry = f"""
[SOURCE {i}]
Case: {case_name}
Court: {court}
IPC Sections: {', '.join(ipc_sections) if ipc_sections else 'N/A'}
Citations: {', '.join(citations) if citations else 'N/A'}

Content:
{text[:500]}...

---"""
            formatted.append(entry)
        
        return "\n".join(formatted)

    def _format_chat_history(self, history: List[Dict]) -> str:
        """
        Format chat history for inclusion in prompt.
        
        Args:
            history: List of conversation turns
        
        Returns:
            Formatted history string
        """
        formatted = []
        
        for turn in history:
            role = turn.get("role", "user").upper()
            content = turn.get("content", "")
            formatted.append(f"{role}: {content}")
        
        return "\n".join(formatted)


# Predefined prompt templates as simple strings
LEGAL_QA_TEMPLATE = """You are an expert Indian legal assistant. Answer based on provided legal context.

CONTEXT:
{context}

QUESTION: {question}

Answer with proper citations. Use format: [YYYY] Reporter Page for cases, Section X IPC for statutes."""

LEGAL_EXPLANATION_TEMPLATE = """Explain this legal concept:

CONCEPT: {concept}

CONTEXT FROM CASES:
{context}

Provide clear explanation with:
1. Definition
2. Legal basis (cases/sections)
3. Key principles
4. Practical examples
5. Related concepts"""

LEGAL_COMPARISON_TEMPLATE = """Compare these legal items:

ITEM 1: {item1}
ITEM 2: {item2}

CONTEXT:
{context}

Show similarities, differences, and when each applies."""


if __name__ == "__main__":
    # Example usage
    print("\n" + "="*60)
    print("Legal Prompt Templates Demo")
    print("="*60)
    
    templates = LegalPromptTemplates()
    
    print("\nSystem Prompt:")
    print(templates.get_system_prompt()[:300] + "...")
    
    print("\nRAG Prompt Template:")
    rag_prompt = templates.get_rag_prompt()
    print(f"Format variables: {rag_prompt.input_variables}")
    
    # Example with builder
    builder = LegalPromptBuilder()
    
    sample_context = [
        {
            "text": "Section 302 IPC prescribes life imprisonment for murder",
            "case_name": "State v. Sharma",
            "court_name": "Supreme Court",
            "case_citations": ["[2021] SCC 45"],
            "ipc_sections": ["Section 302"]
        }
    ]
    
    prompt = builder.build_rag_prompt_with_context(
        question="What is the punishment for murder?",
        context_docs=sample_context
    )
    
    print("\n" + "="*60)
    print("Built RAG Prompt:")
    print("="*60)
    print(prompt[:500] + "...\n")
