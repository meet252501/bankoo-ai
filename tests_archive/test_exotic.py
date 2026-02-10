import os
import requests
import config

models_to_test = [
    "openai/gpt-oss-120b",
    "moonshotai/kimi-k2-instruct"
]

headers = {
    "Authorization": f"Bearer {config.GROQ_API_KEY}",
    "Content-Type": "application/json"
}

print("🧪 Testing Exotic Models...")

for model in models_to_test:
    try:
        print(f"\n--- Testing {model} ---")
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": "Say 'Active'"}]
        }
        res = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload, timeout=10)
        
        if res.status_code == 200:
            print(f"✅ {model} is ALIVE!")
            print(f"Response: {res.json()['choices'][0]['message']['content']}")
        else:
            print(f"❌ {model} Failed: {res.status_code} - {res.text}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")
