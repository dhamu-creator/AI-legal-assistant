import os
import json
import uuid
import io
import logging
from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException, Header, Body, Response, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel
from dotenv import load_dotenv
import bcrypt
import jwt
import asyncio
from pymongo import MongoClient

from security_audit import AuditLogger, RateLimiter, RefreshTokenManager
from agentic_system import AgenticSystem

# ── Centralized Logging ──────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("ai_legal_assistant")

# ReportLab imports for PDF generation
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(CURRENT_DIR, "..", ".env")
load_dotenv(dotenv_path=env_path, override=True)

app = FastAPI(title="AI Legal Assistant - Python Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Unicode Font Setup ───────────────────────────────────────────────────────
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(CURRENT_DIR, "assets", "fonts")
FONT_PATH = os.path.join(FONT_DIR, "NotoSans-Regular.ttf")

FONT_NAME = "Helvetica"
font_registered = False
if os.path.exists(FONT_PATH):
    try:
        pdfmetrics.registerFont(TTFont('NotoSans', FONT_PATH))
        FONT_NAME = 'NotoSans'
        font_registered = True
        logger.info(f"Unicode PDF font registered from: {FONT_PATH}")
    except Exception as e:
        logger.warning(f"Failed to register Unicode font {FONT_PATH}: {e}")
else:
    logger.warning("Target Unicode font missing. Falling back to default system metrics.")

# ── Groq AI Setup ───────────────────────────────────────────────────
test_mode = False
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    logger.warning("GROQ_API_KEY not found or valid - running in Test Mode.")
    test_mode = True
else:
    logger.info("Groq API Key found. Will use Groq as AI backend.")

# ── MongoDB & JSON File Database ──────────────────────────────────────────────
DB_FILE = os.path.join(os.path.dirname(__file__), "database.json")
MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME", "ai_legal_assistant")

class MongoDictWrapper:
    def __init__(self, db_interface, collection_name):
        self.db = db_interface
        self.col_name = collection_name

    def get(self, key, default=None):
        res = self.db.get_record(self.col_name, key)
        return res if res is not None else default

    def values(self):
        return self.db.get_all_records(self.col_name)

    def __getitem__(self, key):
        val = self.get(key)
        if val is None:
            raise KeyError(key)
        return val

    def __setitem__(self, key, value):
        self.db.save_record(self.col_name, value)

    def __delitem__(self, key):
        self.db.delete_record(self.col_name, key)

    def __contains__(self, key):
        return self.get(key) is not None

class DatabaseInterface:
    def __init__(self):
        self.use_mongo = False
        self.mongo_client = None
        self.mongo_db = None
        self.local_db = {"users": {}, "chat_sessions": {}, "firs": {}, "agent_logs": {}, "legal_history": {}}
        
        # Load local database.json
        if os.path.exists(DB_FILE):
            try:
                with open(DB_FILE, "r", encoding="utf-8") as f:
                    loaded_db = json.load(f)
                    # Support legacy databases with uppercase keys case-insensitively
                    for key, val in loaded_db.items():
                        norm_key = key
                        if key.lower() == "users": norm_key = "users"
                        elif key.lower() == "chats": norm_key = "chat_sessions"
                        elif key.lower() == "firreports": norm_key = "firs"
                        elif key.lower() == "agentlogs": norm_key = "agent_logs"
                        elif key.lower() == "legalhistory": norm_key = "legal_history"
                        
                        # also handle if they were already snake_case
                        if key == "chat_sessions": norm_key = "chat_sessions"
                        elif key == "firs": norm_key = "firs"
                        elif key == "agent_logs": norm_key = "agent_logs"
                        elif key == "legal_history": norm_key = "legal_history"

                        self.local_db[norm_key] = val
            except json.JSONDecodeError as e:
                logger.error(f"Failed to decode database.json, file might be corrupted. Loading empty database. Error: {e}")
            except Exception as e:
                logger.error(f"Unexpected error loading database.json: {e}")
                
        # Try connecting to MongoDB
        uri = os.getenv("MONGODB_URI")
        if uri:
            self.mongo_client = MongoClient(uri, serverSelectionTimeoutMS=5000)
            for attempt in range(1, 4):
                try:
                    self.mongo_client.server_info() # trigger connection check
                    self.mongo_db = self.mongo_client[MONGODB_DB_NAME]
                    self.use_mongo = True
                    logger.info(f"MongoDB connection verified on attempt {attempt}.")
                    self._migrate_data()
                    break
                except Exception as e:
                    logger.warning(f"MongoDB connection attempt {attempt} failed. Re-evaluating...")
                    import time
                    time.sleep(2)
            if not self.use_mongo:
                logger.critical("Cloud Cluster unreachable. Activating local JSON cold storage backup pipeline.")
        else:
            logger.info("No MONGODB_URI configured. Running with local JSON database.")
            
        self.users = MongoDictWrapper(self, "users")
        self.chat_sessions = MongoDictWrapper(self, "chat_sessions")
        self.firs = MongoDictWrapper(self, "firs")
        self.agent_logs = MongoDictWrapper(self, "agent_logs")
        self.legal_history = MongoDictWrapper(self, "legal_history")

    def _migrate_data(self):
        if not self.use_mongo:
            return
        collections_to_migrate = [
            ("users", "Users"),
            ("chat_sessions", "Chats"),
            ("firs", "FIRReports"),
            ("agent_logs", "AgentLogs"),
            ("legal_history", "LegalHistory")
        ]
        try:
            for old_col, new_col in collections_to_migrate:
                local_data = self.local_db.get(new_col) or self.local_db.get(old_col)
                if local_data and self.mongo_db[new_col].count_documents({}) == 0:
                    data_list = list(local_data.values())
                    if data_list:
                        self.mongo_db[new_col].insert_many(data_list)
                        logger.info(f"Migrated {len(data_list)} {old_col} to MongoDB collection {new_col}.")
        except Exception as e:
            logger.error(f"Data migration failed: {e}")

    def get_record(self, col_name: str, key: str) -> dict:
        if self.use_mongo:
            return self.mongo_db[col_name].find_one({"id": key} if col_name != "Users" else {"$or": [{"id": key}, {"_id": key}]})
        return self.local_db[col_name].get(key)

    def save_record(self, col_name: str, record: dict):
        rec_id = record.get("id") or record.get("_id")
        if self.use_mongo:
            self.mongo_db[col_name].replace_one({"id": rec_id}, record, upsert=True)
        else:
            self.local_db[col_name][rec_id] = record
            self._save_local()

    def get_all_records(self, col_name: str):
        if self.use_mongo:
            return list(self.mongo_db[col_name].find({}))
        return list(self.local_db[col_name].values())

    def delete_record(self, col_name: str, key: str):
        if self.use_mongo:
            self.mongo_db[col_name].delete_one({"id": key})
        else:
            if key in self.local_db[col_name]:
                del self.local_db[col_name][key]
                self._save_local()

    # Legacy wrappers for backward compatibility if any old code uses db.get_user directly
    def get_user(self, user_id): return self.get_record("Users", user_id)
    def save_user(self, user): self.save_record("Users", user)
    def get_all_users(self): return self.get_all_records("Users")
    def get_chat_session(self, sid): return self.get_record("Chats", sid)
    def save_chat_session(self, s): self.save_record("Chats", s)
    def delete_chat_session(self, sid): self.delete_record("Chats", sid)
    def get_fir(self, fid): return self.get_record("FIRReports", fid)
    def save_fir(self, f): self.save_record("FIRReports", f)
    def delete_fir(self, fid): self.delete_record("FIRReports", fid)

    def _save_local(self):
        import copy, threading, tempfile, os
        if not hasattr(self, '_save_lock'):
            self._save_lock = threading.Lock()
        with self._save_lock:
            snapshot = copy.deepcopy(self.local_db)
        
        dir_name = os.path.dirname(DB_FILE)
        try:
            with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=dir_name, delete=False) as tf:
                json.dump(snapshot, tf, indent=2, ensure_ascii=False)
                temp_name = tf.name
            os.replace(temp_name, DB_FILE)
        except Exception as e:
            logger.error(f"Atomic save failed: {e}")

    def __getitem__(self, key):
        if key in ["users", "Users"]: return self.users
        elif key in ["chat_sessions", "Chats"]: return self.chat_sessions
        elif key in ["firs", "FIRReports"]: return self.firs
        elif key in ["agent_logs", "AgentLogs"]: return self.agent_logs
        elif key in ["legal_history", "LegalHistory"]: return self.legal_history
        raise KeyError(key)

