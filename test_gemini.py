# -*- coding: utf-8 -*-
"""
test_gemini.py
--------------
Quick connectivity test for Google Gemini API.
Run this BEFORE starting the Streamlit app to verify your key works.

Usage:
    python test_gemini.py
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
for _k in ("GEMINI_API_KEY", "GOOGLE_API_KEY", "GEMINI_MODEL"):
    os.environ.pop(_k, None)

# Read values directly from file (bypasses any cached env)
_env_vals = dotenv_values(env_path)
for _k, _v in _env_vals.items():
    if _v is not None:
        os.environ[_k] = _v

load_dotenv(env_path, override=True)
print(f"[OK]  .env loaded from: {env_path}")

# ── 2. Read key ────────────────────────────────────────────────────────────────
api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
model   = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

print("=" * 60)
print("  Gemini API Connection Test")
print("=" * 60)

if not api_key:
    print("[ERROR] GEMINI_API_KEY not found in .env")
    print("    Add the following line to your .env file:")
    print("    GEMINI_API_KEY=AIzaSy...")
    sys.exit(1)

masked = api_key[:8] + "*" * (len(api_key) - 12) + api_key[-4:]
print(f"[OK]  Key loaded  : {masked}")
print(f"[OK]  Model       : {model}")

# ── 3. Import langchain-google-genai ──────────────────────────────────────────
try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    print(f"[OK]  langchain-google-genai imported successfully")
except ImportError:
    print("\n[ERROR] langchain-google-genai not installed.")
    print("    Run: pip install langchain-google-genai google-generativeai")
    sys.exit(1)

# ── 4. Send test message ───────────────────────────────────────────────────────
print("\n[...] Sending test message to Gemini...")
print("-" * 60)

try:
    llm = ChatGoogleGenerativeAI(
        model=model,
        google_api_key=api_key,
        temperature=0.1,
        convert_system_message_to_human=True,
    )

    response = llm.invoke(
        "Hello! Please reply with exactly: 'Gemini is connected and working!'"
    )

    reply = response.content if hasattr(response, "content") else str(response)

    print(f"\n[GEMINI REPLY]:\n\n    {reply}\n")
    print("=" * 60)
    print("[SUCCESS] CONNECTION SUCCESSFUL -- Gemini is ready!")
    print("=" * 60)
    print("\nNext step -- run the app with:")
    print("    streamlit run app/streamlit_app.py")

except Exception as e:
    print(f"\n[ERROR] Connection failed: {e}")
    print("\nCommon fixes:")
    print("  1. Check GEMINI_API_KEY is correct in .env")
    print("  2. Ensure internet access is available")
    print("  3. Run: pip install --upgrade langchain-google-genai google-generativeai")
    sys.exit(1)
