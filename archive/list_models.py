import os
import requests
import config

try:
    print("📡 Querying Groq for available models...")
    
    headers = {
        "Authorization": f"Bearer {config.GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    response = requests.get("https://api.groq.com/openai/v1/models", headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print("\n✅ AVAILABLE MODELS:")
        for model in data.get('data', []):
            print(f"- {model['id']}")
    else:
        print(f"❌ Error {response.status_code}: {response.text}")

except Exception as e:
    print(f"❌ Script Error: {e}")
