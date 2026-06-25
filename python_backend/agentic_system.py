import json
import logging
from datetime import datetime
from uuid import uuid4
from typing import Any
import re

# Import legal data and functions from existing knowledge base
from legal_knowledge_base import CRIME_TO_SECTIONS, get_legal_section, search_judgements, SAMPLE_JUDGEMENTS, search_sections
from utils.ai_service import AIService
from utils.rag_service import RAGService
from utils.external_api import ExternalAPIService

logger = logging.getLogger("ai_legal_assistant")

def fallback_detect_crime(text: str) -> str:
    """Heuristic fallback classifier. Returns GeneralInquiry for procedural/generic questions."""
    text = text.lower()
    # Procedural / generic questions should NOT be misclassified as a specific crime
    if any(w in text for w in ["file", "complaint", "fir", "report", "police station", "procedure", "how to", "what is", "rights", "process", "bail", "anticipatory"]):
        return "GeneralInquiry"
    # Most severe crimes first (order matters for overlapping keywords)
    if any(w in text for w in ["terror", "bomb", "explosive", "jihad"]):
        return "Terrorism"
    if any(w in text for w in ["kill", "murder", "dead", "homicide", "assassinate", "shoot", "stab", "slit throat", "buried", "body"]):
        return "Murder"
    if any(w in text for w in ["rape", "sexual assault", "molest", "gang rape", "penetrat"]):
        return "SexualAssault"
    if any(w in text for w in ["kidnap", "abduct", "ransom", "hostage", "missing child", "taken away"]):
        return "Kidnapping"
    if any(w in text for w in ["acid attack", "acid throw", "disfigure"]):
        return "AcidAttack"
    if any(w in text for w in ["child abuse", "child porn", "pocso", "minor abuse", "pedophil"]):
        return "ChildAbuse"
    if any(w in text for w in ["dowry death", "bride burn", "dowry harass", "dahej"]):
        return "DowryDeath"
    if any(w in text for w in ["drug", "narcotic", "ganja", "cocaine", "heroin", "charas", "ndps", "cannabis", "smack"]):
        return "DrugOffenses"
    if any(w in text for w in ["scam", "telegram", "whatsapp", "job scam", "loan scam", "phish", "upi", "electricity bill"]):
        return "Scam"
    if any(w in text for w in ["hack", "online", "otp", "bank transfer", "fraud", "cyber"]):
        return "CyberFraud"
    if any(w in text for w in ["robbery", "dacoity", "loot", "armed robbery"]):
        return "Robbery"
    if any(w in text for w in ["stole", "stolen", "theft", "pickpocket", "snatch", "shoplifting"]):
        return "Theft"
    if any(w in text for w in ["beat", "assault", "attack", "hit", "punch", "kick", "slap", "grievous hurt"]):
        return "PhysicalAssault"
    if any(w in text for w in ["domestic", "wife beating", "husband beat", "spouse", "dowry", "cruelty by husband"]):
        return "DomesticViolence"
    if any(w in text for w in ["stalk", "follow", "tease", "eve teas"]):
        return "Stalking"
    if any(w in text for w in ["harass", "bully", "workplace harass"]):
        return "Harassment"
    if any(w in text for w in ["blackmail", "extort", "threaten", "threat"]):
        return "Blackmail"
    if any(w in text for w in ["identity", "impersonate", "fake id", "fake profile", "fake account"]):
        return "IdentityTheft"
    if any(w in text for w in ["forgery", "forge", "fake document", "counterfeit", "fake signature"]):
        return "Forgery"
    if any(w in text for w in ["drunk driv", "drunken driv", "drink and driv", "dui"]):
        return "DrunkenDriving"
    if any(w in text for w in ["road accident", "hit and run", "vehicle accident", "rash driving", "negligent driving"]):
        return "RoadAccidentDeath"
    if any(w in text for w in ["caste", "dalit", "sc/st", "atrocity", "untouchab"]):
        return "CasteAtrocity"
    if any(w in text for w in ["defam", "slander", "libel", "reputation"]):
        return "Defamation"
    if any(w in text for w in ["money", "finance", "cheat", "invest", "ponzi", "misappropriat"]):
        return "FinancialFraud"
    if any(w in text for w in ["confine", "lock", "imprison", "detain"]):
        return "WrongfulConfinement"
    if any(w in text for w in ["voyeur", "peeping", "hidden camera", "spy cam"]):
        return "Voyeurism"
    if any(w in text for w in ["poison", "sedat", "drug in drink"]):
        return "Poisoning"
    return "GeneralInquiry"



