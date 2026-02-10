
import config
from api_hub import hub
import time

def test_config():
    print("----- CONFIGURATION TEST -----")
    print(f"STT_MODE: {config.STT_MODE}")
    if config.STT_MODE == "online":
        print("✅ STT Config is CORRECT (Online)")
    else:
        print("❌ STT Config is WRONG (Should be 'online')")

    print(f"Gemini Key Present: {'Yes' if config.GEMINI_API_KEY else 'No'}")

def test_vision():
    print("\n----- VISION TEST (Gemini) -----")
    test_url = "https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png"
    print(f"Testing URL: {test_url}")
    
    try:
        result = hub.tag_image(test_url)
        print("\n--- GEMINI RESULT ---")
        print(result)
        
        if "Google" in result or "logo" in result:
             print("\n✅ Vision Test PASSED")
        elif "Error" in result:
             print("\n❌ Vision Test FAILED (Error returned)")
        else:
             print("\n⚠️ Vision Test UNCERTAIN (Check output)")
             
    except Exception as e:
        print(f"\n❌ Vision Test CRASHED: {e}")

if __name__ == "__main__":
    test_config()
    test_vision()
