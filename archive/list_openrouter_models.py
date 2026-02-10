import os
import requests
import config

try:
    print("📡 Querying OpenRouter for available models...")
    
    headers = {
        "Authorization": f"Bearer {config.OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    
    response = requests.get("https://openrouter.ai/api/v1/models", headers=headers, timeout=10)
    
    if response.status_code == 200:
        data = response.json()
        print("\n✅ AVAILABLE OPENROUTER MODELS (Top 50 sorted by context):")
        
        # Sort by context length to find powerful models
        models = data.get('data', [])
        # Simple filter for interesting ones
        interesting = [m for m in models if ":free" in m['id'] or "free" in m['pricing'].get('prompt', '0')]
        
        print("\n💰 DEFINITELY FREE MODELS FOUND:")
        # Print first 30 interesting ones
        for model in interesting[:30]:
            print(f"- {model['id']}")
            
        print(f"\nTotal Models Found: {len(models)}")
    else:
        print(f"❌ Error {response.status_code}: {response.text}")

except Exception as e:
    print(f"❌ Script Error: {e}")
