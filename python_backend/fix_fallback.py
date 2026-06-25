import re

def fix_agentic():
    file_path = "c:/placement project/AI Legel Assistant/python_backend/agentic_system.py"
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # We need to replace self.get_general_inquiry_fallback(message, language) with a standard message
    new_content = content.replace(
        "self.get_general_inquiry_fallback(message, language)",
        "f\"I am an AI Legal Assistant. Please provide more details about your incident or legal issue so I can assist you better. ({language})\""
    )
    
    # We also want to make sure it's valid
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)

if __name__ == "__main__":
    fix_agentic()
