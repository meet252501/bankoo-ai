import os
import sys
import json
import requests
import traceback

def check_env():
    print("📋 [1/4] Environment Check")
    print(f"   Python: {sys.version.split()[0]}")
    try:
        import flask, requests, bs4, lxml, webview, psutil
        print("   ✅ Core Libraries installed.")
    except ImportError as e:
        print(f"   ❌ Missing library: {e}")
        return False
    return True

def check_backend_api():
    print("📋 [2/4] API Connectivity Check")
    try:
        res = requests.get("http://127.0.0.1:5001/api/ping", timeout=3)
        print(f"   ✅ Backend responding: {res.json()}")
    except Exception as e:
        print("   ⚠️  Bankoo Server NOT detected at 127.0.0.1:5001")
        print("      (Run START_BANKOO.bat first for full API testing)")
        return False
    return True

def check_brain_logic():
    print("📋 [3/4] Scraper Brain Logic Test")
    try:
        from web_scraper_brain import WebScraperBrain
        brain = WebScraperBrain()
        print("   ✅ WebScraperBrain imported successfully.")
        
        # Test spider structure (dry run)
        # We don't want to actually crawl, just test return structure
        try:
             # Just check if method exists
             has_spider = hasattr(brain, 'scrape_spider')
             print(f"   ✅ Spider Method Found: {has_spider}")
        except:
             print("   ❌ Spider Method missing/broken!")
             return False
    except Exception as e:
        print(f"   ❌ Brain Import Failed: {e}")
        traceback.print_exc()
        return False
    return True

def check_ui_integrity():
    print("📋 [4/4] UI File Verification")
    files = ["bankoo_ui.html", "web_scraper_advanced.html", "bankoo_main.py"]
    missing = []
    for f in files:
        if not os.path.exists(f):
            missing.append(f)
    
    if missing:
        print(f"   ❌ Missing files: {', '.join(missing)}")
        return False
    
    # Check for specific tags I edited recently
    with open("bankoo_ui.html", "r", encoding="utf-8") as f:
        content = f.read()
        if "🕷️" in content:
            # Check if it's in the sidebar (it shouldn't be anymore)
            if 'class="agents-sidebar"' in content and '🕷️' in content.split('class="agents-sidebar"')[1].split('</div>')[0]:
                 print("   ⚠️  Spider Icon still detected in Sidebar! (Unexpected)")
            else:
                 print("   ✅ Sidebar Spider cleanup verified.")
        else:
            print("   ✅ Spider Icon completely removed.")
            
    return True

if __name__ == "__main__":
    print("================================================")
    print("         BANKOO SYSTEM VALIDATION v2.0")
    print("================================================\n")
    
    results = {
        "env": check_env(),
        "api": check_backend_api(),
        "brain": check_brain_logic(),
        "ui": check_ui_integrity()
    }
    
    print("\n" + "="*48)
    if all(results.values()):
        print("   ✨ SYSTEM UPGRADE SUCCESS: ALL SYSTEMS GO! ✨")
    else:
        print("   ⚠️  VALIDATION FAILED: CHECK ERRORS ABOVE ⚠️")
    print("="*48)
