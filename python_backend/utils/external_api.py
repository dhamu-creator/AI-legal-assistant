import random
import time
import uuid

class ExternalAPIService:
    """
    A mock service that simulates integrating with external government portals
    and cybercrime databases.
    """
    
    @staticmethod
    def submit_efir(fir_details: dict) -> dict:
        """
        Simulates submitting an e-FIR to the CCTNS or State Police Portal.
        """
        # Simulate network latency
        time.sleep(1.5)
        
        # Generate a mock tracking ID
        tracking_id = f"CCTNS-{random.randint(10000, 99999)}-{random.choice(['DL', 'MH', 'UP', 'KA'])}"
        
        return {
            "status": "success",
            "tracking_id": tracking_id,
            "submission_timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "message": "FIR draft successfully transmitted to the central mock portal."
        }
        
    @staticmethod
    def check_fraud_registry(entities: list) -> dict:
        """
        Simulates querying a national cybercrime registry (like Indian Cyber Crime Coordination Centre)
        for known malicious UPI IDs, URLs, or phone numbers.
        """
        # Simulate network latency
        time.sleep(1.0)
        
        results = {}
        for entity in entities:
            # Deterministic mocking based on the entity string
            if "scam" in entity.lower() or "fraud" in entity.lower():
                score = random.randint(80, 100)
            elif "@" in entity or ".com" in entity:
                # Randomize somewhat for realistic feeling
                score = random.randint(10, 90)
            else:
                score = random.randint(0, 50)
                
            risk_level = "High" if score >= 75 else "Medium" if score >= 40 else "Low"
            
            results[entity] = {
                "risk_score": score,
                "risk_level": risk_level,
                "reports_count": random.randint(0, 50) if score > 40 else 0
            }
            
        return {
            "registry": "Mock Cybercrime Intelligence Platform",
            "entities_scanned": len(entities),
            "results": results
        }
