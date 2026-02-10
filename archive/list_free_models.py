"""
FREE AI MODEL DISCOVERY TOOL
Scans all providers (Cerebras, Groq, DeepInfra, Fireworks, OpenRouter) 
and lists FREE models for instant access.
"""
import requests
import config

print("🔍 SCANNING ALL PROVIDERS FOR FREE AI MODELS")
print("=" * 70)

# Provider URLs
providers = {
    "Cerebras": {
        "url": "https://api.cerebras.ai/v1/models",
        "key": getattr(config, 'CEREBRAS_API_KEY', ''),
        "note": "Currently FREE (Beta)"
    },
    "Groq": {
        "url": "https://api.groq.com/openai/v1/models",
        "key": getattr(config, 'GROQ_API_KEY', ''),
        "note": "FREE tier with RPM limits"
    },
    "DeepInfra": {
        "url": "https://api.deepinfra.com/v1/openai/models",
        "key": getattr(config, 'DEEPINFRA_API_KEY', ''),
        "note": "Pay-as-you-go ($0.10/M tokens)"
    },
    "Fireworks": {
        "url": "https://api.fireworks.ai/inference/v1/models",
        "key": getattr(config, 'FIREWORKS_API_KEY', ''),
        "note": "Free trial credits"
    },
    "OpenRouter": {
        "url": "https://openrouter.ai/api/v1/models",
        "key": getattr(config, 'OPENROUTER_API_KEY', ''),
        "note": "Many FREE models"
    }
}

for provider_name, info in providers.items():
    print(f"\n🌐 {provider_name.upper()} ({info['note']})")
    print("-" * 70)
    
    if not info['key']:
        print(f"   ⚠️  No API Key configured. Skipping.")
        continue
    
    try:
        headers = {"Authorization": f"Bearer {info['key']}"}
        resp = requests.get(info['url'], headers=headers, timeout=10)
        
        if resp.status_code == 200:
            data = resp.json()
            models = data.get('data', [])
            
            if not models:
                print(f"   ⚠️  No models returned.")
                continue
            
            # Filter and display
            print(f"   📋 Available Models ({len(models)} total):\n")
            
            for idx, model in enumerate(models[:15], 1):  # Show top 15
                model_id = model.get('id', 'Unknown')
                
                # Check if free (OpenRouter specific)
                if provider_name == "OpenRouter":
                    pricing = model.get('pricing', {})
                    prompt_price = float(pricing.get('prompt', 1))
                    if prompt_price == 0 or ':free' in model_id:
                        print(f"   {idx}. 🆓 {model_id}")
                else:
                    print(f"   {idx}. {model_id}")
            
            if len(models) > 15:
                print(f"\n   ... and {len(models) - 15} more models")
        else:
            print(f"   ❌ Error: {resp.status_code}")
            
    except Exception as e:
        print(f"   ❌ Connection Failed: {e}")

print("\n" + "=" * 70)
print("✅ SCAN COMPLETE")
print("\nTo use a model, update your config.py with:")
print('   PRIMARY_MODEL = "provider/model-name"')
print('   Example: PRIMARY_MODEL = "cerebras/llama3.1-70b"')
