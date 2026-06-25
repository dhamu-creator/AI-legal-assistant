# AI Legal Assistant - Security & Audit Module
# Provides rate limiting, audit logging, and security enhancements

from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json
import os
from collections import defaultdict, deque
from threading import Lock

# ── Rate Limiting ──────────────────────────────────────────────────────────

class RateLimiter:
    """Token bucket rate limiter per user/IP and endpoint type"""
    
    def __init__(self, default_requests_per_minute: int = 60):
        self.default_rpm = default_requests_per_minute
        self.endpoint_limits = {
            "default": default_requests_per_minute,
            "fir_generate": 10,  # Stricter limit for heavy operations
            "auth": 20           # Login/Register limit
        }
        self.requests = defaultdict(lambda: deque(maxlen=200))
        self.lock = Lock()
    
    def is_allowed(self, identifier: str, endpoint_type: str = "default") -> bool:
        """Check if request is allowed for identifier (user_id or IP) on specific endpoint"""
        with self.lock:
            now = datetime.utcnow()
            minute_ago = now - timedelta(minutes=1)
            hour_ago = now - timedelta(hours=1)
            
            # Use compound key for per-endpoint tracking
            key = f"{identifier}:{endpoint_type}"
            requests = self.requests[key]
            
            # Remove old requests outside window
            while requests and requests[0] < hour_ago:
                requests.popleft()
            
            # Check rate limits
            recent_minute = sum(1 for t in requests if t > minute_ago)
            recent_hour = len(requests)
            
            limit_rpm = self.endpoint_limits.get(endpoint_type, self.default_rpm)
            limit_rph = limit_rpm * 10
            
            if recent_minute >= limit_rpm:
                return False
            if recent_hour >= limit_rph:
                return False
            
            # Add current request
            requests.append(now)
            return True
    
    def get_remaining(self, identifier: str) -> dict:
        """Get remaining requests for identifier"""
        with self.lock:
            now = datetime.utcnow()
            minute_ago = now - timedelta(minutes=1)
            
            requests = self.requests[identifier]
            recent_minute = sum(1 for t in requests if t > minute_ago)
            
            return {
                "remaining_this_minute": max(0, self.requests_per_minute - recent_minute),
                "total_requests_per_minute": self.requests_per_minute
            }

# ── Audit Logging ──────────────────────────────────────────────────────────

