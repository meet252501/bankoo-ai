import requests
import config

try:
    print("📡 Querying Fireworks for available models...")
    
    headers = {
        "Authorization": f"Bearer {config.FIREWORKS_API_KEY}",
        "Content-Type": "application/json"
    }
    
    response = requests.get("https://api.fireworks.ai/inference/v1/models", headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print("\n✅ AVAILABLE MODELS:")
        for model in data.get('data', []):
            if "deepseek" in model['id'].lower() or "llama-v3p3" in model['id'].lower():
                print(f"- {model['id']}")
    else:
        print(f"❌ Error {response.status_code}: {response.text}")

except Exception as e:
    print(f"❌ Script Error: {e}")