db = DatabaseInterface()
audit_logger = AuditLogger(db)
rate_limiter = RateLimiter()
refresh_token_manager = RefreshTokenManager(db)

def save_db(db_obj):
    if not db_obj.use_mongo:
        db_obj._save_local()

# ── Helpers ──────────────────────────────────────────────────────────────────
def new_id():
    return uuid.uuid4().hex[:24]

# ── Bcrypt Hashing & JWT Auth ────────────────────────────────────────────────
JWT_SECRET = os.getenv("JWT_SECRET", "super_secret_legal_key_123!")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

if ENVIRONMENT == "production" and JWT_SECRET == "super_secret_legal_key_123!":
    raise ValueError("CRITICAL: Default JWT_SECRET is active in production environment! Set JWT_SECRET.")

JWT_ALGORITHM = "HS256"

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    except Exception:
        return False

def create_jwt_token(user_id: str) -> str:
    payload = {
        "sub": user_id,
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(days=7)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def decode_jwt_token(token: str) -> str:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload.get("sub")
    except Exception:
        return None

agent_system = AgenticSystem(db, test_mode)

# ── AI Intelligence Upgrades (Groq) ──────────────────────────────────────────
def classify_crime_with_ai(text: str) -> str:
    if test_mode:
        return detect_crime(text)
    
    categories_str = ", ".join(MODERN_LEGAL_MAP.keys())
    prompt = (
        f"You are an expert Indian legal annotator trained on the Bharatiya Nyaya Sanhita (BNS) and "
        f"Bharatiya Nagarik Suraksha Sanhita (BNSS). Analyze this user input and classify it into "
        f"EXACTLY ONE of the following categories:\n"
        f"[{categories_str}]\n\n"
        f"IMPORTANT: If the user is asking a general procedural question (e.g., how to file a complaint, "
        f"what is an FIR, what are my rights, how does the legal process work), classify as 'GeneralInquiry'.\n\n"
        f"User input: \"{text}\"\n\n"
        f"Return ONLY the exact category name and nothing else."
    )
    try:
        result_text = agent_system.ai_service.generate_content(prompt)
        if not result_text or result_text.startswith("Error"):
            return detect_crime(text)
        category = result_text.replace("`", "").replace("\"", "").replace("'", "").strip()
        if category in MODERN_LEGAL_MAP:
            return category
        # If AI returns a partial match, try to resolve it
        for cat in MODERN_LEGAL_MAP.keys():
            if cat.lower() in category.lower():
                return cat
        return detect_crime(text)
    except Exception as e:
        audit_logger.log_action("system", "AI_API_FAILURE", "groq_model", "POST", "failed", {"error_message": str(e), "action": "Executed heuristic fallback local engine parser (detect_crime)"})
        logger.error(f"AI crime classification failed: {e}")
        return detect_crime(text)

def generate_evidence_checklist_with_ai(crime_category: str, language: str = "en") -> dict:
    if test_mode:
        return None
        
    lang_name = LANG_NAMES.get(language, "English")
    prompt = (
        f"For the Indian crime category '{crime_category}', provide a customized legal guide in {lang_name}. "
        f"Respond ONLY with a JSON object. Do not include any formatting like ```json or markdown. The JSON schema must be exactly:\n"
        f"{{\n"
        f"  \"items\": [\n"
        f"    {{\"name\": \"Evidence Item\", \"description\": \"How to collect it\", \"importance\": \"critical\"}}\n"
        f"  ],\n"
        f"  \"procedureSteps\": [\n"
        f"    \"Step 1...\", \"Step 2...\"\n"
        f"  ],\n"
        f"  \"emergencyContacts\": [\n"
        f"    {{\"name\": \"Contact Name\", \"number\": \"Phone/Helpline\"}}\n"
        f"  ]\n"
        f"}}\n"
    )
    try:
        result_json = agent_system.ai_service.generate_json(prompt)
        return result_json
    except Exception as e:
        logger.error(f"Evidence recommendation failed: {e}")
        return None

def generate_legal_timeline_with_ai(crime_category: str, language: str = "en") -> list:
    if test_mode:
        return None
    
    lang_name = LANG_NAMES.get(language, "English")
    prompt = (
        f"As an expert Indian legal advisor, create a step-by-step procedural timeline from incident reporting "
        f"to investigation, charge sheet, and final trial in court for the crime category '{crime_category}' "
        f"under the Bharatiya Nagarik Suraksha Sanhita (BNSS) or current Indian laws.\n\n"
        f"Respond in {lang_name} ONLY with a JSON list. Do not include any formatting like ```json or markdown. The schema must be exactly:\n"
        f"[\n"
        f"  {{\"stage\": \"Stage Name\", \"timeline\": \"Expected Timeline (e.g. Day 1, Within 60 Days)\", \"description\": \"Procedural detail\", \"section\": \"Relevant Law Section (BNSS/BNS/IPC)\"}}\n"
        f"]\n"
    )
    try:
        result_json = agent_system.ai_service.generate_json(prompt)
        return result_json
    except Exception as e:
        logger.error(f"Timeline generation failed: {e}")
        return None

LANG_NAMES = {
    "en": "English", "ta": "Tamil", "hi": "Hindi",
    "te": "Telugu", "ml": "Malayalam", "ka": "Kannada"
}

# ── Modern Legal Mapping Engine (BNS/BNSS) ──────────────────────────────────
# All references are to the Bharatiya Nyaya Sanhita (BNS), Bharatiya Nagarik
# Suraksha Sanhita (BNSS), IT Act 2000, PWDVA 2005, POCSO 2012, NDPS 1985,
# SC/ST Act 1989, and Motor Vehicles Act 1988.
MODERN_LEGAL_MAP = {
    "Theft":             ["BNS 303", "BNS 304", "BNS 305"],
    "Robbery":           ["BNS 309", "BNS 310", "BNS 311"],
    "CyberFraud":        ["BNS 318", "BNS 319", "IT Act 66", "IT Act 66C", "IT Act 66D"],
    "Harassment":        ["BNS 74", "BNS 75", "BNS 79"],
    "SexualAssault":     ["BNS 63", "BNS 64", "BNS 65", "BNS 70"],
    "DomesticViolence":  ["BNS 85", "BNS 86", "PWDVA 2005"],
    "Blackmail":         ["BNS 308", "BNS 351"],
    "OnlineScams":       ["BNS 318", "IT Act 66D", "IT Act 66"],
    "IdentityTheft":     ["BNS 316", "BNS 319", "IT Act 66C"],
    "FinancialFraud":    ["BNS 315", "BNS 316", "BNS 336"],
    "PhysicalAssault":   ["BNS 115", "BNS 117", "BNS 127"],
    "Murder":            ["BNS 101", "BNS 103", "BNS 104", "BNS 109"],
    "Kidnapping":        ["BNS 137", "BNS 138", "BNS 139", "BNS 140"],
    "DowryDeath":        ["BNS 105", "BNS 85"],
    "DrugOffenses":      ["NDPS 20", "NDPS 21", "NDPS 22"],
    "ChildAbuse":        ["POCSO 4", "POCSO 6", "BNS 66", "BNS 67"],
    "AcidAttack":        ["BNS 127", "BNS 117"],
    "Defamation":        ["BNS 356", "BNS 352"],
    "Forgery":           ["BNS 319", "BNS 320"],
    "DrunkenDriving":    ["MV Act 184", "MV Act 185"],
    "RoadAccidentDeath": ["BNS 106", "MV Act 184"],
    "CasteAtrocity":     ["SC/ST Act 3"],
    "Stalking":          ["BNS 79"],
    "Voyeurism":         ["BNS 78", "IT Act 66E"],
    "OrganisedCrime":    ["BNS 111", "BNS 112"],
    "Terrorism":         ["BNS 113"],
    "CriminalIntimidation": ["BNS 351", "BNS 352"],
    "WrongfulConfinement": ["BNS 122"],
    "Poisoning":         ["BNS 121"],
    "Scam":              ["IT Act 66D", "BNS 318", "BNS 315"],
    "ConsumerRights":    ["BNS 315", "IPC 420"],
    "MissingPerson":     ["BNSS 173"],
    "LostDocument":      ["BNSS 173"],
    "GeneralInquiry":    ["BNSS 173"],
}

# Backward-compatible alias so any stale references still resolve
CRIME_IPCMAP = MODERN_LEGAL_MAP

def detect_crime(text: str):
    """Heuristic fallback classifier. Returns GeneralInquiry for procedural/generic questions."""
    text = text.lower()
    if any(w in text for w in ["file", "complaint", "fir", "report", "police station", "procedure", "how to", "what is", "rights", "process", "bail", "anticipatory"]): return "GeneralInquiry"
    if any(w in text for w in ["terror", "bomb", "explosive"]): return "Terrorism"
    if any(w in text for w in ["kill", "murder", "dead", "homicide", "assassinate", "shoot", "stab", "buried", "body"]): return "Murder"
    if any(w in text for w in ["rape", "sexual assault", "molest", "gang rape"]): return "SexualAssault"
    if any(w in text for w in ["kidnap", "abduct", "ransom", "hostage"]): return "Kidnapping"
    if any(w in text for w in ["acid attack", "acid throw", "disfigure"]): return "AcidAttack"
    if any(w in text for w in ["child abuse", "child porn", "pocso", "minor abuse"]): return "ChildAbuse"
    if any(w in text for w in ["dowry death", "bride burn"]): return "DowryDeath"
    if any(w in text for w in ["drug", "narcotic", "ganja", "cocaine", "heroin", "ndps", "cannabis"]): return "DrugOffenses"
    if any(w in text for w in ["scam", "telegram", "whatsapp", "job scam", "loan scam", "phish", "upi", "electricity bill"]): return "Scam"
    if any(w in text for w in ["hack", "online", "otp", "bank transfer", "fraud", "cyber"]): return "CyberFraud"
    if any(w in text for w in ["robbery", "dacoity", "loot", "armed robbery"]): return "Robbery"
    if any(w in text for w in ["stole", "stolen", "theft", "pickpocket", "snatch"]): return "Theft"
    if any(w in text for w in ["beat", "assault", "attack", "hit", "punch", "kick", "slap"]): return "PhysicalAssault"
    if any(w in text for w in ["domestic", "wife beating", "husband beat", "spouse", "dowry", "cruelty by husband"]): return "DomesticViolence"
    if any(w in text for w in ["stalk", "follow", "eve teas"]): return "Stalking"
    if any(w in text for w in ["harass", "bully", "workplace harass"]): return "Harassment"
    if any(w in text for w in ["blackmail", "extort", "threaten", "threat"]): return "Blackmail"
    if any(w in text for w in ["identity", "impersonate", "fake id", "fake profile"]): return "IdentityTheft"
    if any(w in text for w in ["forgery", "forge", "fake document", "counterfeit"]): return "Forgery"
    if any(w in text for w in ["drunk driv", "drunken driv", "dui"]): return "DrunkenDriving"
    if any(w in text for w in ["road accident", "hit and run", "rash driving"]): return "RoadAccidentDeath"
    if any(w in text for w in ["caste", "dalit", "sc/st", "atrocity"]): return "CasteAtrocity"
    if any(w in text for w in ["defam", "slander", "libel"]): return "Defamation"
    if any(w in text for w in ["money", "finance", "cheat", "invest", "ponzi"]): return "FinancialFraud"
    if any(w in text for w in ["voyeur", "peeping", "hidden camera"]): return "Voyeurism"
    if any(w in text for w in ["confine", "lock", "imprison"]): return "WrongfulConfinement"
    if any(w in text for w in ["poison", "sedat"]): return "Poisoning"
    if any(w in text for w in ["consumer", "fake product", "warranty", "refund", "defective", "ecommerce"]): return "ConsumerRights"
    if any(w in text for w in ["missing", "disappeared", "runaway", "ran away", "ranaway", "missing person"]): return "MissingPerson"
    if any(w in text for w in ["lost document", "lost aadhaar", "lost pan", "lost passport", "lost license", "lost mark sheet", "lost certificate", "lost my aadhaar", "lost my pan", "lost my wallet", "lost my bag"]): return "LostDocument"
    return "GeneralInquiry"

# ── Pydantic Models ──────────────────────────────────────────────────────────
class RegisterReq(BaseModel):
    name: str
    email: str
    password: str
    language: str = "en"
    role: str = "user"

class LoginReq(BaseModel):
    email: str
    password: str
    mfa_token: str = None

class SessionReq(BaseModel):
    userId: str
    language: str = "en"

class MessageReq(BaseModel):
    sessionId: str
    message: str
    language: str = "en"

# ── Health ───────────────────────────────────────────────────────────────────
@app.get("/api/ready")
@app.get("/api/health")
def health():
    return {"status": "ok", "message": "AI Legal Assistant Python API is running", "ready": True}

# ── Legal Info ───────────────────────────────────────────────────────────────
@app.get("/api/legal/languages")
def languages():
    return {"success": True, "data": {
        "en": {"name": "English",   "nativeName": "English"},
        "ta": {"name": "Tamil",     "nativeName": "தமிழ்"},
        "hi": {"name": "Hindi",     "nativeName": "हिन्दी"},
        "te": {"name": "Telugu",    "nativeName": "తెలుగు"},
        "ml": {"name": "Malayalam", "nativeName": "മലയാളം"},
        "ka": {"name": "Kannada",   "nativeName": "ಕನ್ನಡ"},
    }}

@app.get("/api/legal/crime-categories")
def crime_categories():
    return {"success": True, "data": list(CRIME_IPCMAP.keys())}

@app.get("/api/legal/disclaimer")
def disclaimer():
    return {"success": True, "data": {"text": "This AI assistant provides legal information only. It is not a substitute for a licensed advocate. Always consult a qualified legal professional before taking action."}}

@app.get("/api/legal/emergency-contacts")
def emergency_contacts():
    return {"success": True, "data": [
        {"name": "Police",            "number": "100"},
        {"name": "Women Helpline",    "number": "1091"},
        {"name": "Cyber Crime",       "number": "1930"},
        {"name": "Emergency",         "number": "112"},
        {"name": "Child Helpline",    "number": "1098"},
        {"name": "Senior Citizen",    "number": "14567"},
    ]}

# ── Auth ─────────────────────────────────────────────────────────────────────
def require_admin(user_id: str):
    user = db["users"].get(user_id)
    if not user or user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin privileges required")

@app.post("/api/auth/register")
def register(req: RegisterReq, request: Request):
    client_ip = request.client.host if request.client else "unknown"
    if not rate_limiter.is_allowed(client_ip, endpoint_type="auth"):
        raise HTTPException(status_code=429, detail="Too many registration attempts.")

    # Check duplicate email
    for u in db["users"].values():
        if u["email"] == req.email:
            raise HTTPException(status_code=400, detail="Email already registered")
    uid = new_id()
    hashed = hash_password(req.password)
    from utils.crypto import MultiFactorAuth
    mfa_secret = MultiFactorAuth.generate_new_secret()
    user = {"_id": uid, "id": uid, "name": req.name, "email": req.email,
            "password": hashed, "language": req.language, "role": req.role,
            "mfaEnabled": False, "mfaSecret": mfa_secret,
            "savedReports": [], "chatSessions": [],
            "preferences": {"darkMode": False, "notifications": True},
            "createdAt": datetime.now().isoformat()}
    db["users"][uid] = user
    save_db(db)
    token = create_jwt_token(uid)
    return {"success": True, "data": {"user": user, "token": token}}

@app.post("/api/auth/login")
def login(req: LoginReq, request: Request):
    client_ip = request.client.host if request.client else "unknown"
    if not rate_limiter.is_allowed(client_ip, endpoint_type="auth"):
        raise HTTPException(status_code=429, detail="Too many login attempts. Please try again later.")

    for u in db["users"].values():
        if u["email"] == req.email:
            if verify_password(req.password, u["password"]):
                # MFA Check
                if u.get("mfaEnabled"):
                    if not req.mfa_token:
                        return {"success": False, "mfa_required": True, "message": "MFA token required"}
                    from utils.crypto import MultiFactorAuth
                    if not MultiFactorAuth.verify_token(u.get("mfaSecret"), req.mfa_token):
                        raise HTTPException(status_code=401, detail="Invalid MFA token")
                        
                token = create_jwt_token(u['id'])
                return {"success": True, "data": {"user": u, "token": token}}
    raise HTTPException(status_code=401, detail="Invalid email or password")

@app.get("/api/auth/me")
def get_me(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="No token")
    token = authorization.replace("Bearer ", "")
    user_id = decode_jwt_token(token)
    if not user_id:
        if token.startswith("token-"):
            user_id = token.replace("token-", "")
        else:
            raise HTTPException(status_code=401, detail="Invalid token")
    user = db["users"].get(user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return {"success": True, "data": user}

# ── Chat ─────────────────────────────────────────────────────────────────────
@app.post("/api/chat/session")
def create_session(req: SessionReq):
    sid = new_id()
    session = {
        "_id": sid, "id": sid, "userId": req.userId,
        "title": f"Chat - {datetime.now().strftime('%d/%m/%Y')}",
        "language": req.language, "messages": [],
        "ipcSections": [], "bnsSections": [],
        "confidenceScore": 0, "isResolved": False,
        "createdAt": datetime.now().isoformat(), "updatedAt": datetime.now().isoformat()
    }
    db["chat_sessions"][sid] = session
    save_db(db)
    return {"success": True, "data": session}

@app.get("/api/chat/sessions/{user_id}")
def get_sessions(user_id: str):
    sessions = [s for s in db["chat_sessions"].values() if s.get("userId") == user_id]
    return {"success": True, "data": sorted(sessions, key=lambda x: x["createdAt"], reverse=True)}

@app.get("/api/chat/history/{session_id}")
def get_history(session_id: str):
    s = db["chat_sessions"].get(session_id)
    if not s:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"success": True, "data": s}

@app.delete("/api/chat/session/{session_id}")
def delete_session(session_id: str):
    if session_id in db["chat_sessions"]:
        del db["chat_sessions"][session_id]
        save_db(db)
    return {"success": True}

@app.post("/api/chat/message")
def send_message(req: MessageReq):
    session = db["chat_sessions"].get(req.sessionId)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    user_msg = {"role": "user", "content": req.message,
                "language": req.language, "createdAt": datetime.now().isoformat()}
    session["messages"].append(user_msg)

    # Build conversation history from session for contextual awareness
    history_lines = []
    for msg in session.get("messages", [])[:-1]:  # Exclude the current message
        role_label = "User" if msg["role"] == "user" else "Assistant"
        content = msg["content"][:500] + "..." if len(msg["content"]) > 500 else msg["content"]
        history_lines.append(f"{role_label}: {content}")

    # Invoke Legal Orchestrator Agent
    lang_name = LANG_NAMES.get(req.language, "English")
    agent_res = agent_system.agent_orchestrator(
        user_id=session.get("userId", "anonymous"),
        session_id=req.sessionId,
        message=req.message,
        conversation_history=history_lines,
        language=lang_name
    )

    detected_lang_name = agent_res.get("language", lang_name)
    REV_LANG_NAMES = {v: k for k, v in LANG_NAMES.items()}
    detected_lang_code = REV_LANG_NAMES.get(detected_lang_name, req.language)

    ai_msg = {
        "role": "assistant", 
        "content": agent_res["assistantResponse"],
        "language": detected_lang_code,
        "detectedCrimeCategory": agent_res["crimeCategory"],
        "relevantIPCSection": agent_res["ipcSections"][0] if agent_res["ipcSections"] else "",
        "sourceDocuments": agent_res["ipcSections"],
        "agentData": agent_res.get("agentData", {}),
        "createdAt": datetime.now().isoformat()
    }
    session["messages"].append(ai_msg)
    session["crimeCategory"] = agent_res["crimeCategory"]
    session["ipcSections"] = agent_res["ipcSections"]
    session["updatedAt"] = datetime.now().isoformat()
    db["chat_sessions"][req.sessionId] = session
    save_db(db)

    return {"success": True, "data": {
        "sessionId": req.sessionId,
        "userMessage": req.message,
        "assistantResponse": agent_res["assistantResponse"],
        "crimeCategory": agent_res["crimeCategory"],
        "ipcSections": agent_res["ipcSections"],
        "bnsSections": agent_res["ipcSections"],
        "language": detected_lang_code
    }}

# ── FIR ──────────────────────────────────────────────────────────────────────
@app.post("/api/fir/generate/{user_id}")
def generate_fir_endpoint(user_id: str, payload: dict = Body(...)):
    incident = payload.get("incidentData", {})
    language = payload.get("language", "en")
    complainant = incident.get("complainantDetails", {})
    crime_cat = incident.get("crimeCategory", "Theft")
    ipc_sections = MODERN_LEGAL_MAP.get(crime_cat, ["BNS 303"])

    lang_name = LANG_NAMES.get(language, "English")
    agent_res = agent_system.agent_fir_drafting(complainant, incident, ipc_sections, lang_name)
    draft = agent_res.get("draft", f"FIR Draft (BNSS 173): Complainant: {complainant.get('name')}. Sections: {', '.join(ipc_sections)}")

    fir_id = new_id()
    fir = {
        "_id": fir_id, "id": fir_id, "userId": user_id,
        "title": f"FIR - {datetime.now().strftime('%d/%m/%Y')}",
        "firDraft": draft, "status": "draft", "language": language,
        "crimeCategory": crime_cat, "ipcSections": ipc_sections, "bnsSections": [],
        "complainantDetails": complainant,
        "incidentDetails": incident.get("incidentDetails", ""),
        "incidentDate": incident.get("incidentDate", ""),
        "incidentLocation": incident.get("incidentLocation", ""),
        "suspectDetails": incident.get("suspectDetails", {}),
        "witnessDetails": [], "evidence": incident.get("evidence", []),
        "createdAt": datetime.now().isoformat(), "updatedAt": datetime.now().isoformat()
    }
    db["firs"][fir_id] = fir
    save_db(db)
    audit_logger.log_action(user_id, "GENERATE_FIR", "fir", "POST", "success",
                           {"crime_category": crime_cat})
    return {"success": True, "data": fir}

@app.post("/api/fir/create/{user_id}")
def create_fir(user_id: str, payload: dict = Body(...)):
    required = ["title", "incidentDetails", "incidentDate", "incidentLocation", "crimeCategory", "complainantDetails"]
    for field in required:
        if not payload.get(field):
            raise HTTPException(status_code=400, detail=f"Missing required FIR fields")
    fir_id = new_id()
    fir = {"_id": fir_id, "id": fir_id, "userId": user_id, "status": "draft",
           "ipcSections": CRIME_IPCMAP.get(payload.get("crimeCategory","Theft"),[]),
           "bnsSections": [], "witnessDetails": [],
           "createdAt": datetime.now().isoformat(), "updatedAt": datetime.now().isoformat(),
           **payload}
    db["firs"][fir_id] = fir
    save_db(db)
    return {"success": True, "data": fir}

@app.get("/api/fir/user/{user_id}")
def get_user_firs(user_id: str):
    firs = [f for f in db["firs"].values() if f.get("userId") == user_id]
    return {"success": True, "data": sorted(firs, key=lambda x: x["createdAt"], reverse=True)}

@app.get("/api/fir/{fir_id}")
def get_fir(fir_id: str):
    fir = db["firs"].get(fir_id)
    if not fir:
        raise HTTPException(status_code=404, detail="FIR not found")
    return {"success": True, "data": fir}

@app.put("/api/fir/{fir_id}")
def update_fir(fir_id: str, payload: dict = Body(...)):
    fir = db["firs"].get(fir_id)
    if not fir:
        raise HTTPException(status_code=404, detail="FIR not found")
    fir.update(payload)
    fir["updatedAt"] = datetime.now().isoformat()
    db["firs"][fir_id] = fir
    save_db(db)
    return {"success": True, "data": {"fir": fir}}

@app.delete("/api/fir/{fir_id}")
def delete_fir(fir_id: str):
    if fir_id in db["firs"]:
        del db["firs"][fir_id]
        save_db(db)
    return {"success": True}

@app.post("/api/fir/finalize/{fir_id}")
def finalize_fir(fir_id: str):
    fir = db["firs"].get(fir_id)
    if not fir:
        raise HTTPException(status_code=404, detail="FIR not found")
    fir["status"] = "submitted"
    fir["updatedAt"] = datetime.now().isoformat()
    db["firs"][fir_id] = fir
    save_db(db)
    return {"success": True, "data": fir}

@app.post("/api/fir/evidence/checklist")
def evidence_checklist(payload: dict = Body(...)):
    crime = payload.get("crimeCategory", "Theft")
    language = payload.get("language", "en")
    
    agent_res = agent_system.agent_evidence_recommendation(crime, language)
    if agent_res and "evidence" in agent_res and len(agent_res["evidence"]) > 0:
        # Map evidence to the UI's expected format
        items = [{"name": i, "description": f"Collect: {i}", "importance": "critical" if idx==0 else "important"} for idx, i in enumerate(agent_res["evidence"])]
        
        # Use Timeline agent for procedure steps
        timeline_res = agent_system.agent_legal_timeline(crime, language)
        steps = []
        if timeline_res and "timeline" in timeline_res:
            steps = [t["stage"] + ": " + t["description"] for t in timeline_res["timeline"]]
        if not steps:
            steps = [
                "Go to nearest police station immediately",
                "Request FIR registration under Section 173 BNSS",
                "Preserve all evidence carefully"
            ]
            
        return {"success": True, "data": {
            "items": items,
            "procedureSteps": steps,
            "emergencyContacts": [
                {"name": "Police Control Room", "number": "100"},
                {"name": "National Emergency", "number": "112"},
                {"name": "Women Helpline", "number": "1091"},
                {"name": "Cyber Crime", "number": "1930"}
            ]
        }}
        
    # Fallback to local static map
    checklists = {
        "Theft":           ["ID Proof", "List of stolen items with values", "CCTV footage if available", "Witness statements"],
        "CyberFraud":      ["Screenshots of fraud messages", "Bank transaction records", "Email/SMS evidence", "Complaint to bank"],
        "PhysicalAssault": ["Medical certificate (Medico-Legal Case)", "Photos of injuries", "Witness details", "CCTV footage"],
        "DomesticViolence":["Medical reports", "Photos of injuries", "Call recordings if any", "Witness statements"],
        "Harassment":      ["Screenshots/messages", "Witness statements", "CCTV footage", "Complaint history"],
        "Robbery":         ["Medical certificate if injured", "Description of stolen items", "Witness statements", "CCTV footage"],
    }
    items_list = checklists.get(crime, ["ID Proof", "Written complaint", "Witness details"])
    return {"success": True, "data": {
        "items": [{"name": i, "description": f"Collect: {i}", "importance": "critical" if idx==0 else "important"} for idx,i in enumerate(items_list)],
        "procedureSteps": [
            "Go to nearest police station immediately",
            "Request FIR registration under Section 154 CrPC / 173 BNSS",
            "Preserve all evidence carefully",
            "Keep copies of all documents submitted",
            "Follow up with police regularly"
        ],
        "emergencyContacts": [
            {"name": "Police", "number": "100"},
            {"name": "Women Helpline", "number": "1091"},
            {"name": "Cyber Crime", "number": "1930"},
            {"name": "Emergency", "number": "112"}
        ]
    }}

@app.get("/api/legal/timeline/{crime_category}")
def legal_timeline(crime_category: str, language: str = "en"):
    timeline = agent_system.agent_legal_timeline(crime_category, language)
    if timeline and "timeline" in timeline:
        return {"success": True, "data": timeline["timeline"]}
        
    # Fallback default timeline
    return {"success": True, "data": [
        {"stage": "Complaint Filing", "timeline": "Immediate (Day 1)", "description": "Lodge complaint at local police station or via e-FIR.", "section": "Section 173 BNSS"},
        {"stage": "FIR Registration", "timeline": "Within 3 days", "description": "Police register official FIR if a cognizable offense is prima facie found.", "section": "Section 173(3) BNSS"},
        {"stage": "Investigation", "timeline": "Within 60-90 days", "description": "Police gather evidence, record statements, and identify suspects.", "section": "Section 175-192 BNSS"},
        {"stage": "Charge Sheet", "timeline": "Upon completion of investigation", "description": "Final police report filed in court.", "section": "Section 193 BNSS"},
        {"stage": "Trial & Judgement", "timeline": "Varies", "description": "Court hearings, arguments, and final verdict.", "section": "BNSS Court Procedures"}
    ]}

# ── PDF Generation ───────────────────────────────────────────────────────────
LABELS_MAP = {
    "en": {
        "titleMain": "First Information Report (FIR)",
        "meta": "AI Legal Assistant — Official Draft",
        "generated": "Generated",
        "firId": "FIR ID",
        "title": "Title",
        "status": "Status",
        "submittedAt": "Submitted At",
        "complainantDetails": "Complainant Details",
        "name": "Name",
        "phone": "Phone",
        "email": "Email",
        "address": "Address",
        "incidentDetails": "Incident Details",
        "date": "Date",
        "location": "Location",
        "crimeCategory": "Crime Category",
        "details": "Details",
        "witnesses": "Witnesses",
        "evidence": "Evidence",
        "aiDraft": "AI-generated FIR Draft",
        "footer": "AI Legal Assistant — For informational purposes only. Contact: support@example.org",
    },
    "hi": {
        "titleMain": "प्राथमिक सूचना रिपोर्ट (FIR)",
        "meta": "AI लीगल असिस्टेंट — आधिकारिक मसौदा",
        "generated": "जनरेट किया गया",
        "firId": "FIR आईडी",
        "title": "शीर्षक",
        "status": "स्थिति",
        "submittedAt": "प्रस्तुत किया गया",
        "complainantDetails": "शिकायतकर्ता का विवरण",
        "name": "नाम",
        "phone": "फ़ोन",
        "email": "ईमेल",
        "address": "पता",
        "incidentDetails": "घटना का विवरण",
        "date": "तारीख",
        "location": "स्थान",
        "crimeCategory": "अपराध श्रेणी",
        "details": "विवरण",
        "witnesses": "गवाह",
        "evidence": "साक्ष्य",
        "aiDraft": "एआई-जनित FIR मसौदा",
        "footer": "सूचना के लिए: AI लीगल असिस्टेंट। हमेशा वकील से परामर्श करें।",
    },
    "ta": {
        "titleMain": "முதல் தகவல் அறிக்கை (FIR)",
        "meta": "AI லீகல் அசிஸ்டண்ட் — அதிகாரப்பூர்வ வரைவு",
        "generated": "உருவாக்கப்பட்டது",
        "firId": "FIR ஐடி",
        "title": "தலைப்பு",
        "status": "நிலை",
        "submittedAt": "சமர்ப்பிக்கப்பட்ட தேதி",
        "complainantDetails": "புகார் தருமவர் விவரங்கள்",
        "name": "பெயர்",
        "phone": "தெலைபேசி",
        "email": "மின்னஞ்சல்",
        "address": "முகவரி",
        "incidentDetails": "நிகழ்வு விவரம்",
        "date": "தேதி",
        "location": "இடம்",
        "crimeCategory": "குற்ற வகை",
        "details": "விவரங்கள்",
        "witnesses": "சாட்சிகள்",
        "evidence": "சான்றுகள்",
        "aiDraft": "ஏ.ஐ. உருவாக்கிய FIR வரைவு",
        "footer": "அறிவிப்பு: AI லீகல் அசிஸ்டண்ட் — தகவல उद्देश्यத்திற்காக. ஆலோசனைக்கு வழக்கு வழக்கறிஞரை அணுகவும்.",
    },
    "te": {
        "titleMain": "మొదటి సమాచారం నివేదనం (FIR)",
        "meta": "AI లీగల్ అసిస్టెంట్ — అధికారిక ముసాయిదా",
        "generated": "సృష్టించబడినది",
        "firId": "FIR ఐడీ",
        "title": "శీర్షిక",
        "status": "స్థితి",
        "submittedAt": "సమర్పించిన సమయం",
        "complainantDetails": "ఫిర్యాదుదారు వివరాలు",
        "name": "పేరు",
        "phone": "ఫోన్",
        "email": "ఈమెయిల్",
        "address": "చిరునామా",
        "incidentDetails": "సంఘటన వివరాలు",
        "date": "తేదీ",
        "location": "స్థానం",
        "crimeCategory": "నేర వర్గం",
        "details": "వివరాలు",
        "witnesses": "సాక్షులు",
        "evidence": "సాక్ష్యాలు",
        "aiDraft": "ఏఐ రూపొందించిన FIR ముసాయిదా",
        "footer": "సూచన: AI లీగల్ అసిస్టెంట్ — సమాచారపూర్వకంగా మాత్రమే. చట్టసంబంధి సలహాల కోసం న్యాయవాది ని సంప్రదించండి.",
    },
    "ml": {
        "titleMain": "ആദ്യ റിപ്പോർട്ട് (FIR)",
        "meta": "AI ലീഗൽ അസിസ്റ്റന്റ് — ഔദ്യോഗിക ഡ്രാഫ്റ്റ്",
        "generated": "സൃഷ്ടിച്ചത്",
        "firId": "FIR ഐഡി",
        "title": "തലക്കെട്ട്",
        "status": "നില",
        "submittedAt": "സമർപ്പിച്ചത്",
        "complainantDetails": "പരാതിക്കാരൻ വിവരങ്ങൾ",
        "name": "പേര്",
        "phone": "ഫോൺ",
        "email": "ഇമെയിൽ",
        "address": "വിലാസം",
        "incidentDetails": "സംഭവത്തിന്റെ വിശദാംശങ്ങൾ",
        "date": "തിയതി",
        "location": "സ്ഥലം",
        "crimeCategory": "കുറ്റകൃത്യ വിഭാഗം",
        "details": "വിശദാംശങ്ങൾ",
        "witnesses": "സാക്ഷികൾ",
        "evidence": "സാക്ഷ്യങ്ങൾ",
        "aiDraft": "AI തയ്യാറാക്കിയ FIR ഡ്രാഫ്റ്റ്",
        "footer": "അറിയിപ്പ്: AI ലീഗൽ അസിസ്റ്റന്റ് — വെറും വിവരാനുകൂല്യത്തിന്. നിയമസഹായത്തിന് ഒരു അഭിഭാഷകനെ സമീപിക്കുക.",
    },
    "ka": {
        "titleMain": "ಪ್ರಾಥಮಿಕ ಮಾಹಿತಿ ವರದಿ (FIR)",
        "meta": "AI ಲೆಗ್ಗಲ್ ಅಸಿಸ್ಟೆಂಟ್ — ಅಧಿಕೃತ ಕರಡು",
        "generated": "ರಚಿಸಲಾಗಿದೆ",
        "firId": "FIR ಐಡಿ",
        "title": "ಶೀರ್ಷಿಕೆ",
        "status": "ಸ್ಥಿತಿ",
        "submittedAt": "ಸಲ್ಲಿಸಲಾಗಿದೆ",
        "complainantDetails": "ಫಿರ್ಯಾದಿದಾರರ ವಿವರಗಳು",
        "name": "ಹೆಸರು",
        "phone": "ದೂರವಾಣಿ",
        "email": "ಇಮೇಲ್",
        "address": "ವಿಳಾಸ",
        "incidentDetails": "ಘಟನೆಯ ವಿವರಗಳು",
        "date": "ದಿನಾಂಕ",
        "location": "ಸ್ಥಳ",
        "crimeCategory": "ಅಪರಾಧ ವರ್ಗ",
        "details": "ವಿವರಗಳು",
        "witnesses": "ಸಾಕ್ಷಿಗಳು",
        "evidence": "ಸಾಕ್ಷ್ಯಗಳು",
        "aiDraft": "AI ರಚಿತ FIR ಕರಡು",
        "footer": "ಉಪಯೋಗಕ್ಕಾಗಿ: AI ಲೆಗ್ಗಲ್ ಅಸಿಸ್ಟೆಂಟ್ — ಮಾಹಿತಿಪೂರಕ ಮಾತ್ರ. ಕಾನೂನು ಸಲಹೆಗೆ ವಕೀಲರನ್ನು ಸಂಪರ್ಕಿಸಿ.",
    }
}

@app.get("/api/fir/pdf/{fir_id}")
def generate_fir_pdf(fir_id: str, language: str = "en"):
    fir = db["firs"].get(fir_id)
    if not fir:
        raise HTTPException(status_code=404, detail="FIR not found")
    
    lang = language.lower()
    labels = LABELS_MAP.get(lang, LABELS_MAP["en"])
    
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )
    story = []
    
    styles = getSampleStyleSheet()
    
    # Custom styles to support registered Unicode font if available
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName=FONT_NAME + '-Bold' if not font_registered else FONT_NAME,
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#0f172a'),
        alignment=1
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName=FONT_NAME + '-Oblique' if not font_registered else FONT_NAME,
        fontSize=9,
        leading=11,
        textColor=colors.HexColor('#64748b'),
        alignment=1
    )
    
    h2_style = ParagraphStyle(
        'SectionHeader',
        parent=styles['Heading2'],
        fontName=FONT_NAME + '-Bold' if not font_registered else FONT_NAME,
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#0f172a'),
        spaceBefore=14,
        spaceAfter=6
    )
    
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName=FONT_NAME,
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#334155')
    )
    
    bold_body_style = ParagraphStyle(
        'BoldBody',
        parent=styles['Normal'],
        fontName=FONT_NAME + '-Bold' if not font_registered else FONT_NAME,
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#0f172a')
    )
    
    story.append(Paragraph(labels["titleMain"], title_style))
    story.append(Paragraph(labels["meta"], subtitle_style))
    story.append(Spacer(1, 15))
    
    # Info Table
    info_data = [
        [Paragraph(labels["firId"], bold_body_style), Paragraph(str(fir.get("id", fir.get("_id", ""))), body_style)],
        [Paragraph(labels["title"], bold_body_style), Paragraph(fir.get("title", "—"), body_style)],
        [Paragraph(labels["status"], bold_body_style), Paragraph(fir.get("status", "draft").upper(), body_style)],
        [Paragraph(labels["submittedAt"], bold_body_style), Paragraph(fir.get("updatedAt", "—"), body_style)]
    ]
    
    t = Table(info_data, colWidths=[150, 350])
    t.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor('#f8fafc')),
        ('PADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t)
    story.append(Spacer(1, 10))
    
    # Complainant Details Section
    story.append(Paragraph(labels["complainantDetails"], h2_style))
    comp = fir.get("complainantDetails", {})
    comp_data = [
        [Paragraph(labels["name"], bold_body_style), Paragraph(comp.get("name", "—"), body_style)],
        [Paragraph(labels["phone"], bold_body_style), Paragraph(comp.get("phone", "—"), body_style)],
        [Paragraph(labels["email"], bold_body_style), Paragraph(comp.get("email", "—"), body_style)],
        [Paragraph(labels["address"], bold_body_style), Paragraph(comp.get("address", "—"), body_style)]
    ]
    t_comp = Table(comp_data, colWidths=[150, 350])
    t_comp.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor('#f8fafc')),
        ('PADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_comp)
    story.append(Spacer(1, 10))
    
    # Incident Details Section
    story.append(Paragraph(labels["incidentDetails"], h2_style))
    incident_data = [
        [Paragraph(labels["date"], bold_body_style), Paragraph(fir.get("incidentDate", "—"), body_style)],
        [Paragraph(labels["location"], bold_body_style), Paragraph(fir.get("incidentLocation", "—"), body_style)],
        [Paragraph(labels["crimeCategory"], bold_body_style), Paragraph(fir.get("crimeCategory", "—"), body_style)]
    ]
    t_inc = Table(incident_data, colWidths=[150, 350])
    t_inc.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor('#f8fafc')),
        ('PADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_inc)
    story.append(Spacer(1, 10))
    
    # Details Text Section
    story.append(Paragraph(labels["details"], h2_style))
    details_text = fir.get("incidentDetails", "—")
    story.append(Paragraph(details_text.replace('\n', '<br/>'), body_style))
    story.append(Spacer(1, 10))
    
    # Witnesses Section
    witnesses = fir.get("witnessDetails", [])
    if witnesses:
        story.append(Paragraph(labels["witnesses"], h2_style))
        for w in witnesses:
            story.append(Paragraph(f"• <b>{w.get('name', '—')}</b> (Phone: {w.get('phone', '—')})<br/>Statement: {w.get('statement', '')}", body_style))
        story.append(Spacer(1, 10))
        
    # Evidence Section
    evidence = fir.get("evidence", [])
    if evidence:
        story.append(Paragraph(labels["evidence"], h2_style))
        for ev in evidence:
            story.append(Paragraph(f"• {ev}", body_style))
        story.append(Spacer(1, 10))
        
    # AI Draft Section
    story.append(Paragraph(labels["aiDraft"], h2_style))
    draft_text = fir.get("firDraft", "—")
    story.append(Paragraph(draft_text.replace('\n', '<br/>'), body_style))
    
    # Build Document
    try:
        doc.build(story)
    except Exception as e:
        logger.error(f"PDF generation failed: {e}. Trying simple build...")
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        fallback_story = [Paragraph("FIRST INFORMATION REPORT (PDF BUILD FALLBACK)", title_style)]
        # Clean unicode characters to avoid errors
        clean_draft = "".join(c if ord(c) < 128 else ' ' for c in draft_text)
        fallback_story.append(Paragraph(clean_draft.replace('\n', '<br/>'), body_style))
        doc.build(fallback_story)
        
    buffer.seek(0)
    return Response(
        content=buffer.getvalue(),
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=FIR_{fir_id}.pdf"}
    )

# ── Audit & Admin Endpoints ──────────────────────────────────────────────────

@app.get("/api/admin/audit-logs")
def get_audit_logs(user_id: str = None, limit: int = 100, authorization: str = Header(None)):
    """Get audit logs (admin only)"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization required")
    
    token = authorization.replace("Bearer ", "")
    admin_id = decode_jwt_token(token)
    if not admin_id:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    require_admin(admin_id)
    
    if user_id:
        logs = audit_logger.get_user_logs(user_id, limit=limit)
    else:
        logs = audit_logger.get_all_logs(limit=limit)
    
    audit_logger.log_action(admin_id, "VIEW_AUDIT_LOGS", "audit", "GET", "success",
                           {"target_user": user_id, "count": len(logs)})
    return {"success": True, "data": logs, "count": len(logs)}

@app.get("/api/admin/system-health")
def system_health(authorization: str = Header(None)):
    """Get system health and statistics"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization required")
    
    token = authorization.replace("Bearer ", "")
    admin_id = decode_jwt_token(token)
    if not admin_id:
        raise HTTPException(status_code=401, detail="Invalid token")
        
    require_admin(admin_id)
        
    stats = {
        "total_users": len(db["users"].values()),
        "total_chat_sessions": len(db["chat_sessions"].values()),
        "total_firs": len(db["firs"].values()),
        "ai_status": "connected" if not test_mode else "test_mode",
        "database_type": "mongodb" if db.use_mongo else "json_local",
        "timestamp": datetime.utcnow().isoformat()
    }
    
    audit_logger.log_action(admin_id, "CHECK_HEALTH", "system", "GET", "success")
    return {"success": True, "data": stats}

