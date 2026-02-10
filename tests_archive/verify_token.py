
import requests
import config

token = config.HUGGINGFACE_API_KEY
headers = {"Authorization": f"Bearer {token}"}

print(f"🔑 Verifying Token: {token[:4]}...{token[-4:]}")

# 1. WhoAmI Check (Basic Auth)
try:
    resp = requests.get("https://huggingface.co/api/whoami-v2", headers=headers)
    if resp.status_code == 200:
        data = resp.json()
        print(f"✅ Auth Success! User: {data.get('name')}")
        print(f"   Type: {data.get('type')}")
        print(f"   Email Verified: {data.get('emailVerified')}")
        
        # Check Scopes
        auth = data.get('auth', {})
        access = auth.get('accessToken', {})
        fine_grained = access.get('fineGrained', {})
        
        if fine_grained:
            print(f"🔎 Token Type: FINE-GRAINED (Good)")
            scopes = fine_grained.get('scoped', [])
            print("📜 Scopes Found:")
            has_inference = False
            for s in scopes:
                print(f"   - {s}")
                if 'inference-api' in str(s): has_inference = True
            
            if has_inference:
                print("✅ INFERENCE PERMISSION FOUND!")
            else:
                print("❌ MISSING 'Inference' Scope!")
        else:
            print("⚠️ Token Type: LEGACY (Read/Write)")
            print("   Legacy tokens might not support all inference endpoints.")

    else:
        print(f"❌ Auth Failed: {resp.status_code}")
        print(resp.text)
except Exception as e:
    print(f"❌ Connection Error: {e}")

input("\nPress Enter to exit...")
