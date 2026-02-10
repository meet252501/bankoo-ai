
import requests
import config

token = config.HUGGINGFACE_API_KEY
headers = {"Authorization": f"Bearer {token}"}

print(f"🔑 Debugging Endpoints with Token: {token[:4]}...")

# Target Model: GPT2 is the safest baseline
models = ["gpt2", "openai-community/gpt2", "distilbert/distilgpt2"]

# Endpoint format variations
endpoints = [
    "https://router.huggingface.co/hf-inference/models/",
    "https://router.huggingface.co/hf-inference/v1/", 
    "https://router.huggingface.co/hf-inference/",
    "https://api-inference.huggingface.co/models/" # Old fallback
]

payload = {"inputs": "Hello world"}

print("\n--- STARTING PROBE ---")

for model in models:
    print(f"\n📡 Probing Model: {model}")
    for base in endpoints:
        url = f"{base}{model}"
        print(f"   URL: {url}")
        try:
            r = requests.post(url, headers=headers, json=payload, timeout=5)
            print(f"   👉 Status: {r.status_code}")
            if r.status_code == 200:
                print(f"   ✅ SUCCESS! Response: {r.text[:60]}...")
            else:
                print(f"   ❌ Fail: {r.status_code} - {r.text[:100]}")
        except Exception as e:
            print(f"   ⚠️ Exception: {e}")

print("\n--- DONE ---")
input("Press Enter to exit...")
