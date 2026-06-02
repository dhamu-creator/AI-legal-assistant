# -*- coding: utf-8 -*-
"""
test_groq.py
------------
Quick connectivity test for Groq API.
Run this BEFORE starting the Streamlit app to verify your key works.

Usage:
    python test_groq.py
"""

import os
import sys
from pathlib import Path

# Force UTF-8 output on Windows (fixes emoji encoding errors)
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# ── 1. Load .env from project root ────────────────────────────────────────────
try:
    from dotenv import load_dotenv, dotenv_values
except ImportError:
    print("[ERROR] python-dotenv not installed. Run: pip install python-dotenv")
    sys.exit(1)

env_path = Path(__file__).parent / ".env"

# Force-clear old keys from process environment before loading fresh values
for _k in ("GROQ_API_KEY", "GROQ_MODEL"):
    os.environ.pop(_k, None)

# Read values directly from file (bypasses any cached env)
_env_vals = dotenv_values(env_path)
for _k, _v in _env_vals.items():
    if _v is not None:
        os.environ[_k] = _v

load_dotenv(env_path, override=True)
print(f"[OK]  .env loaded from: {env_path}")

# ── 2. Read key ────────────────────────────────────────────────────────────────
api_key = os.getenv("GROQ_API_KEY")
model   = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

print("=" * 60)
print("  Groq API Connection Test")
print("=" * 60)

if not api_key or api_key.startswith("your"):
    print("[ERROR] GROQ_API_KEY not found or not set in .env")
    print("    Add the following line to your .env file:")
    print("    GROQ_API_KEY=gsk_...")
    sys.exit(1)

masked = api_key[:8] + "*" * (len(api_key) - 12) + api_key[-4:]
print(f"[OK]  Key loaded  : {masked}")
print(f"[OK]  Model       : {model}")

# ── 3. Import langchain-groq ──────────────────────────────────────────────────
try:
    from langchain_groq import ChatGroq
    print(f"[OK]  langchain-groq imported successfully")
except ImportError:
    print("\n[ERROR] langchain-groq not installed.")
    print("    Run: pip install langchain-groq")
    sys.exit(1)

# ── 4. Send test message ───────────────────────────────────────────────────────
print("\n[...] Sending test message to Groq...")
print("-" * 60)

try:
    llm = ChatGroq(
        model=model,
        groq_api_key=api_key,
        temperature=0.1,
    )

    response = llm.invoke(
        "Hello! Please reply with exactly: 'Groq is connected and working!'"
    )

    reply = response.content if hasattr(response, "content") else str(response)

    print(f"\n[GROQ REPLY]:\n\n    {reply}\n")
    print("=" * 60)
    print("[SUCCESS] CONNECTION SUCCESSFUL -- Groq is ready!")
    print("=" * 60)
    print("\nNext step -- run the app with:")
    print("    streamlit run app/streamlit_app.py")

except Exception as e:
    print(f"\n[ERROR] Connection failed: {e}")
    print("\nCommon fixes:")
    print("  1. Check GROQ_API_KEY is correct in .env")
    print("  2. Ensure internet access is available")
    print("  3. Run: pip install --upgrade langchain-groq")
    sys.exit(1)
