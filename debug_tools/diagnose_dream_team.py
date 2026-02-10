
import requests
import json
import os
import sys

# Import config directly via path
sys.path.append(os.getcwd())
import config

def test_provider(name, model, url, api_key):
    print(f"📡 Testing {name} ({model})...")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model.split("/")[-1] if "/" in model and name != "Fireworks" else model,
        "messages": [{"role": "user", "content": "Say 'OK' if you are alive."}],
        "max_tokens": 10
    }
    
    # Fireworks model path is special
    if name == "Fireworks":
        payload["model"] = model.replace("fireworks/", "")

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=15)
        if resp.status_code == 200:
            content = resp.json()['choices'][0]['message']['content']
            print(f"✅ {name} responded: {content.strip()}")
            return True
        else:
            print(f"❌ {name} failed: {resp.status_code} - {resp.text}")
            return False
    except Exception as e:
        print(f"❌ {name} exception: {e}")
        return False

if __name__ == "__main__":
    print("💎 Bankoo Dream Team Connectivity Audit 💎\n")
    
    results = [
        test_provider("Groq (Llama 70B)", config.PRIMARY_MODEL, "https://api.groq.com/openai/v1/chat/completions", config.GROQ_API_KEY),
        test_provider("Cerebras (Llama 70B)", "cerebras/llama-3.3-70b", "https://api.cerebras.ai/v1/chat/completions", config.CEREBRAS_API_KEY),
    ]

    print("\n🕵️ Probing Fireworks for correct model IDs...")
    fireworks_candidates = [
        "accounts/fireworks/models/deepseek-v3",
        "accounts/fireworks/models/deepseek-v3p1",
        "accounts/fireworks/models/llama-v3p3-70b-instruct",
        "accounts/fireworks/models/llama-v3-70b-instruct"
    ]
    
    for candidate in fireworks_candidates:
        if test_provider("Fireworks Probe", candidate, "https://api.fireworks.ai/inference/v1/chat/completions", config.FIREWORKS_API_KEY):
            print(f"🌟 FOUND VALID FIREWORKS ID: {candidate}")
            results.append(True)
            break
    else:
        results.append(False)
    
    if all(results):
        print("\n🏆 Result: The AI Playground is PERFECT and fully responsive!")
    else:
        print("\n⚠️ Result: Some providers are lagging. Check API keys in config.py.")
