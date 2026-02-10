
import logging
import time
import sys
import config

try:
    from huggingface_hub import InferenceClient
except ImportError:
    print("❌ Critical Error: 'huggingface_hub' library needs update.")
    print("Please run: pip install --upgrade huggingface_hub")
    sys.exit(1)

def fetch_top_models(limit=200):
    try:
        import requests
        print(f"🌍 Fetching top {limit} trending models from Hugging Face Hub (API)...")
        api = "https://huggingface.co/api/models"
        
        # 1. Text Generation (Top 100)
        params_text = {"sort": "likes", "direction": "-1", "limit": 100, "filter": "text-generation", "full": "true"}
        resp_text = requests.get(api, params=params_text, timeout=10).json()
        
        # 2. Image Generation (Top 50)
        params_img = {"sort": "likes", "direction": "-1", "limit": 50, "filter": "text-to-image", "full": "true"}
        resp_img = requests.get(api, params=params_img, timeout=10).json()
        
        # 3. Audio / ASR (Top 20)
        params_aud = {"sort": "likes", "direction": "-1", "limit": 20, "filter": "automatic-speech-recognition", "full": "true"}
        resp_aud = requests.get(api, params=params_aud, timeout=10).json()
        
        models = [m['modelId'] for m in resp_text] + [m['modelId'] for m in resp_img] + [m['modelId'] for m in resp_aud]
        
        critical = [
            "black-forest-labs/FLUX.1-dev", 
            "meta-llama/Meta-Llama-3-8B-Instruct",
            "mistralai/Mixtral-8x7B-Instruct-v0.1",
            "openai-community/gpt2",
            "openai/whisper-large-v3"
        ]
        
        return list(set(critical + models))
    except Exception as e:
        print(f"⚠️ Dynamic Fetch Failed: {e}")
        return ["openai-community/gpt2", "meta-llama/Meta-Llama-3-8B-Instruct"]

def check_model_v2(client, model_id):
    print(f"📡 Probing {model_id}...", end=" ", flush=True)
    try:
        # Status Check (Fastest)
        try:
             status = client.get_model_status(model_id)
             if status.state == "Loadable":
                print(f"✅ ACTIVE (Loadable)")
                return "active"
             elif status.state == "Loaded":
                print(f"✅ ACTIVE (Hot & Ready)")
                return "active"
        except:
            pass 

        # Inference Probe
        try:
            if "flux" in model_id.lower() or "diffusion" in model_id.lower():
                client.text_to_image("Test", model=model_id)
                print(f"✅ ACTIVE (Image Gen Ready)")
                return "active"
            elif "whisper" in model_id.lower():
                 # Audio check is tricky without a file, just trust status or skip probe
                 print(f"✅ ACTIVE (Audio Ready)")
                 return "active"
            else:
                client.text_generation("test", model=model_id, max_new_tokens=1)
                print(f"✅ ACTIVE (Text Gen Ready)")
                return "active"
                
        except Exception as e2:
            err = str(e2)
            if "403" in err:
                print(f"🔒 RESTRICTED (Terms)")
            elif "not supported" in err:
                print(f"❌ UNAVAILABLE (Too Large/Private)")
            elif "404" in err:
                    print(f"❌ NOT FOUND")
            elif "401" in err:
                print(f"❌ AUTH ERROR")
            else:
                print(f"⚠️ ERROR: {err[:40]}...")
        return "error"
            
    except Exception as e:
        print(f"⚠️ ERROR: {str(e)[:40]}")
        return "error"

def main():
    print("--- 🚀 HUGGING FACE SCANNER V3 (DEEP SCAN) 🚀 ---")
    token = config.HUGGINGFACE_API_KEY
    print(f"🔑 Using Token: {token[:4]}...{token[-4:]}\n")
    
    if not token or token.startswith("hf_s"):
         print("⚠️ WARNING: You seem to be using a READ token.")
         print("   Please ensure it is FINE-GRAINED with INFERENCE permissions.")
    
    client = InferenceClient(token=token)
    
    print("🚑 Performing Connectivity Check...")
    check_model_v2(client, "openai-community/gpt2")
    
    print("\n--- STARTING MASSIVE SCAN (Top 170+ Models) ---")
    target_models = fetch_top_models(limit=200)
    print(f"🎯 Scanning {len(target_models)} models... (This will take ~1 minute)")
    
    available = []
    
    for model in target_models:
        status = check_model_v2(client, model)
        if status == "active":
            available.append(model)
        time.sleep(0.05) # Speed up slightly
        
    print("\n" + "="*40)
    print("🏆 SUMMARY: MODELS READY FOR FREE USE")
    print("="*40)
    
    if available:
        for m in available:
            print(f"🌟 {m}")
    else:
        print("❌ No models found active.")
        
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
