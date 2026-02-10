import os
import sys
import logging
import pyautogui
import json
import time

# Setup basic logging to see the internal agent logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("TestVision")

# Add project root to path
sys.path.append(os.getcwd())

from vision_agent import VisionAgent
import config

def test_vision():
    print("🚀 Initializing Vision Agent...")
    # Ensure API Key is loaded
    api_key = config.OPENROUTER_API_KEY
    if not api_key:
        print("❌ Error: OPENROUTER_API_KEY not found in config.py")
        return

    agent = VisionAgent(api_key)
    
    print("📸 Capturing Screenshot...")
    screenshot_path = "test_vision_snap.jpg"
    pyautogui.screenshot(screenshot_path)
    
    goal = "Find the Windows Start button or icon"
    print(f"🧠 Asking Brain (UI-Tars) to: '{goal}'")
    
    start_time = time.time()
    try:
        result = agent.analyze_screen(screenshot_path, goal)
        duration = time.time() - start_time
        
        print("\n" + "="*40)
        print(f"⏱️ Time Taken: {duration:.2f}s")
        print(f"🎯 Result: {json.dumps(result, indent=2)}")
        print("="*40 + "\n")
        
        if "error" in result:
             print("❌ Test Failed: Model returned error.")
        else:
             print("✅ Test Passed: Coordinates received.")
             
    except Exception as e:
        print(f"❌ Critical Error: {e}")
    finally:
        # Cleanup
        if os.path.exists(screenshot_path):
            os.remove(screenshot_path)

if __name__ == "__main__":
    test_vision()
