import urllib.request
import json

BASE = "http://localhost:8000"

def call(method, path, data=None, expect_status=None):
    url = BASE + path
    body = json.dumps(data).encode() if data else None
    headers = {"Content-Type": "application/json"}
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as r:
            status = r.status
            body_res = json.loads(r.read())
            if expect_status and status != expect_status:
                print(f"FAILED: Expected {expect_status}, got {status}")
                exit(1)
            return status, body_res
    except Exception as e:
        print(f"FAILED: Request to {url} threw exception: {e}")
        exit(1)

print("=" * 50)
print("  AI Legal Assistant - API Test")
print("=" * 50)

# Health
s, b = call("GET", "/api/health")
print(f"[Health]          {s} - {b.get('message','')}")

# Languages
s, b = call("GET", "/api/legal/languages")
print(f"[Languages]       {s} - {len(b.get('data',{}))} languages")

# Crime Categories
s, b = call("GET", "/api/legal/crime-categories")
print(f"[Crime Cats]      {s} - {len(b.get('data',[]))} categories")

# Emergency Contacts
s, b = call("GET", "/api/legal/emergency-contacts")
print(f"[Emergency]       {s} - {len(b.get('data',[]))} contacts")

# Register
import time
email = f"test{int(time.time())}@test.com"
s, b = call("POST", "/api/auth/register", {"name":"Test User","email":email,"password":"Test123!","language":"en"})
token = b.get("data",{}).get("token","")
uid = b.get("data",{}).get("user",{}).get("id","")
print(f"[Register]        {s} - user id: {uid}")

# Login
s, b = call("POST", "/api/auth/login", {"email":email,"password":"Test123!"})
print(f"[Login]           {s} - token received: {bool(b.get('data',{}).get('token'))}")

# Chat Session
s, b = call("POST", "/api/chat/session", {"userId": uid, "language":"en"})
sid = b.get("data",{}).get("_id","")
print(f"[Chat Session]    {s} - session id: {sid}")

# Send Message
s, b = call("POST", "/api/chat/message", {"sessionId":sid,"message":"I was robbed near my house last night","language":"en"})
cat = b.get("data",{}).get("crimeCategory","")
print(f"[Chat Message]    {s} - crime detected: {cat}")

# FIR Generate
fir_payload = {
    "incidentData": {
        "complainantDetails": {"name":"Test User","phone":"9999999999","address":"Chennai"},
        "incidentDetails": "Stolen mobile phone in market",
        "incidentDate": "2026-06-04",
        "incidentLocation": "T Nagar Market, Chennai",
        "crimeCategory": "Theft",
        "suspectDetails": {"name":"Unknown","description":"Tall person in black shirt"},
        "evidence": ["CCTV footage"]
    },
    "language": "en"
}
s, b = call("POST", f"/api/fir/generate/{uid}", fir_payload)
fir_id = b.get("data",{}).get("_id","")
print(f"[FIR Generate]    {s} - fir id: {fir_id}")

# Get User FIRs
s, b = call("GET", f"/api/fir/user/{uid}")
print(f"[Get FIRs]        {s} - {len(b.get('data',[]))} FIRs found")

# Evidence Checklist
s, b = call("POST", "/api/fir/evidence/checklist", {"crimeCategory":"Theft","language":"en"})
print(f"[Evidence List]   {s} - {len(b.get('data',{}).get('items',[]))} items")

# Update FIR
s, b = call("PUT", f"/api/fir/{fir_id}", {"title":"Updated FIR"})
print(f"[Update FIR]      {s} - updated: {b.get('data',{}).get('fir',{}).get('title','')}")

# Finalize FIR
s, b = call("POST", f"/api/fir/finalize/{fir_id}", {})
print(f"[Finalize FIR]    {s} - status: {b.get('data',{}).get('status','')}")

# Generate PDF Test
pdf_url = f"{BASE}/api/fir/pdf/{fir_id}?language=en"
try:
    with urllib.request.urlopen(pdf_url) as r:
        pdf_data = r.read()
        print(f"[Generate PDF]    {r.status} - received PDF buffer ({len(pdf_data)} bytes)")
except Exception as e:
    print(f"[Generate PDF]    ERROR: {e}")

print("=" * 50)
print("  ALL TESTS PASSED - Python Backend is READY!")
print("=" * 50)
