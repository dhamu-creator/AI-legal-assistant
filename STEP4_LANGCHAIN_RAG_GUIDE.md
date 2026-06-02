# STEP 4: LangChain RAG Chain & LLM Integration - Complete Guide

## Overview

This step integrates the retriever with a Large Language Model (Claude or GPT-4) using LangChain to build a complete Retrieval-Augmented Generation (RAG) system.

## Architecture

```
Query Input
    ↓
Hybrid Retriever
    ↓ (Top-5 relevant docs)
Context Formatter
    ↓
Prompt Builder (with legal templates)
    ↓
LLM (Claude/GPT-4)
    ↓
Response Generation
    ↓
Citation Extractor
    ↓
Formatted Output with Citations
```

## Components Built

### 1. **src/generation/prompt_templates.py** (600+ lines) ✅

Legal-specific prompt templates for various legal QA scenarios.

**Classes:**
- `LegalPromptTemplates` - Collection of pre-built templates
- `LegalPromptBuilder` - Helper to build customized prompts

**Key Templates:**
- System prompt setting guardrails
- RAG prompt combining context + question
- Multi-turn conversation prompt
- Citation extraction prompt
- Case analysis prompt
- IPC section explanation prompt
- Comparison prompt
- Practical advice prompt

**Key Features:**
```python
✅ Legal-specific guardrails (prevents hallucination)
✅ Citation formatting rules
✅ Structural templates for different scenarios
✅ Automatic context formatting
✅ Chat history management
✅ Disclaimer generation
```

**Usage:**
```python
from src.generation.prompt_templates import LegalPromptTemplates, LegalPromptBuilder

# Use pre-built templates
templates = LegalPromptTemplates()
rag_prompt = templates.get_rag_prompt()

# Or build custom prompts with context
builder = LegalPromptBuilder(llm_provider="anthropic")
prompt = builder.build_rag_prompt_with_context(
    question="What is Section 302?",
    context_docs=[...]
)
```

### 2. **src/generation/llm_chain.py** (700+ lines) ✅

Main RAG chain orchestration with multi-turn conversation support.

**Classes:**
- `LegalAnswer` - Structured response dataclass
- `LegalRAGChain` - Main RAG pipeline
- `LegalCitationTracker` - Citation extraction from responses
- `build_rag_chain()` - Factory function

**LegalRAGChain Features:**
```python
✅ Supports Claude (Anthropic) and GPT-4 (OpenAI)
✅ Multi-turn conversations with memory
✅ Streaming responses
✅ Citation extraction
✅ Confidence scoring
✅ Token usage tracking
```

**Key Methods:**
```python
# Initialize
chain = LegalRAGChain(
    retriever=retriever,
    llm_provider="anthropic",
    temperature=0.2
)

# Query
answer = chain.query(
    question="What are my rights under Article 21?",
    top_k=5,
    use_memory=True,
    stream=False
)

# Access results
print(answer.question)        # Original question
print(answer.answer)          # LLM response
print(answer.sources)         # Retrieved documents
print(answer.citations)       # Extracted citations
print(answer.confidence_score) # Confidence 0-1
print(answer.tokens_used)     # Token counts

# Continue conversation
answer2 = chain.query("Tell me more about Section 21...")

# Clear history
chain.clear_memory()
```

### 3. **src/utils/citation_tracker.py** (500+ lines) ✅

Advanced citation extraction and formatting.

**Classes:**
- `Citation` - Structured citation dataclass
- `CitationType` - Citation type enum
- `CitationExtractor` - Extract citations from text
- `CitationFormatter` - Format citations for display
- `CitationLinker` - Link to case law databases

**Supported Citation Types:**
```python
✅ IPC Sections: "Section 302 IPC", "S. 420", "§ 302"
✅ Cases: "[2021] SCC 45", "AIR 2022 SC 123"
✅ Acts: "Indian Penal Code", "Criminal Procedure Code"
✅ Articles: "Article 21"
✅ Rules: "Rule 5"
✅ Schedules: "Schedule III"
✅ Amendments: "73rd Amendment"
```

**Usage:**
```python
from src.utils.citation_tracker import CitationExtractor, CitationFormatter

# Extract citations
extractor = CitationExtractor()
citations = extractor.extract_all(response_text)

# Format for display
formatter = CitationFormatter()
bibliography = formatter.format_bibliography(citations)
print(bibliography)

# Export as JSON
citations_json = formatter.create_citation_list(citations)
```

---

## Complete Workflow

### Setup

```python
# 1. Initialize vector store and retriever (from STEP 3)
from src.ingestion.embedder import LegalEmbedder
from src.retrieval.vector_store import ChromaDBStore, load_and_index_chunks

embedder = LegalEmbedder()
vector_store = ChromaDBStore("./data/chromadb")
retriever = load_and_index_chunks(
    "data/processed/chunks/embedded",
    vector_store,
    embedder
)

# 2. Initialize RAG chain (NEW - STEP 4)
from src.generation.llm_chain import LegalRAGChain

chain = LegalRAGChain(
    retriever=retriever,
    llm_provider="anthropic",  # or "openai"
    model_name="claude-sonnet-20240229",
    temperature=0.2,
    use_conversation_memory=True
)

# 3. Query the system
answer = chain.query("What is the punishment for murder under IPC?")

# 4. Display results
print(f"Question: {answer.question}")
print(f"\nAnswer:\n{answer.answer}")
print(f"\nCitations: {', '.join(answer.citations)}")
print(f"Confidence: {answer.confidence_score:.2%}")
print(f"\nSources:")
for source in answer.sources:
    print(f"  - {source['case_name']}: {source['text'][:100]}...")
```

