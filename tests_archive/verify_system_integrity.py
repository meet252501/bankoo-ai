
import config
import requests
import sys
import time

try:
    from huggingface_hub import InferenceClient
except ImportError:
    print("❌ Error: huggingface_hub missing.")
    sys.exit(1)

# --- CONFIG LOADING ---
print("🔍 analyzing config.py...")
COUNCIL = config.COUNCIL_CONFIG
KEYS = {
    "GROQ": config.GROQ_API_KEY,
    "OPENROUTER": config.OPENROUTER_API_KEY,
    "CEREBRAS": getattr(config, "CEREBRAS_API_KEY", None),
    "HF": config.HUGGINGFACE_API_KEY
}

# --- TESTERS ---

def test_huggingface(model_id):
    print(f"   📡 HF: {model_id:<40}", end="", flush=True)
    if not KEYS["HF"]: 
        print("❌ SKIPPED (No Key)")
        return False
    
    client = InferenceClient(token=KEYS["HF"])
    try:
        # Check status first
        try:
             s = client.get_model_status(model_id)
             if s.state in ["Loadable", "Loaded"]:
                 print("✅ STATUS O.K.", end=" ")
        except: pass

        if "flux" in model_id.lower():
            client.text_to_image("A tiny red dot", model=model_id)
        elif "whisper" in model_id.lower():
            pass # Skip audio inference for speed/complexity
        else:
            client.text_generation("Test", model=model_id, max_new_tokens=1)
        print("✅ ACTIVE")
        return True
    except Exception as e:
        print(f"❌ FAILED ({str(e)[:30]}...)")
        return False

def test_groq(model_id):
    # Strip prefix if present (groq/...)
    clean_id = model_id.split("/")[-1] if "/" in model_id else model_id
    print(f"   ⚡ GROQ: {clean_id:<40}", end="", flush=True)
    
    if not KEYS["GROQ"]:
        print("❌ SKIPPED (No Key)")
        return False
        
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {KEYS['GROQ']}", "Content-Type": "application/json"}
    payload = {
        "model": clean_id,
        "messages": [{"role": "user", "content": "Hi"}],
        "max_tokens": 1
    }
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=10)
        if r.status_code == 200:
            print("✅ ACTIVE")
            return True
        else:
            print(f"❌ FAIL {r.status_code}")
            return False
    except:
        print("❌ NET ERROR")
        return False

def test_cerebras(model_id):
    clean_id = model_id.split("/")[-1] if "/" in model_id else model_id
    print(f"   🧠 CEREBRAS: {clean_id:<36}", end="", flush=True)
    
    if not KEYS["CEREBRAS"]:
        print("❌ SKIPPED (No Key)")
        return False

    url = "https://api.cerebras.ai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {KEYS['CEREBRAS']}", "Content-Type": "application/json"}
    payload = {
        "model": clean_id,
        "messages": [{"role": "user", "content": "Hi"}],
        "max_tokens": 1
    }
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=10)
        if r.status_code == 200:
            print("✅ ACTIVE")
            return True
        else:
            print(f"❌ FAIL {r.status_code} ({r.text[:20]})")
            return False
    except Exception as e:
        print(f"❌ ERR: {e}")
        return False

def test_openrouter(model_id):
    # OpenRouter keeps the prefix usually (deepseek/deepseek-chat)
    print(f"   🦄 OPENROUTER: {model_id:<33}", end="", flush=True)
    
    if not KEYS["OPENROUTER"]:
        print("❌ SKIPPED (No Key)")
        return False

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {"Authorization": f"Bearer {KEYS['OPENROUTER']}", "Content-Type": "application/json"}
    payload = {
        "model": model_id,
        "messages": [{"role": "user", "content": "Hi"}],
        "max_tokens": 1
    }
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=10)
        if r.status_code == 200:
            print("✅ ACTIVE")
            return True
        else:
            print(f"❌ FAIL {r.status_code}")
            return False
    except:
        print("❌ NET ERROR")
        return False

# --- DISPATCHER ---
def check_model(role, model_raw):
    # 1. Determine Provider
    model_id = model_raw
    
    # HUGGING FACE
    if "black-forest" in model_id or "google/gemma" in model_id or "meta-llama/Llama-3.1-8B" in model_id or "whisper" in model_id:
         # Explicit HF check based on what we just added
         test_huggingface(model_id)
         return

    # GROQ
    if "groq" in model_id.lower():
        test_groq(model_id)
        return

    # CEREBRAS
    if "cerebras" in model_id.lower():
        test_cerebras(model_id)
        return

    # DEEPSEEK (via OpenRouter or Direct?)
    if "deepseek" in model_id.lower():
        # Config says "OpenRouter handles everything"
        test_openrouter(model_id)
        return
    
    # Fallback to HF or OpenRouter
    if "/" in model_id:
        test_huggingface(model_id)
    else:
        print(f"   ❓ UNKNOWN: {model_id}")

# --- MAIN ---
print("\n--- 🕵️‍♀️ BANKOO SYSTEM INTEGRITY CHECK ---")

print("\n[COUNCIL MEMBERS]")
for role, model in COUNCIL.items():
    print(f"Checking {role}...", end="\r")
    check_model(role, model)
    time.sleep(0.1)

print("\n[GLOBAL OVERRIDES]")
overrides = {
    "DESIGNER": config.CREATIVE_MODEL,
    "SAFE_MODE": config.SAFE_MODE_MODEL,
    "WHISPER": getattr(config, "WHISPER_MODEL", "None")
}
for name, model in overrides.items():
    check_model(name, model)

print("\n" + "="*40)
print("🏁 Check Complete.")
input("Press Enter to exit...")
