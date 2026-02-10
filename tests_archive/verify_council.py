import os
import requests
import config
import time

# The Rosters from Config (Dynamic Loading)
models = {
    "PRIME": config.PRIMARY_MODEL,
    "FAST": config.FAST_MODEL,
    "JUDGE": config.COUNCIL_CONFIG["JUDGE"],
    "CODER": config.COUNCIL_CONFIG["CODER"],
    "CRITIC": config.COUNCIL_CONFIG["CRITIC"],
    "VISIONARY": getattr(config, 'CREATIVE_MODEL', "N/A"),
    "GUARDIAN": getattr(config, 'SECURITY_MODEL', "N/A")
}

headers = {
    "Authorization": f"Bearer {config.OPENROUTER_API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "http://localhost:5000", 
    "X-Title": "Bankoo Health Check"
}

print(f"🏥 BANKOO AI COUNCIL HEALTH CHECK")
print("==================================================")
print(f"Gateway: OpenRouter (Universal)")
print("==================================================\n")

for role, model_id in models.items():
    print(f"Testing {role}...")
    print(f"   Model: {model_id}")
    
    try:
        start = time.time()
        payload = {
            "model": model_id,
            "messages": [{"role": "user", "content": "Reply with 'Online'"}],
            "max_tokens": 5
        }
        
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload, timeout=20)
        
        if response.status_code == 200:
            data = response.json()
            if 'error' in data:
                 print(f"   ❌ API Error: {data['error']['message']}")
            else:
                reply = data['choices'][0]['message']['content']
                latency = round((time.time() - start) * 1000)
                print(f"   ✅ STATUS: ACTIVE ({latency}ms)")
                print(f"   💬 Reply: {reply}")
        else:
             print(f"   ❌ HTTP Error {response.status_code}: {response.text}")
             
    except Exception as e:
        print(f"   ❌ Connection Error: {e}")
    
    print("-" * 40)

print("\nHealth Check Complete.")