### Multi-Turn Conversation

```python
# Conversation with memory
chain = LegalRAGChain(retriever, llm_provider="anthropic")

# First turn
ans1 = chain.query("What is Section 302 IPC?")
print(ans1.answer)

# Second turn - can reference first turn
ans2 = chain.query("What about Section 304?")
print(ans2.answer)

# Memory automatically persists context
ans3 = chain.query("How do these differ?")
print(ans3.answer)

# Clear memory for new conversation
chain.clear_memory()
```

### Citation Handling

```python
from src.utils.citation_tracker import CitationExtractor, CitationFormatter

# Extract all citations from answer
extractor = CitationExtractor()
citations = extractor.extract_all(answer.answer)

# Format as bibliography
formatter = CitationFormatter()
bib_markdown = formatter.format_bibliography(citations, format_type="markdown")
bib_html = formatter.format_bibliography(citations, format_type="html")

# Or use chain's built-in citation tracking
answer = chain.query(question)
extracted_cites = answer.citations  # Already extracted!
```

---

## Configuration

### Environment Variables (.env)

```bash
# LLM Provider Settings
LLM_PROVIDER=anthropic              # "anthropic" or "openai"
ANTHROPIC_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here

# Model Configuration
LLM_MODEL=claude-sonnet-20240229    # For Anthropic
# OR
LLM_MODEL=gpt-4-turbo-preview      # For OpenAI

# Generation Parameters
LLM_TEMPERATURE=0.2                 # 0.0-1.0 (lower = more focused)
LLM_MAX_TOKENS=1500                 # Maximum response length

# Memory Configuration
USE_CONVERSATION_MEMORY=true
MEMORY_TYPE=buffer                  # "buffer" or "summary"

# Retrieval Settings
TOP_K_CHUNKS=5                      # Docs to retrieve
SIMILARITY_THRESHOLD=0.5
```

### Python Configuration

```python
chain = LegalRAGChain(
    retriever=retriever,
    llm_provider="anthropic",       # Key choice
    model_name="claude-sonnet-20240229",
    temperature=0.2,                # Lower = more focused
    max_tokens=1500,                # Response length
    use_conversation_memory=True,
    memory_type="buffer"            # Full history kept
)
```

---

## Prompt Templates Explained

### System Prompt
Sets guardrails and defines the assistant's role.

```
You are an expert Indian legal assistant...
- Always cite specific sections and cases
- Never make up information
- Use official legal terminology
- State when unsure
```

### RAG Prompt
Combines context documents with user question.

```
CONTEXT: [Retrieved legal documents]
QUESTION: [User's question]
Answer based ONLY on provided context...
```

### Multi-Turn Prompt
Includes conversation history for continuity.

```
HISTORY: [Previous Q&A]
CONTEXT: [New retrieved docs]
QUESTION: [Current question]
Consider previous context if relevant...
```

---

## Response Structure

### LegalAnswer Object

```python
@dataclass
class LegalAnswer:
    question: str                    # User's question
    answer: str                      # LLM response
    sources: List[Dict]              # Retrieved documents
    citations: List[str]             # Extracted citations
    confidence_score: float          # 0.0-1.0
    model: str                       # Model used
    tokens_used: Dict                # {input, output}
```

### Example Response

```python
LegalAnswer(
    question="What is Section 302?",
    answer="Section 302 of the Indian Penal Code prescribes...",
    sources=[
        {
            "text": "State v. Sharma [2021]...",
            "case_name": "State v. Sharma",
            "court_name": "Supreme Court",
            "ipc_sections": ["Section 302"]
        }
    ],
    citations=["Section 302 IPC", "[2021] SCC 45"],
    confidence_score=0.87,
    model="claude-sonnet-20240229",
    tokens_used={"input": 425, "output": 187}
)
```

---

## Citation Extraction

### Automatic Extraction

Citations are automatically extracted from LLM responses:

```python
answer = chain.query("Question about Section 302...")

# Automatically extracted
print(answer.citations)  # ["Section 302 IPC", "[2021] SCC 45", ...]
```

### Manual Extraction

For other text:

```python
from src.utils.citation_tracker import CitationExtractor

extractor = CitationExtractor()
citations = extractor.extract_all(any_text)

# Results:
# citations["ipc_sections"]   → ["302", "304"]
# citations["cases"]          → [Citation objects]
# citations["acts"]           → [Citation objects]
# citations["articles"]       → [Citation objects]
```

### Citation Formatting

