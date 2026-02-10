import requests
import config

key = config.BYTEZ_API_KEY
endpoints = [
    "https://api.bytez.com/models/v2",
    "https://api.bytez.com/models",
    "https://api.bytez.com/model/list",
    "https://api.bytez.com/v2/models"
]

print(f"🕵️ Probing Bytez API with key prefix: {key[:5]}...")

for url in endpoints:
    print(f"\n--- Testing Endpoint: {url} ---")
    try:
        # Try standard Bearer token
        headers = {"Authorization": f"Bearer {key}"}
        resp = requests.get(url, headers=headers, timeout=5)
        
        if resp.status_code == 200:
            print("✅ SUCCESS! Found working endpoint.")
            data = resp.json()
            
            # Parsing for Free Models
            models = data.get('data', []) if isinstance(data, dict) else data
            if isinstance(models, list):
                print(f"\n🎁 Scanning {len(models)} models for FREE options...")
                free_models = []
                for m in models:
                    # Check for 'pricing' dict or keywords
                    is_free = False
                    if 'pricing' in m and (m['pricing'].get('input') == 0 or m['pricing'].get('prompt') == 0):
                        is_free = True
                    if 'free' in m.get('id', '').lower():
                        is_free = True
                        
                    if is_free:
                        print(f"   - 🆓 {m['id']}")
                        free_models.append(m['id'])
                
                if not free_models:
                    print("   (No explicitly free models found in metadata. Try established open weights like Llama/Mistral)")
            else:
                 print(f"Raw Response: {data}")
            break
        elif resp.status_code == 401:
            print("❌ 401 Unauthorized (Key might be wrong or header format incorrect)")
        else:
            print(f"❌ {resp.status_code}: {resp.text[:100]}")
            
    except Exception as e:
        print(f"❌ Connection Failed: {e}")

print("\n(If all failed, we need the official API Documentation URL from the user)")
