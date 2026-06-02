#!/usr/bin/env python3
"""
Complete diagnostic script for AI Legal Assistant
"""
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path.cwd()))

# Load .env manually
env_path = Path('.env')
if env_path.exists():
    with open(env_path) as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                try:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip().strip('"\'')
                except:
                    pass

print('=' * 60)
print('ENVIRONMENT CHECK')
print('=' * 60)
print(f'LLM_PROVIDER: {os.getenv("LLM_PROVIDER")}')
print(f'GEMINI_API_KEY: {bool(os.getenv("GEMINI_API_KEY"))}')
print()

print('=' * 60)
print('CHECKING BACKEND IMPORTS')
print('=' * 60)

try:
    from src.ingestion.embedder import LegalEmbedder
    print('✓ LegalEmbedder imported')
except Exception as e:
    print(f'✗ LegalEmbedder error: {e}')
    import traceback
    traceback.print_exc()

try:
    from src.retrieval.vector_store import ChromaDBStore, load_and_index_chunks
    print('✓ ChromaDBStore imported')
except Exception as e:
    print(f'✗ ChromaDBStore error: {e}')
    import traceback
    traceback.print_exc()

try:
    from src.generation.llm_chain import LegalRAGChain
    print('✓ LegalRAGChain imported')
except Exception as e:
    print(f'✗ LegalRAGChain error: {e}')
    import traceback
    traceback.print_exc()

print()
print('=' * 60)
print('DATA FILES CHECK')
print('=' * 60)
print(f'ChromaDB exists: {Path("./data/chromadb").exists()}')
print(f'Embedded chunks exist: {Path("./data/processed/chunks/embedded").exists()}')

if Path("./data/processed/chunks/embedded").exists():
    files = list(Path("./data/processed/chunks/embedded").glob("*_embedded.json"))
    print(f'Embedded files count: {len(files)}')
    for f in files:
        print(f'  - {f.name}')

print()
print('=' * 60)
print('CHECKING GEMINI SUPPORT')
print('=' * 60)

try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    print('✓ langchain_google_genai available')
except ImportError:
    print('✗ langchain_google_genai NOT installed')

try:
    from langchain.memory import ConversationBufferMemory
    print('✓ langchain.memory available')
except:
    print('✗ langchain.memory not available')
    try:
        from langchain_community.memory import ConversationBufferMemory
        print('  ✓ But langchain_community.memory available')
    except:
        print('  ✗ And langchain_community.memory not available')

print()
print('=' * 60)
print('TESTING INITIALIZATION')
print('=' * 60)

try:
    embedder = LegalEmbedder()
    print('✓ LegalEmbedder initialized')
except Exception as e:
    print(f'✗ LegalEmbedder init error: {e}')

try:
    vector_store = ChromaDBStore("./data/chromadb")
    print('✓ ChromaDBStore initialized')
except Exception as e:
    print(f'✗ ChromaDBStore init error: {e}')

try:
    retriever = load_and_index_chunks(
        "data/processed/chunks/embedded",
        vector_store,
        embedder
    )
    print(f'✓ Retriever initialized with {len(retriever.documents) if hasattr(retriever, "documents") else "?"} documents')
except Exception as e:
    print(f'✗ Retriever init error: {e}')
    import traceback
    traceback.print_exc()

try:
    chain = LegalRAGChain(
        retriever=retriever,
        llm_provider="google",
        temperature=0.2,
        use_conversation_memory=True
    )
    print('✓ LegalRAGChain initialized')
except Exception as e:
    print(f'✗ LegalRAGChain init error: {e}')
    import traceback
    traceback.print_exc()

print()
print('=' * 60)
print('DIAGNOSTIC COMPLETE')
print('=' * 60)