```python
from src.utils.citation_tracker import CitationFormatter

formatter = CitationFormatter()

# Format for display
formatted = formatter.format_bibliography(citations)
# Output:
# Cases Cited:
#   • [2021] SCC 45
#   • AIR 2022 SC 123
# IPC Sections Cited:
#   • Section 302 IPC
#   • Section 304 IPC
```

---

## Advanced Features

### Streaming Response

Stream LLM response token-by-token:

```python
# Note: Streaming returns full response, but prints as it generates
answer = chain.query(
    question="Long question requiring detailed response",
    stream=True
)
# Prints tokens as they arrive, then returns complete answer
print(answer.answer)
```

### Custom Prompts

Build custom prompts for specific scenarios:

```python
builder = LegalPromptBuilder()

# Case analysis
prompt = builder.build_case_analysis_prompt(case_docs)

# IPC section explanation
prompt = builder.build_ipc_section_prompt("302", case_docs)

# Practical advice
prompt = builder.build_practical_advice_prompt(
    situation="I was arrested without warrant...",
    context_docs=docs
)
```

### Memory Management

```python
# Check memory
summary = chain.get_memory_summary()
print(summary)

# Clear memory
chain.clear_memory()

# Disable memory (single-turn only)
chain_single = LegalRAGChain(
    retriever,
    use_conversation_memory=False
)
```

---

## Error Handling

```python
try:
    answer = chain.query("Question")
except Exception as e:
    logger.error(f"Query error: {str(e)}")
    # Fallback response
    print("Unable to generate response. Please check your API keys.")
```

---

## Performance Tips

1. **Lower Temperature**: Use 0.2 for factual legal answers
2. **Fewer Tokens**: Set max_tokens=1500 instead of 4096
3. **Retrieve More**: Use top_k=7-10 for complex questions
4. **Memory Type**: Use "buffer" for conversations, "summary" for long histories
5. **Batch Queries**: Process multiple questions together

---

## Legal Compliance

**Important Disclaimers:**
- This is NOT a substitute for professional legal counsel
- Responses are educational only
- Always verify with qualified lawyers
- System uses retrieved documents as source of truth
- May have inaccuracies or incomplete information

**Default Disclaimer:**
```
This is for educational purposes only, not legal advice. 
Please consult a qualified lawyer for legal matters.
```

---

## Integration with Frontend (Next Step)

This RAG chain integrates seamlessly with Streamlit frontend (Step 8):

```python
# In streamlit app
if user_question:
    answer = rag_chain.query(user_question)
    
    st.write(f"**Answer:** {answer.answer}")
    
    st.markdown("**Citations:**")
    for cite in answer.citations:
        st.write(f"- {cite}")
    
    with st.expander("View Sources"):
        for source in answer.sources:
            st.write(f"**{source['case_name']}**")
            st.write(source['text'][:200] + "...")
```

---

## Quick Reference

| Task | Code |
|------|------|
| Initialize | `chain = LegalRAGChain(retriever)` |
| Single query | `chain.query("Question")` |
| Multi-turn | `chain.query("Q1")` then `chain.query("Q2")` |
| Extract citations | `answer.citations` (automatic) |
| Format citations | `CitationFormatter.format_bibliography(citations)` |
| Clear memory | `chain.clear_memory()` |
| Get memory | `chain.get_memory_summary()` |
| Change model | `LegalRAGChain(..., model_name="gpt-4")` |
| Streaming | `chain.query(..., stream=True)` |

---

## What You Can Do Now

✅ Query legal questions with full context  
✅ Get responses with proper citations  
✅ Have multi-turn conversations  
✅ Extract and format citations automatically  
✅ Stream long responses  
✅ Access source documents  
✅ Track confidence scores  
✅ Monitor token usage  

---

## Next Steps

**STEP 5:** Citation Extraction & Post-Processing
- Extract citations from retrieved chunks
- Validate citations
- Link to case law databases

**STEP 6:** Hindi Language Support
- Add IndicBERT embeddings
- Multi-language input handling
- Translation utilities

**STEP 7:** Frontend Development
- Streamlit web interface
- Chat history management
- Export to PDF

**STEP 8:** Evaluation & Monitoring
- RAGAS metrics
- Citation accuracy checks
- Performance benchmarking

---

## Testing

Run the demo (includes citation extraction):

```bash
python quickstart.py
```

Or test individual components:

```python
# Test prompt builder
from src.generation.prompt_templates import LegalPromptBuilder
builder = LegalPromptBuilder()
print(builder.templates.get_system_prompt())

# Test citation extraction
from src.utils.citation_tracker import CitationExtractor
extractor = CitationExtractor()
cites = extractor.extract_all("Section 302 IPC and [2021] SCC 45...")
print(cites)
```

---

## Files Created

✅ src/generation/prompt_templates.py (600+ lines)
✅ src/generation/llm_chain.py (700+ lines)
✅ src/utils/citation_tracker.py (500+ lines)
✅ Updated __init__.py files with exports

**Total: 1800+ lines of production code**

---

## Status: ✅ COMPLETE

STEP 4 fully implemented with:
- Complete RAG chain with LLM integration
- Legal-specific prompt templates
- Multi-turn conversation support
- Citation extraction and formatting
- Error handling and logging
- Comprehensive documentation
