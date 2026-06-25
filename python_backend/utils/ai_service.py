import json
import logging
import os
import urllib.request
import inspect
from typing import Optional, Any

logger = logging.getLogger("ai_legal_assistant")

class AIService:
    """
    AI service abstraction using Groq as the primary LLM backend,
    with Ollama as an optional local fallback.
    """
    def __init__(self, test_mode: bool = False):
        self.test_mode = test_mode
        self.groq_api_key = os.getenv("GROQ_API_KEY")

    def call_groq(self, prompt: str, system_instruction: str = None, model: str = "llama-3.3-70b-versatile", require_json: bool = False) -> Optional[str]:
        """
        Call Groq API directly using urllib.
        """
        if not self.groq_api_key:
            return None
            
        messages = []
        if system_instruction:
            messages.append({"role": "system", "content": system_instruction})
        messages.append({"role": "user", "content": prompt})
        
        payload = {
            "model": model, 
            "messages": messages, 
            "temperature": 0.4
        }
        if require_json:
            payload["response_format"] = {"type": "json_object"}
            
        req = urllib.request.Request("https://api.groq.com/openai/v1/chat/completions", method="POST")
        req.add_header("Authorization", f"Bearer {self.groq_api_key}")
        req.add_header("Content-Type", "application/json")
        req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
        try:
            with urllib.request.urlopen(req, data=json.dumps(payload).encode("utf-8"), timeout=30) as res:
                body = json.loads(res.read().decode("utf-8"))
                return body["choices"][0]["message"]["content"]
        except Exception as e:
            logger.error(f"Groq API error: {e}")
            return None

    def call_groq_with_tools(self, prompt: str, tools: list, system_instruction: str = None, model: str = "llama-3.1-8b-instant") -> Optional[str]:
        """
        Call Groq API with tool execution loop.
        """
        if not self.groq_api_key:
            return None
            
        groq_tools = []
        tool_map = {}
        for t in tools:
            tool_map[t.__name__] = t
            sig = inspect.signature(t)
            props = {}
            req_params = []
            for name, p in sig.parameters.items():
                props[name] = {"type": "string"}
                if p.default == inspect.Parameter.empty:
                    req_params.append(name)
            groq_tools.append({
                "type": "function",
                "function": {
                    "name": t.__name__,
                    "description": inspect.getdoc(t) or "",
                    "parameters": {"type": "object", "properties": props, "required": req_params}
                }
            })
            
        messages = []
        if system_instruction:
            messages.append({"role": "system", "content": system_instruction})
        messages.append({"role": "user", "content": prompt})
        
        def make_request(msgs):
            req = urllib.request.Request("https://api.groq.com/openai/v1/chat/completions", method="POST")
            req.add_header("Authorization", f"Bearer {self.groq_api_key}")
            req.add_header("Content-Type", "application/json")
            req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
            data = {"model": model, "messages": msgs, "tools": groq_tools, "tool_choice": "auto"}
            with urllib.request.urlopen(req, data=json.dumps(data).encode("utf-8"), timeout=45) as res:
                return json.loads(res.read().decode("utf-8"))
        
        for _ in range(5):  # Max 5 tool calls chain
            try:
                response = make_request(messages)
            except urllib.error.HTTPError as e:
                err_body = e.read().decode("utf-8", errors="replace")
                logger.error(f"Groq API tool error: {e} - Body: {err_body}")
                return None
            except Exception as e:
                logger.error(f"Groq API tool error: {e}")
                return None
                
            msg = response["choices"][0]["message"]
            messages.append(msg)
            
            if msg.get("tool_calls"):
                for tc in msg["tool_calls"]:
                    func_name = tc["function"]["name"]
                    args = json.loads(tc["function"]["arguments"])
                    tool_res = ""
                    if func_name in tool_map:
                        try:
                            result = tool_map[func_name](**args)
                            tool_res = json.dumps(result) if isinstance(result, (dict, list)) else str(result)
                        except Exception as e:
                            tool_res = f"Error executing tool: {str(e)}"
                    else:
                        tool_res = "Tool not found"
                        
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tc["id"],
                        "name": func_name,
                        "content": tool_res
                    })
            else:
                return msg.get("content", "")
                
        return "Error: Tool execution limit reached"

    def call_ollama(self, prompt: str, require_json: bool = False) -> Optional[str]:
        """
        Fallback call to local Ollama service if available
        """
        ollama_url = "http://127.0.0.1:11434"
        try:
            req = urllib.request.Request(f"{ollama_url}/api/tags", method="GET")
            with urllib.request.urlopen(req, timeout=0.5) as response:
                models_data = json.loads(response.read().decode("utf-8"))
            
            models = [m["name"] for m in models_data.get("models", [])]
            if not models:
                logger.warning("Ollama is running but no models are installed.")
                return None
                
            preferred = ["qwen2.5:latest", "qwen2.5", "llama3:8b", "llama3", "gemma3:latest", "gemma3"]
            selected_model = None
            for pref in preferred:
                for m in models:
                    if pref in m or m.startswith(pref):
                        selected_model = m
                        break
                if selected_model:
                    break
            
            if not selected_model:
                for m in models:
                    if "embed" not in m.lower():
                        selected_model = m
                        break
            if not selected_model:
                selected_model = models[0]
                
            logger.info(f"Ollama fallback selected model: {selected_model}")
            
            payload = {
                "model": selected_model,
                "system": "You are a highly detailed and knowledgeable Indian AI Legal Assistant. Always provide comprehensive, step-by-step, and detailed explanations using BNS, BNSS, IPC, and other relevant Indian laws. Never give short answers.",
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.4,
                    "top_p": 0.7,
                    "num_predict": 2048
                }
            }
            if require_json:
                payload["format"] = "json"
                
            body = json.dumps(payload).encode("utf-8")
            headers = {"Content-Type": "application/json"}
            
            req_gen = urllib.request.Request(f"{ollama_url}/api/generate", data=body, headers=headers, method="POST")
            with urllib.request.urlopen(req_gen, timeout=45.0) as response_gen:
                res_data = json.loads(response_gen.read().decode("utf-8"))
                
            return res_data.get("response", "").strip()
            
        except Exception as e:
            logger.warning(f"Ollama fallback service failed or unreachable: {e}")
            return None

    def generate_content(self, prompt: str, model: Optional[str] = None) -> Optional[str]:
        if self.test_mode: return None
        
        # 1. Try Groq (primary)
        if self.groq_api_key:
            res = self.call_groq(prompt)
            if res: return res.strip()

        # 2. Try Ollama (local fallback)
        logger.info("Attempting Ollama local fallback...")
        ollama_res = self.call_ollama(prompt, require_json=False)
        if ollama_res: return ollama_res
        return "Error: All AI backends failed."

    def generate_json(self, prompt: str, model: Optional[str] = None) -> Optional[dict]:
        if self.test_mode: return None
        
        text = None
        # 1. Try Groq (primary)
        if self.groq_api_key:
            text = self.call_groq(prompt, require_json=True)
            
        # 2. Try Ollama (local fallback)
        if not text:
            logger.info("Attempting Ollama local JSON fallback...")
            text = self.call_ollama(prompt, require_json=True)

        if not text:
            return None

        # Clean markdown wrappers
        cleaned_text = text.strip()
        if cleaned_text.startswith("```json"): cleaned_text = cleaned_text[7:]
        elif cleaned_text.startswith("```"): cleaned_text = cleaned_text[3:]
        if cleaned_text.endswith("```"): cleaned_text = cleaned_text[:-3]

        try:
            return json.loads(cleaned_text.strip())
        except Exception as e:
            logger.error(f"JSON Parsing Error: {e}. Raw response: {text}")
            return None

    def generate_with_tools(self, prompt: str, tools: list, system_instruction: str = None, model: Optional[str] = None) -> Optional[str]:
        if self.test_mode: return None
        
        # 1. Try Groq with tools (primary)
        if self.groq_api_key:
            res = self.call_groq_with_tools(prompt, tools, system_instruction)
            if res: return res

        return "Error: Tool execution failed - no AI backend available."
