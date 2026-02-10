"""
AI COUNCIL MODEL VERIFICATION
Tests every expert in the council to ensure they're accessible.
"""
import requests
import config
import time

print("🧪 TESTING AI COUNCIL - 18 EXPERT VERIFICATION")
print("=" * 80)

# Extract base URL and model from the format "provider/model"
def parse_model(model_str):
    if "/" in model_str and not model_str.startswith("meta-llama"):
        # Format: "provider/model"
        parts = model_str.split("/", 1)
        provider = parts[0]
        model = parts[1]
    else:
        # OpenRouter format: "meta-llama/..."
        provider = "openrouter"
        model = model_str
    return provider, model

# Provider configurations
provider_configs = {
    "cerebras": {
        "base_url": "https://api.cerebras.ai/v1",
        "key": getattr(config, 'CEREBRAS_API_KEY', '')
    },
    "groq": {
        "base_url": "https://api.groq.com/openai/v1",
        "key": getattr(config, 'GROQ_API_KEY', '')
    },
    "fireworks": {
        "base_url": "https://api.fireworks.ai/inference/v1",
        "key": getattr(config, 'FIREWORKS_API_KEY', '')
    },
    "openrouter": {
        "base_url": "https://openrouter.ai/api/v1",
        "key": getattr(config, 'OPENROUTER_API_KEY', '')
    }
}

results = []
test_prompt = "Reply with 'OK' only."

for role, model_str in config.COUNCIL_CONFIG.items():
    print(f"\n🔍 Testing {role}...")
    print(f"   Model: {model_str}")
    
    provider, model = parse_model(model_str)
    
    if provider not in provider_configs:
        print(f"   ⚠️  Unknown provider: {provider}")
        results.append({"role": role, "status": "UNKNOWN_PROVIDER"})
        continue
    
    provider_info = provider_configs[provider]
    
    if not provider_info['key']:
        print(f"   ⚠️  No API Key for {provider}")
        results.append({"role": role, "status": "NO_KEY", "provider": provider})
        continue
    
    try:
        url = f"{provider_info['base_url']}/chat/completions"
        headers = {
            "Authorization": f"Bearer {provider_info['key']}",
            "Content-Type": "application/json"
        }
        
        # OpenRouter specific headers
        if provider == "openrouter":
            headers["HTTP-Referer"] = "http://localhost:5001"
            headers["X-Title"] = "Bankoo Council Test"
        
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": test_prompt}],
            "max_tokens": 10,
            "temperature": 0
        }
        
        start = time.time()
        resp = requests.post(url, json=payload, headers=headers, timeout=20)
        latency = round((time.time() - start) * 1000)
        
        if resp.status_code == 200:
            data = resp.json()
            reply = data['choices'][0]['message']['content']
            print(f"   ✅ ONLINE - {latency}ms")
            results.append({
                "role": role, 
                "status": "ONLINE", 
                "latency": latency,
                "provider": provider
            })
        else:
            error_msg = resp.json().get('error', {}).get('message', f'HTTP {resp.status_code}')
            print(f"   ❌ FAILED - {error_msg[:60]}")
            results.append({
                "role": role, 
                "status": "ERROR", 
                "error": error_msg,
                "provider": provider
            })
            
    except requests.exceptions.Timeout:
        print(f"   ⏱️  TIMEOUT")
        results.append({"role": role, "status": "TIMEOUT", "provider": provider})
    except Exception as e:
        print(f"   ❌ EXCEPTION: {str(e)[:60]}")
        results.append({"role": role, "status": "EXCEPTION", "error": str(e)})

# Final Report
print("\n" + "=" * 80)
print("📊 COUNCIL STATUS REPORT")
print("=" * 80)

online = [r for r in results if r['status'] == 'ONLINE']
failed = [r for r in results if r['status'] not in ['ONLINE', 'NO_KEY']]

print(f"\n✅ WORKING EXPERTS: {len(online)}/{len(config.COUNCIL_CONFIG)}")
for r in sorted(online, key=lambda x: x.get('latency', 9999)):
    print(f"   • {r['role']:<25} - {r.get('latency', 'N/A'):>5}ms ({r.get('provider', 'N/A')})")

if failed:
    print(f"\n❌ FAILED EXPERTS: {len(failed)}")
    for r in failed:
        print(f"   • {r['role']:<25} - {r['status']} ({r.get('provider', 'N/A')})")

# Provider Summary
print(f"\n📈 BY PROVIDER:")
for prov in ['cerebras', 'groq', 'fireworks', 'openrouter']:
    prov_results = [r for r in online if r.get('provider') == prov]
    print(f"   • {prov.upper():<15} - {len(prov_results)} experts working")

print("\n💡 All working experts are ready for AI Council debates!")
