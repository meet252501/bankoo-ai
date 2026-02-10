
import logging
import time
import sys
import config
import requests
import os

try:
    from huggingface_hub import InferenceClient
except ImportError:
    print("❌ Critical Error: 'huggingface_hub' library needs update.")
    sys.exit(1)

# LOGGING SETUP
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("scan_debug.log", encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

HISTORY_FILE = "scanned_history.txt"
GOOD_MODELS_FILE = "good_models.txt"

def load_history():
    """Loads set of already scanned model IDs."""
    scanned = set()
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            for line in f:
                scanned.add(line.strip())
    
    # Also ignore models already known to be good (no need to re-verify constantly)
    if os.path.exists(GOOD_MODELS_FILE):
        with open(GOOD_MODELS_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    scanned.add(line)
                    
    print(f"📚 Loaded History: Skipping {len(scanned)} previously scanned models.")
    return scanned

def append_to_history(model_id):
    with open(HISTORY_FILE, "a", encoding="utf-8") as f:
        f.write(model_id + "\n")

def fetch_massive_model_list(limit=20000):
    print(f"🌍 Fetching Top {limit} Popular Models (EXTREME DEEP DIVE)...")
    base_api = "https://huggingface.co/api/models"
    
    params = {
        "sort": "likes",
        "direction": "-1",
        "limit": limit,
        "full": "false",
        "config": "true" 
    }
    
    try:
        resp = requests.get(base_api, params=params, timeout=45)
        data = resp.json()
        
        valid_pipeline_tags = [
            "text-generation", "text-to-image", "automatic-speech-recognition", 
            "text-to-speech", "image-classification", "translation"
        ]
        
        filtered = []
        for m in data:
            if m.get('pipeline_tag') in valid_pipeline_tags:
                filtered.append(m['modelId'])
        
        print(f"✅ API returned {len(filtered)} potential candidates.")
        return filtered
        
    except Exception as e:
        print(f"❌ API Fetch Error: {e}")
        return []

def check_model_robust(client, model_id):
    print(f"📡 {model_id:<50}", end="", flush=True)
    
    try:
        # 1. STATUS CHECK (Fast)
        try:
            status = client.get_model_status(model_id)
            if status.state in ["Loadable", "Loaded"]:
                print("✅ ACTIVE (Status)")
                return "active"
        except:
            pass 

        # 2. INFERENCE CHECK
        try:
            if "flux" in model_id.lower() or "diffusion" in model_id.lower():
                client.text_to_image("Test", model=model_id)
                print("✅ ACTIVE (Image Gen)")
                return "active"
            elif "whisper" in model_id.lower():
                print("✅ ACTIVE (Audio Assumed)")
                return "active"
            else:
                client.text_generation("test", model=model_id, max_new_tokens=1)
                print("✅ ACTIVE (Text Gen)")
                return "active"
                
        except Exception as e:
            err = str(e)
            if "not supported" in err:
                print("❌ Too Large/No API")
            elif "403" in err:
                print("🔒 Gated/Terms")
            elif "404" in err:
                print("❌ Not Found")
            elif "401" in err:
                 print("❌ Auth Fail")
            elif "504" in err or "503" in err:
                 print("⏳ Loading/Timeout") # Treat timeouts as potentially active but cold
                 return "loading"
            else:
                print(f"⚠️ Error")
            return "error"
            
    except Exception as e:
        print(f"⚠️ Sys Error")
        return "error"

def main():
    print("--- 🌌 MASSIVE HUGGING FACE DEEP SCANNER V2 (SMART) 🌌 ---")
    print("Feature: Skips already checked models. Goes 5x deeper.")
    print(f"Results -> {GOOD_MODELS_FILE}")
    print(f"History -> {HISTORY_FILE}\n")
    
    token = config.HUGGINGFACE_API_KEY
    client = InferenceClient(token=token)
    
    # Load History
    already_scanned = load_history()
    
    # Fetch Candidates
    candidates = fetch_massive_model_list(limit=20000)
    
    # Filter
    to_scan = [m for m in candidates if m not in already_scanned]
    print(f"🎯 New models to scan: {len(to_scan)} (Skipped {len(candidates) - len(to_scan)})")
    
    if not to_scan:
        print("🎉 You have already scanned all top 20,000 models! Nothing new to do.")
        input("Press Enter to exit...")
        return

    count = 0
    active_count = 0
    
    for model in to_scan:
        count += 1
        if count % 20 == 0: time.sleep(1) # Rate limit niceness
        
        res = check_model_robust(client, model)
        
        # Log to history regardless of result so we don't check again
        append_to_history(model)
        
        if res == "active" or res == "loading":
            active_count += 1
            with open(GOOD_MODELS_FILE, "a", encoding="utf-8") as f:
                f.write(model + "\n")
                
    print("\n" + "="*40)
    print(f"🏁 SCAN COMPLETE. Found {active_count} New Active Models.")
    print("="*40)
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()
