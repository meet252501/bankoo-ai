import requests
import json
import base64
import os
import time

def test_flask_health():
    print("🔍 [TEST] Checking Flask Backend Health...")
    try:
        # We'll use a standard endpoint to see if it's up
        res = requests.get("http://127.0.0.1:5001/", timeout=5)
        if res.status_code == 200:
            print("✅ Flask Backend is ONLINE.")
            return True
    except:
        print("❌ Flask Backend is OFFLINE.")
    return False

def test_vision_analyzer():
    print("\n🔍 [TEST] Checking Neural Vision Analyzer...")
    max_retries = 10
    for i in range(max_retries):
        try:
            # Create a tiny mock image (100x100 red square)
            from PIL import Image
            import io
            img = Image.new('RGB', (100, 100), color = 'red')
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='PNG')
            b64_img = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')

            payload = {
                "image": b64_img,
                "prompt": "Locate the center of the red square. Respond with ONLY JSON {x, y}."
            }
            
            res = requests.post("http://127.0.0.1:5001/api/vision/analyze", json=payload, timeout=25)
            if res.status_code == 200:
                data = res.json()
                print(f"✅ Vision Analysis Successful: {data.get('coordinates')}")
                return True
            elif res.status_code == 503:
                print(f"⏳ Brain still warming up... ({i+1}/{max_retries})")
                time.sleep(5)
            else:
                print(f"❌ Vision Analysis Failed (Code {res.status_code}): {res.text}")
                return False
        except Exception as e:
            print(f"❌ Vision test error: {e}")
            return False
    print("❌ Vision Test Timed Out (Brain took too long to load).")
    return False

if __name__ == "__main__":
    print("="*60)
    print("   BANKOO v12 CORE SMOKE TEST")
    print("="*60)
    
    if test_flask_health():
        test_vision_analyzer()
    else:
        print("\n⚠️  SKIPPING vision test because backend is unreachable.")
        print("   Make sure to run 'python bankoo_core.py' first!")
    
    print("\n" + "="*60)
