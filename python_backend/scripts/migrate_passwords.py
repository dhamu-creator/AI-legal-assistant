import json
import os
import sys

# Since we're in python_backend/scripts, we need to locate database.json correctly
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.dirname(CURRENT_DIR)
DB_FILEPATH = os.path.join(BACKEND_DIR, "database.json")

# we might need bcrypt, let's use the actual bcrypt library used in main.py
import bcrypt

def migrate_json_database(filepath=DB_FILEPATH):
    if not os.path.exists(filepath):
        print(f"[-] Migration skipped: {filepath} not found.")
        return

    with open(filepath, "r+", encoding="utf-8") as file:
        data = json.load(file)
        updated = False
        
        users = data.get("users", {})
        for uid, user in users.items():
            # Check if password string lacks a valid bcrypt blowfish prefix ($2b$)
            if not user["password"].startswith("$2b$"):
                # Use standard bcrypt library since that's what's in requirements.txt
                salt = bcrypt.gensalt()
                hashed = bcrypt.hashpw(user["password"].encode('utf-8'), salt)
                user["password"] = hashed.decode('utf-8')
                updated = True
        
        if updated:
            file.seek(0)
            json.dump(data, file, indent=2, ensure_ascii=False)
            file.truncate()
            print("[+] Success: All plaintext passwords migrated to bcrypt.")
        else:
            print("[*] Info: No legacy plaintext passwords detected.")

if __name__ == "__main__":
    migrate_json_database()