class AgenticSystem:
    def __init__(self, db_interface, test_mode=False):
        self.db = db_interface
        self.test_mode = test_mode
        self.ai_service = AIService(test_mode=test_mode)
        self.rag_service = RAGService()

    def detect_language(self, text: str, default_lang: str = "English") -> str:
        # First check for native scripts to avoid API calls
        if any(c in text for c in [chr(i) for i in range(0x0b80, 0x0c00)]): # Tamil
            return "Tamil"
        if any(c in text for c in [chr(i) for i in range(0x0900, 0x0980)]): # Hindi / Devanagari
            return "Hindi"
        if any(c in text for c in [chr(i) for i in range(0x0c00, 0x0c80)]): # Telugu
            return "Telugu"
        if any(c in text for c in [chr(i) for i in range(0x0c80, 0x0d00)]): # Kannada
            return "Kannada"
        if any(c in text for c in [chr(i) for i in range(0x0d00, 0x0d80)]): # Malayalam
            return "Malayalam"

        # If it's Latin script (including English, Tanglish, Hinglish, etc.), use the LLM to detect the language.
        # But only do it if the length of the query is substantial (e.g. > 10 chars) to save rate limits
        if len(text.strip()) < 10:
            return default_lang

        prompt = (
            f"Analyze the language of the following user query. "
            f"Classify it into EXACTLY ONE of these languages: 'English', 'Tamil', 'Hindi', 'Telugu', 'Malayalam', 'Kannada'. "
            f"If it is mixed or written in Roman/English script (transliterated like Tanglish, Hinglish, etc.), you MUST return the name of the underlying regional language (e.g. for Tanglish like 'yendha languagela input tharaaro' return 'Tamil', for 'mujhe help chahiye' return 'Hindi'). "
            f"If the text is purely in English or a general greeting in English, return 'English'.\n\n"
            f"Text: \"{text}\"\n\n"
            f"Return ONLY the exact language name and nothing else."
        )
        try:
            detected = self.ai_service.generate_content(prompt)
            if detected:
                detected_clean = detected.replace("`", "").replace("\"", "").replace("'", "").strip()
                valid_languages = ["English", "Tamil", "Hindi", "Telugu", "Malayalam", "Kannada"]
                for lang in valid_languages:
                    if lang.lower() in detected_clean.lower():
                        return lang
        except Exception as e:
            logger.error(f"Error detecting language with LLM: {e}")
        
        return default_lang

    def log_agent_action(self, user_id: str, session_id: str, agent_name: str, input_data: Any, output_data: Any):
        log_id = uuid4().hex[:24]
        log_entry = {
            "id": log_id,
            "userId": user_id,
            "sessionId": session_id,
            "agentName": agent_name,
            "input": input_data,
            "output": output_data,
            "timestamp": datetime.now().isoformat()
        }
        # Save to database (resolves case-insensitively via __getitem__)
        self.db.agent_logs[log_id] = log_entry

    # Comprehensive Legal Analysis Agent (Replacing Agents 2-14)
    def agent_comprehensive_analysis(self, incident_text: str, language: str = "English") -> dict:
        if self.test_mode:
            return {
                "crime_category": "GeneralInquiry",
                "severity": {"severity": "Low", "score": 10, "reason": ["Test mode"], "urgency": "None", "priority": "Low"},
                "evidence": ["ID Proof"],
                "document_requirements": ["Written complaint"],
                "investigation_support": "Contact local police",
                "timeline": [{"stage": "FIR filing", "timeline": "Day 1", "description": "Lodge FIR", "section": "BNSS 173"}],
                "specialized_advice": {}
            }

        prompt = (
            f"You are the Comprehensive Legal Analysis Agent. Analyze the following user incident:\n"
            f"Incident: \"{incident_text}\"\n\n"
            f"1. Classify it into EXACTLY ONE of the following Indian crime categories (or 'GeneralInquiry'):\n"
            f"[{', '.join(CRIME_TO_SECTIONS.keys())}]\n"
            f"2. Assess the severity, urgency, and priority.\n"
            f"3. Recommend specific evidence and documents to collect.\n"
            f"4. Provide a step-by-step procedural timeline from reporting to trial.\n"
            f"5. If the incident involves Scam, CyberFraud, Harassment, ConsumerRights, Kidnapping, or Lost Documents, provide relevant 'specialized_advice' in the JSON (e.g. scam indicators, emergency cyber steps, safety guidance).\n\n"
            f"Respond in {language} EXACTLY with this JSON schema:\n"
            f"{{\n"
            f"  \"crime_category\": \"CategoryName\",\n"
            f"  \"severity\": {{\n"
            f"    \"severity\": \"Critical/High/Medium/Low\",\n"
            f"    \"score\": 85,\n"
            f"    \"reason\": [\"Reason 1\"],\n"
            f"    \"urgency\": \"Urgency guidance\",\n"
            f"    \"priority\": \"Critical/High/Medium/Low\"\n"
            f"  }},\n"
            f"  \"evidence\": [\"Evidence Item 1\"],\n"
            f"  \"document_requirements\": [\"Doc Req 1\"],\n"
            f"  \"investigation_support\": \"Support guidance\",\n"
            f"  \"timeline\": [\n"
            f"    {{\"stage\": \"Name\", \"timeline\": \"Time\", \"description\": \"Desc\", \"section\": \"Sec\"}}\n"
            f"  ],\n"
            f"  \"specialized_advice\": {{\n"
            f"    \"scam_probability\": 90,\n"
            f"    \"scam_indicators\": [\"Indicator\"],\n"
            f"    \"cyber_emergency_steps\": [\"Step 1\"],\n"
            f"    \"safety_guidance\": \"Guidance\",\n"
            f"    \"consumer_rights_info\": \"Info\",\n"
            f"    \"missing_person_contacts\": [\"100\"],\n"
            f"    \"lost_document_procedure\": \"Procedure\"\n"
            f"  }}\n"
            f"}}\n"
            f"Do not include markdown blocks like ```json."
        )
        res = self.ai_service.generate_json(prompt)
        if not res or "crime_category" not in res:
            category = fallback_detect_crime(incident_text)
            return {
                "crime_category": category,
                "severity": self.SEVERITY_DEFAULTS.get(category, {"severity": "Low", "score": 10, "reason": ["Fallback"], "urgency": "None", "priority": "Low"}),
                "evidence": ["ID Proof", "Written complaint"],
                "document_requirements": ["Proof of Identity"],
                "investigation_support": "Preserve all records.",
                "timeline": [{"stage": "Complaint Filing", "timeline": "Immediate", "description": "Lodge complaint", "section": "Section 173 BNSS"}],
                "specialized_advice": {}
            }
        return res

    def agent_orchestrator(self, user_id: str, session_id: str, message: str, conversation_history: list, language: str) -> dict:
        # Auto-detect language
        detected_language = self.detect_language(message, default_lang=language)
        language = detected_language

        # Determine if the input is transliterated (written in Roman script instead of native script)
        native_ranges = {
            "Tamil": range(0x0b80, 0x0c00),
            "Hindi": range(0x0900, 0x0980),
            "Telugu": range(0x0c00, 0x0c80),
            "Kannada": range(0x0c80, 0x0d00),
            "Malayalam": range(0x0d00, 0x0d80)
        }
        
        language_for_llm = language
        if language in native_ranges:
            has_native = any(c in message for c in [chr(i) for i in native_ranges[language]])
            if not has_native:
                if language == "Tamil":
                    language_for_llm = "Tanglish (transliterated Tamil using Roman/English characters ONLY - do NOT use Tamil script)"
                elif language == "Hindi":
                    language_for_llm = "Hinglish (transliterated Hindi using Roman/English characters ONLY - do NOT use Devanagari script)"
                else:
                    language_for_llm = f"{language} (transliterated using Roman/English characters ONLY - do NOT use native script)"

        captured_data = {
            "crimeCategory": "GeneralInquiry",
            "ipcSections": [],
            "agentData": {},
            "evidence": {},
            "severity": {},
            "legal": {},
            "judgements": {},
            "timeline": {}
        }

        try:
            # Check if it's a general greeting using fallback heuristic to save tool calls
            if len(message.split()) < 4 and any(w in message.lower() for w in ["hi", "hello", "hey", "help", "good"]):
                raise Exception("Greeting fallback")

            # 1. Comprehensive Analysis (Single API Call)
            analysis_res = self.agent_comprehensive_analysis(message, language_for_llm)
            cat = analysis_res.get("crime_category", "GeneralInquiry")
            captured_data["crimeCategory"] = cat
            captured_data["severity"] = analysis_res.get("severity", {})
            captured_data["evidence"] = {
                "items": [{"name": item, "description": "", "importance": "High"} for item in analysis_res.get("evidence", [])],
                "document_requirements": analysis_res.get("document_requirements", []),
                "investigation_support": analysis_res.get("investigation_support", "")
            }
            captured_data["timeline"] = {"procedureSteps": [f"{t.get('stage')} ({t.get('timeline')}): {t.get('description')} [{t.get('section')}]" for t in analysis_res.get("timeline", [])]}
            captured_data["agentData"]["comprehensive_analysis"] = analysis_res
            self.log_agent_action(user_id, session_id, "ComprehensiveAnalysisAgent", message, analysis_res)

            # 2. Direct Legal & Judgement Retrieval (No API Calls)
            sections_codes = CRIME_TO_SECTIONS.get(cat, [])
            retrieved_info = []
            for code in sections_codes:
                sec = get_legal_section(code)
                if sec:
                    retrieved_info.append(sec)
                    captured_data["ipcSections"].append(sec.get("code", ""))

            rag_context = ""
            try:
                rag_context = self.rag_service.get_context_for_prompt(message, n_results=3)
            except Exception as e:
                logger.error(f"RAG Retrieval error: {e}")

            static_judgements = search_judgements(crime_type=cat)
            if not static_judgements:
                keywords = [w for w in message.lower().split() if len(w) > 4][:3]
                for kw in keywords:
                    static_judgements = search_judgements(keyword=kw)
                    if static_judgements: break
            if not static_judgements:
                related_types = {"Murder": ["PhysicalAssault", "Kidnapping"], "PhysicalAssault": ["Murder", "DomesticViolence"], "Robbery": ["Theft", "Blackmail"], "SexualAssault": ["Harassment", "DomesticViolence"], "Kidnapping": ["Murder", "Blackmail"]}
                for related in related_types.get(cat, []):
                    static_judgements = search_judgements(crime_type=related)
                    if static_judgements: break
            if not static_judgements:
                static_judgements = SAMPLE_JUDGEMENTS[:3]

            captured_data["legal"] = {"sections": retrieved_info}
            captured_data["judgements"] = {"judgements": static_judgements}

            # 3. Final Synthesis & FIR Drafting (Single API Call)
            context_summary = f"User Query: {message}\n"
            context_summary += f"Detected Language: {language_for_llm}\n"
            context_summary += f"Incident Classification: {cat} (Severity: {analysis_res.get('severity', {}).get('severity', 'Medium')})\n"
            sections_list = [f"- Section {s.get('code')}: {s.get('title')} ({s.get('punishment')})" for s in retrieved_info]
            context_summary += "\nApplicable Legal Sections:\n" + ("\n".join(sections_list) if sections_list else "None found.")
            evidence_list = [f"- {item}" for item in analysis_res.get("evidence", [])]
            context_summary += "\nRecommended Evidence:\n" + ("\n".join(evidence_list) if evidence_list else "None found.")
            steps_list = [step for step in captured_data["timeline"]["procedureSteps"]]
            context_summary += "\nProcedure Roadmap:\n" + ("\n".join(steps_list) if steps_list else "None found.")
            judgements_list = [f"- Case: {j.get('case_name')} ({j.get('year')}) Summary: {j.get('summary')}" for j in static_judgements]
            context_summary += "\nRelevant Court Precedents:\n" + ("\n".join(judgements_list) if judgements_list else "None found.")
            if rag_context:
                context_summary += "\nAdditional Legal Context:\n" + rag_context

            spec_advice_dict = analysis_res.get("specialized_advice", {})
            if spec_advice_dict:
                import json
                context_summary += "\nSpecialized Advice Details:\n" + json.dumps(spec_advice_dict)\n
            synthesis_prompt = (
                f"You are the Agentic AI Orchestrator for the AI Legal Assistant.\n"
                f"Your task is to synthesize the following collected analysis and context into a comprehensive, professional, friendly, and compassionate markdown report in language '{language_for_llm}'.\n\n"
                f"--- Legal Context & Analysis ---\n"
                f"{context_summary}\n\n"
                f"--- Requirements ---\n"
                f"1. You MUST respond in the language '{language_for_llm}'.\n"
                f"   - If '{language_for_llm}' is exactly 'Tamil', write the response in beautiful and grammatically correct Tamil script (தமிழ்).\n"
                f"   - If '{language_for_llm}' is exactly 'Hindi', write in Devanagari script.\n"
                f"   - If '{language_for_llm}' is exactly 'Telugu', write in Telugu script.\n"
                f"   - If '{language_for_llm}' is exactly 'Malayalam', write in Malayalam script.\n"
                f"   - If '{language_for_llm}' is exactly 'Kannada', write in Kannada script.\n"
                f"   - If '{language_for_llm}' is exactly 'English', write in English.\n"
                f"   - If the language is transliterated (like Tanglish, Hinglish, or any language containing 'transliterated'), you MUST write the response in that transliterated language using Roman/English characters ONLY.\n"
                f"2. Use formatting with clear headings like:\n"
                f"   ⚖️ Incident Classification & Severity\n"
                f"   🚨 Specialized Advice (if applicable)\n"
                f"   📚 Applicable Legal Sections (explain their legal meaning based on the retrieved static sections)\n"
                f"   🗂️ Recommended Evidence & Documents\n"
                f"   ⏳ Legal Action Roadmap\n"
                f"   🏛️ Relevant Court Precedents (explain their relevance to the user's case)\n"
                f"   📝 Formal FIR Draft (Write a legally structured First Information Report letter addressed to 'The Inspector of Police' at the very end, if the category is not GeneralInquiry)\n"
                f"3. Do not mention any code variables, internal JSON fields, or 'captured data'. The response must be written directly to the end user as their legal assistant."
            )

            response_text = self.ai_service.generate_content(synthesis_prompt)
            if not response_text or response_text.startswith("Error"):
                raise Exception("Synthesis generation failed")

        except Exception as e:
            logger.error(f"Error in sequential orchestrator: {e}")
            # Fallback to general inquiry response with pre-translated fallbacks
            fallback_dict = {
                "English": "I am an AI Legal Assistant. Please provide more details about your incident or legal issue so I can assist you better.",
                "Tamil": "நான் ஒரு ஏஐ சட்ட உதவியாளர் (AI Legal Assistant). உங்களுக்கு சிறந்த முறையில் உதவ, உங்கள் சம்பவம் அல்லது சட்டப் பிரச்சனை பற்றிய கூடுதல் விவரங்களை வழங்கவும்.",
                "Hindi": "मैं एक एआई कानूनी सहायक (AI Legal Assistant) हूँ। आपकी बेहतर सहायता करने के लिए कृपया अपनी घटना या कानूनी मुद्दे के बारे में अधिक विवरण प्रदान करें।",
                "Telugu": "నేను ఒక ఏఐ న్యాయ సహాయకుడిని (AI Legal Assistant). మీకు మరింత మెరుగ్గా సహాయపడటానికి దయచేసి మీ సంఘటన లేదా చట్టపరమైన సమస్య గురించి మరిన్ని వివరాలను అందించండి.",
                "Malayalam": "ഞാൻ ഒരു എഐ നിയമ സഹായിയാണ് (AI Legal Assistant). നിങ്ങളെ മികച്ച രീതിയിൽ സഹായിക്കുന്നതിന് ദയവായി നിങ്ങളുടെ സംഭവം അല്ലെങ്കിൽ നിയമപരമായ പ്രശ്നം എന്നിവയെക്കുറിച്ചുള്ള കൂടുതൽ വിവരങ്ങൾ നൽകുക.",
                "Kannada": "ನಾನು ಎಐ ಕಾನೂನು ಸಹಾಯಕ (AI Legal Assistant). ನಿಮಗೆ ಉತ್ತಮವಾಗಿ ಸಹಾಯ ಮಾಡಲು ದಯವಿಟ್ಟು ನಿಮ್ಮ ಘಟನೆ ಅಥವಾ ಕಾನೂನು ಸಮಸ್ಯೆಯ ಕುರಿತು ಹೆಚ್ಚಿನ ವಿವರಗಳನ್ನು ನೀಡಿ."
            }
            response_text = fallback_dict.get(language, fallback_dict["English"])
            if "tanglish" in language_for_llm.lower():
                response_text = "Naan oru AI Satta Udhaviyaalar (AI Legal Assistant). Ungalukku sirandha muraiyil udhava, ungal sambavam alladhu satta prachinai patriya koodudhal vivarangalai valangavum."
            elif "hinglish" in language_for_llm.lower():
                response_text = "Main ek AI Kanooni Sahayak (AI Legal Assistant) hoon. Aapki behtar sahayata karne ke liye kripya apni ghatna ya kanooni mudde ke baare mein aur details dein." 

        # Save to legal history
        history_id = uuid4().hex[:24]
        self.db.legal_history[history_id] = {
            "id": history_id,
            "userId": user_id,
            "sessionId": session_id,
            "crimeCategory": captured_data["crimeCategory"],
            "timestamp": datetime.now().isoformat(),
            "results": {
                "evidence": captured_data["evidence"],
                "severity": captured_data["severity"],
                "legal": captured_data["legal"],
                "judgements": captured_data["judgements"],
                "timeline": captured_data["timeline"]
            }
        }

        return {
            "assistantResponse": response_text,
            "crimeCategory": captured_data["crimeCategory"],
            "ipcSections": captured_data["ipcSections"],
            "agentData": captured_data["agentData"],
            "language": language
        }

