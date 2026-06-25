import re

def update_agentic_system():
    file_path = "c:/placement project/AI Legel Assistant/python_backend/agentic_system.py"
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Find the start of agent_orchestrator
    start_pattern = r"    # Agent 1: Legal Orchestrator Agent\n    def agent_orchestrator\(self, user_id: str, session_id: str, message: str, conversation_history: list, language: str\) -> dict:"
    match = re.search(start_pattern, content)
    if not match:
        print("Could not find agent_orchestrator")
        return
        
    start_idx = match.start()
    
    # We want to replace from start_idx to the end of the file or next class method? 
    # agent_orchestrator is the last method in the AgenticSystem class. We can just replace everything from start_idx to the end.
    # Wait, let's check if there's anything after agent_orchestrator.
    # We can view the end of the file.
    
    new_method = """    # Agent 1: Legal Orchestrator Agent
    def agent_orchestrator(self, user_id: str, session_id: str, message: str, conversation_history: list, language: str) -> dict:
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

        def analyze_crime(incident_description: str) -> dict:
            \"\"\"Identify the Indian crime category, severity, and intent from the user's incident description.\"\"\"
            res = self.agent_crime_classification(incident_description)
            captured_data["crimeCategory"] = res.get("crime_category", "GeneralInquiry")
            captured_data["agentData"]["crime_analysis"] = res
            
            # Auto-trigger severity analysis as part of crime analysis
            sev_res = self.agent_severity_analysis(incident_description, captured_data["crimeCategory"], language)
            captured_data["severity"] = sev_res
            captured_data["agentData"]["severity_analysis"] = sev_res
            
            self.log_agent_action(user_id, session_id, "CrimeClassificationAgent", incident_description, res)
            self.log_agent_action(user_id, session_id, "SeverityAnalysisAgent", incident_description, sev_res)
            return {"crime_analysis": res, "severity_analysis": sev_res}

        def recommend_evidence(incident_description: str) -> dict:
            \"\"\"Recommend evidence to collect based on the incident details.\"\"\"
            cat = captured_data["crimeCategory"]
            res = self.agent_evidence_recommendation(cat, incident_description, language)
            captured_data["evidence"] = res
            captured_data["agentData"]["evidence_recommendation"] = res
            self.log_agent_action(user_id, session_id, "EvidenceRecommendationAgent", incident_description, res)
            return res

        def generate_legal_timeline(incident_description: str) -> dict:
            \"\"\"Generate a legal action roadmap from incident reporting to trial.\"\"\"
            cat = captured_data["crimeCategory"]
            res = self.agent_legal_timeline(cat, incident_description, language)
            captured_data["timeline"] = res
            captured_data["agentData"]["legal_timeline"] = res
            self.log_agent_action(user_id, session_id, "LegalTimelineAgent", incident_description, res)
            return res

        def draft_fir(complainant_name: str, incident_description: str) -> dict:
            \"\"\"Generate a legally structured First Information Report (FIR) draft.\"\"\"
            cat = captured_data["crimeCategory"]
            # get legal sections if available
            sections = [s.get("code", "") for s in captured_data["legal"].get("sections", [])]
            res = self.agent_fir_drafting({"name": complainant_name}, {"incidentDetails": incident_description}, sections, language)
            captured_data["agentData"]["fir_draft"] = res
            self.log_agent_action(user_id, session_id, "FIRDraftingAgent", incident_description, res)
            return res

        def detect_scam(incident_description: str) -> dict:
            \"\"\"Detect fraudulent messages and links (OTP, UPI, Loan, Job scams).\"\"\"
            res = self.agent_scam_detection(incident_description, language)
            captured_data["agentData"]["scam_detection"] = res
            self.log_agent_action(user_id, session_id, "ScamDetectionAgent", incident_description, res)
            return res

        def provide_cyber_first_response(incident_description: str) -> dict:
            \"\"\"Provide immediate emergency actions for cyber attacks and financial fraud.\"\"\"
            res = self.agent_cyber_first_response(incident_description, language)
            captured_data["agentData"]["cyber_first_response"] = res
            self.log_agent_action(user_id, session_id, "CyberFirstResponseAgent", incident_description, res)
            return res

        def advise_consumer_rights(incident_description: str) -> dict:
            \"\"\"Handle consumer complaints like refund issues, fake products, and e-commerce fraud.\"\"\"
            res = self.agent_consumer_rights(incident_description, language)
            captured_data["agentData"]["consumer_rights"] = res
            self.log_agent_action(user_id, session_id, "ConsumerRightsAgent", incident_description, res)
            return res

        def assist_missing_person(incident_description: str) -> dict:
            \"\"\"Provide emergency guidance and FIR procedures for missing persons.\"\"\"
            res = self.agent_missing_person(incident_description, language)
            captured_data["agentData"]["missing_person"] = res
            self.log_agent_action(user_id, session_id, "MissingPersonAgent", incident_description, res)
            return res

        def assist_lost_document(incident_description: str) -> dict:
            \"\"\"Explain reporting and reissue procedures for lost documents (Aadhaar, PAN, Passport).\"\"\"
            res = self.agent_lost_document(incident_description, language)
            captured_data["agentData"]["lost_document"] = res
            self.log_agent_action(user_id, session_id, "LostDocumentAgent", incident_description, res)
            return res

        def retrieve_legal_knowledge(incident_description: str) -> dict:
            \"\"\"Retrieve legal information and sections from laws like BNS, BNSS, BSA, IT Act.\"\"\"
            cat = captured_data["crimeCategory"]
            res = self.agent_legal_knowledge(cat, incident_description, language)
            captured_data["legal"] = res
            captured_data["agentData"]["legal_knowledge"] = res
            if "sections" in res:
                captured_data["ipcSections"] = [s.get("code") for s in res["sections"] if s.get("code")]
            self.log_agent_action(user_id, session_id, "LegalKnowledgeRetrievalAgent", incident_description, res)
            return res

        def retrieve_judgements(incident_description: str) -> dict:
            \"\"\"Retrieve relevant Supreme Court or High Court judgements related to the incident.\"\"\"
            cat = captured_data["crimeCategory"]
            res = self.agent_judgement_retrieval(cat, incident_description, language)
            captured_data["judgements"] = res
            captured_data["agentData"]["judgement_retrieval"] = res
            self.log_agent_action(user_id, session_id, "JudgementRetrievalAgent", incident_description, res)
            return res

        tools = [
            analyze_crime,
            recommend_evidence,
            generate_legal_timeline,
            draft_fir,
            detect_scam,
            provide_cyber_first_response,
            advise_consumer_rights,
            assist_missing_person,
            assist_lost_document,
            retrieve_legal_knowledge,
            retrieve_judgements
        ]

        system_instruction = (
            f"You are the Agentic AI Orchestrator for the AI Legal Assistant. "
            f"Your job is to assist the user by autonomously selecting and executing specialized tools to solve their problem. "
            f"You MUST use tools when the user describes an incident, crime, fraud, or legal issue. "
            f"Always call `analyze_crime` first to classify the incident. "
            f"Then call other relevant tools based on the classification (e.g., if it is Cyber Fraud, call `detect_scam` and `provide_cyber_first_response`). "
            f"Call `retrieve_legal_knowledge` to get specific laws. "
            f"After gathering all necessary tool outputs, synthesize the results into a comprehensive, professional, and compassionate markdown report in language '{language}'. "
            f"Format the final response with clear headings like: "
            f"⚖️ Incident Classification & Severity, 🚨 Specialized Advice, 📚 Applicable Legal Sections, 🗂️ Recommended Evidence & Documents, ⏳ Legal Action Roadmap, 🏛️ Relevant Court Precedents."
        )

        try:
            # Check if it's a general greeting using fallback heuristic to save tool calls
            if len(message.split()) < 4 and any(w in message.lower() for w in ["hi", "hello", "hey", "help", "good"]):
                raise Exception("Greeting fallback")
                
            response_text = self.ai_service.generate_with_tools(
                prompt=message,
                tools=tools,
                system_instruction=system_instruction
            )
            
            if not response_text or response_text.startswith("Error"):
                raise Exception("Tool execution failed or returned None")
                
        except Exception as e:
            # Fallback to general inquiry response
            response_text = self.get_general_inquiry_fallback(message, language)

        # Save to legal history
        from uuid import uuid4
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
            "agentData": captured_data["agentData"]
        }
"""
    
    # We need to make sure we replace the correct portion. 
    # I'll truncate everything after start_idx
    new_content = content[:start_idx] + new_method
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)

if __name__ == "__main__":
    update_agentic_system()