@app.get("/api/admin/analytics/summary")
def get_analytics_summary(authorization: str = Header(None)):
    """Get real-time analytics summary"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization required")
    
    token = authorization.replace("Bearer ", "")
    admin_id = decode_jwt_token(token)
    if not admin_id:
        raise HTTPException(status_code=401, detail="Invalid token")
        
    require_admin(admin_id)
    
    summary = audit_logger.get_analytics_summary()
    
    # Add FIR crime category distribution
    crime_dist = {}
    for fir in db["firs"].values():
        cat = fir.get("crimeCategory", "Unknown")
        crime_dist[cat] = crime_dist.get(cat, 0) + 1
    summary["crime_distribution"] = crime_dist
    
    return {"success": True, "data": summary}

@app.get("/api/admin/analytics/stream")
async def get_analytics_stream(request: Request, token: str = None):
    """SSE endpoint for real-time analytics stream"""
    if not token:
        raise HTTPException(status_code=401, detail="Token query parameter required")
        
    admin_id = decode_jwt_token(token)
    if not admin_id:
        raise HTTPException(status_code=401, detail="Invalid token")
        
    require_admin(admin_id)

    async def event_generator():
        while True:
            if await request.is_disconnected():
                break
                
            summary = audit_logger.get_analytics_summary()
            
            crime_dist = {}
            for fir in db["firs"].values():
                cat = fir.get("crimeCategory", "Unknown")
                crime_dist[cat] = crime_dist.get(cat, 0) + 1
            summary["crime_distribution"] = crime_dist
            
            yield f"data: {json.dumps(summary)}\n\n"
            await asyncio.sleep(5)
            
    return StreamingResponse(event_generator(), media_type="text/event-stream")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
