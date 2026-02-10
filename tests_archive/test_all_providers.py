"""
AI PROVIDER VERIFICATION TOOL
Tests if all configured providers and their models are actually accessible.
"""
import requests
import config
import time

print("🧪 TESTING ALL AI PROVIDERS - LIVE VERIFICATION")
print("=" * 70)

# Test configurations
test_prompt = "Say 'OK' if you can hear me."

providers = {
    "Cerebras": {
        "base_url": "https://api.cerebras.ai/v1",
        "key": getattr(config, 'CEREBRAS_API_KEY', ''),
        "test_model": "llama-3.3-70b"  # Fixed: From live scan
    },
    "Groq": {
        "base_url": "https://api.groq.com/openai/v1",
        "key": getattr(config, 'GROQ_API_KEY', ''),
        "test_model": "llama-3.3-70b-versatile"
    },
    "DeepInfra": {
        "base_url": "https://api.deepinfra.com/v1/openai",
        "key": getattr(config, 'DEEPINFRA_API_KEY', ''),
        "test_model": "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo"  # Smaller = Cheaper test
    },
    "Fireworks": {
        "base_url": "https://api.fireworks.ai/inference/v1",
        "key": getattr(config, 'FIREWORKS_API_KEY', ''),
        "test_model": "accounts/fireworks/models/llama-v3p3-70b-instruct"  # Fixed: From live scan
    },
    "OpenRouter": {
        "base_url": "https://openrouter.ai/api/v1",
        "key": getattr(config, 'OPENROUTER_API_KEY', ''),
        "test_model": "meta-llama/llama-3.3-70b-instruct:free"
    }
}

results = []

for provider_name, info in providers.items():
    print(f"\n🔌 Testing {provider_name.upper()}...")
    print("-" * 70)
    
    if not info['key']:
        print(f"   ⚠️  No API Key - SKIPPED")
        results.append({"provider": provider_name, "status": "NO_KEY"})
        continue
    
    try:
        # Test API call
        url = f"{info['base_url']}/chat/completions"
        headers = {
            "Authorization": f"Bearer {info['key']}",
            "Content-Type": "application/json"
        }
        
        # Add OpenRouter specific headers
        if provider_name == "OpenRouter":
            headers["HTTP-Referer"] = "http://localhost:5001"
            headers["X-Title"] = "Bankoo Test"
        
        payload = {
            "model": info['test_model'],
            "messages": [{"role": "user", "content": test_prompt}],
            "max_tokens": 20,
            "temperature": 0
        }
        
        start = time.time()
        resp = requests.post(url, json=payload, headers=headers, timeout=15)
        latency = round((time.time() - start) * 1000)
        
        if resp.status_code == 200:
            data = resp.json()
            reply = data['choices'][0]['message']['content']
            print(f"   ✅ ONLINE - Latency: {latency}ms")
            print(f"   💬 Reply: {reply[:50]}")
            results.append({"provider": provider_name, "status": "ONLINE", "latency": latency})
        else:
            error = resp.json().get('error', {}).get('message', 'Unknown error')
            print(f"   ❌ FAILED - Status {resp.status_code}")
            print(f"   📛 Error: {error[:100]}")
            results.append({"provider": provider_name, "status": "ERROR", "error": error})
            
    except requests.exceptions.Timeout:
        print(f"   ⏱️  TIMEOUT - Server too slow or unreachable")
        results.append({"provider": provider_name, "status": "TIMEOUT"})
    except Exception as e:
        print(f"   ❌ EXCEPTION: {str(e)[:100]}")
        results.append({"provider": provider_name, "status": "EXCEPTION", "error": str(e)})

# Summary
print("\n" + "=" * 70)
print("📊 FINAL REPORT")
print("=" * 70)

online = [r for r in results if r['status'] == 'ONLINE']
failed = [r for r in results if r['status'] not in ['ONLINE', 'NO_KEY']]

print(f"\n✅ WORKING PROVIDERS: {len(online)}/{len([r for r in results if r['status'] != 'NO_KEY'])}")
for r in online:
    print(f"   • {r['provider']:<15} - {r.get('latency', 'N/A')}ms")

if failed:
    print(f"\n❌ FAILED PROVIDERS: {len(failed)}")
    for r in failed:
        print(f"   • {r['provider']:<15} - {r['status']}")

print("\n💡 TIP: If a provider failed, check:")
print("   1. API Key is correct in config.py")
print("   2. You have credits/quota remaining")
print("   3. The test model name is valid for that provider")