class AuditLogger:
    """Audit logger for tracking user actions"""
    
    def __init__(self, db_interface=None):
        self.db = db_interface
        self.logs_file = os.path.join(os.path.dirname(__file__), "audit_logs.json")
        self.in_memory_logs = deque(maxlen=10000)
        self.lock = Lock()
        self._init_audit_collection()
    
    def _init_audit_collection(self):
        """Initialize audit logs collection"""
        if self.db and hasattr(self.db, 'mongo_db'):
            try:
                if self.db.mongo_db and 'audit_logs' not in self.db.mongo_db.list_collection_names():
                    self.db.mongo_db.create_collection('audit_logs')
                    self.db.mongo_db.audit_logs.create_index('timestamp')
                    self.db.mongo_db.audit_logs.create_index('user_id')
                    print("Audit logs collection initialized in MongoDB")
            except Exception as e:
                print(f"Failed to init audit collection: {e}")
    
    def log_action(self, user_id: str, action: str, resource: str, 
                   method: str, status: str, details: dict = None):
        """Log user action"""
        log_entry = {
            "id": os.urandom(12).hex(),
            "user_id": user_id,
            "action": action,
            "resource": resource,
            "method": method,
            "status": status,
            "timestamp": datetime.utcnow().isoformat(),
            "details": details or {}
        }
        
        with self.lock:
            self.in_memory_logs.append(log_entry)
            
            if self.db and hasattr(self.db, 'mongo_db') and self.db.mongo_db:
                try:
                    self.db.mongo_db.audit_logs.insert_one(log_entry)
                except Exception as e:
                    print(f"Failed to log to MongoDB: {e}")
            
            self._save_to_file(log_entry)
    
    def _save_to_file(self, log_entry: dict):
        """Save log entry to local JSON file"""
        try:
            logs = []
            if os.path.exists(self.logs_file):
                with open(self.logs_file, 'r', encoding='utf-8') as f:
                    logs = json.load(f) or []
            
            logs.append(log_entry)
            logs = logs[-1000:]
            
            with open(self.logs_file, 'w', encoding='utf-8') as f:
                json.dump(logs, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Failed to save audit log to file: {e}")
    
    def get_user_logs(self, user_id: str, limit: int = 100) -> list:
        """Get audit logs for a specific user"""
        logs = []
        
        if self.db and hasattr(self.db, 'mongo_db') and self.db.mongo_db:
            try:
                logs = list(self.db.mongo_db.audit_logs
                           .find({"user_id": user_id})
                           .sort("timestamp", -1)
                           .limit(limit))
                return logs
            except Exception as e:
                print(f"Failed to get logs from MongoDB: {e}")
        
        user_logs = [log for log in self.in_memory_logs if log['user_id'] == user_id]
        return sorted(user_logs, key=lambda x: x['timestamp'], reverse=True)[:limit]
    
    def get_all_logs(self, limit: int = 500) -> list:
        """Get all audit logs (admin only)"""
        logs = []
        
        if self.db and hasattr(self.db, 'mongo_db') and self.db.mongo_db:
            try:
                logs = list(self.db.mongo_db.audit_logs
                           .find({})
                           .sort("timestamp", -1)
                           .limit(limit))
                return logs
            except Exception as e:
                print(f"Failed to get logs from MongoDB: {e}")
        
        return sorted(list(self.in_memory_logs), key=lambda x: x['timestamp'], reverse=True)[:limit]

    def get_analytics_summary(self) -> dict:
        """Get aggregated analytics from audit logs for the last 24 hours"""
        now = datetime.utcnow()
        day_ago = now - timedelta(days=1)
        
        logs = []
        if self.db and hasattr(self.db, 'mongo_db') and self.db.mongo_db:
            try:
                logs = list(self.db.mongo_db.audit_logs.find({"timestamp": {"$gte": day_ago.isoformat()}}))
            except Exception as e:
                print(f"Failed to get analytics logs from MongoDB: {e}")
                logs = [log for log in self.in_memory_logs if log.get('timestamp') and datetime.fromisoformat(log['timestamp']) >= day_ago]
        else:
            logs = [log for log in self.in_memory_logs if log.get('timestamp') and datetime.fromisoformat(log['timestamp']) >= day_ago]
            
        active_users = len(set(log['user_id'] for log in logs if 'user_id' in log))
        
        actions = defaultdict(int)
        hourly_activity = defaultdict(int)
        
        for log in logs:
            actions[log.get('action', 'unknown')] += 1
            try:
                log_time = datetime.fromisoformat(log['timestamp'])
                hour_key = log_time.strftime("%Y-%m-%d %H:00")
                hourly_activity[hour_key] += 1
            except Exception:
                pass
            
        return {
            "active_users_24h": active_users,
            "total_actions_24h": len(logs),
            "action_breakdown": dict(actions),
            "hourly_activity": dict(hourly_activity)
        }

# ── JWT Refresh Token Support ──────────────────────────────────────────────

class RefreshTokenManager:
    """Manage refresh tokens for extended sessions"""
    
    def __init__(self, db_interface=None):
        self.db = db_interface
        self.tokens_file = os.path.join(os.path.dirname(__file__), "refresh_tokens.json")
        self.in_memory_tokens = {}
        self.lock = Lock()
        self._init_token_collection()
    
    def _init_token_collection(self):
        """Initialize refresh tokens collection"""
        if self.db and hasattr(self.db, 'mongo_db'):
            try:
                if self.db.mongo_db and 'refresh_tokens' not in self.db.mongo_db.list_collection_names():
                    self.db.mongo_db.create_collection('refresh_tokens')
                    self.db.mongo_db.refresh_tokens.create_index('user_id')
                    self.db.mongo_db.refresh_tokens.create_index('expires_at')
                    print("Refresh tokens collection initialized")
            except Exception as e:
                print(f"Failed to init refresh tokens: {e}")
    
    def create_refresh_token(self, user_id: str) -> str:
        """Create a refresh token"""
        import uuid
        token = str(uuid.uuid4())
        expires_at = datetime.utcnow() + timedelta(days=30)
        
        token_data = {
            "token": token,
            "user_id": user_id,
            "created_at": datetime.utcnow().isoformat(),
            "expires_at": expires_at.isoformat(),
            "revoked": False
        }
        
        with self.lock:
            self.in_memory_tokens[token] = token_data
            
            if self.db and hasattr(self.db, 'mongo_db') and self.db.mongo_db:
                try:
                    self.db.mongo_db.refresh_tokens.insert_one(token_data)
                except Exception as e:
                    print(f"Failed to save refresh token: {e}")
        
        return token
    
    def validate_refresh_token(self, token: str) -> Optional[str]:
        """Validate refresh token and return user_id if valid"""
        with self.lock:
            token_data = self.in_memory_tokens.get(token)
            if token_data and not token_data['revoked']:
                expires = datetime.fromisoformat(token_data['expires_at'])
                if datetime.utcnow() < expires:
                    return token_data['user_id']
            
            if self.db and hasattr(self.db, 'mongo_db') and self.db.mongo_db:
                try:
                    token_data = self.db.mongo_db.refresh_tokens.find_one({
                        "token": token,
                        "revoked": False
                    })
                    if token_data:
                        expires = datetime.fromisoformat(token_data['expires_at'])
                        if datetime.utcnow() < expires:
                            return token_data['user_id']
                except Exception as e:
                    print(f"Failed to validate refresh token: {e}")
        
        return None
    
    def revoke_refresh_token(self, token: str):
        """Revoke a refresh token"""
        with self.lock:
            if token in self.in_memory_tokens:
                self.in_memory_tokens[token]['revoked'] = True
            
            if self.db and hasattr(self.db, 'mongo_db') and self.db.mongo_db:
                try:
                    self.db.mongo_db.refresh_tokens.update_one(
                        {"token": token},
                        {"$set": {"revoked": True}}
                    )
                except Exception as e:
                    print(f"Failed to revoke token: {e}")

# ── Security Headers Middleware ──────────────────────────────────────────

SECURITY_HEADERS = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "X-XSS-Protection": "1; mode=block",
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
    "Content-Security-Policy": "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'",
    "Referrer-Policy": "strict-origin-when-cross-origin"
}

def apply_security_headers(response):
    """Apply security headers to response"""
    for header, value in SECURITY_HEADERS.items():
        response.headers[header] = value
    return response
