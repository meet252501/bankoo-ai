import sys
import os
import pyautogui
import json

# Add current directory to path
sys.path.append(os.getcwd())

from vision_agent import VisionAgent
import config

def run_scenario():
    print("🚀 [SCENARIO: MISSION NEURAL VISION]")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    # 1. Initialize
    print("🧠 Initializing Specialized Vision Brain...")
    brain = VisionAgent(config.GROQ_API_KEY)
    
    # 2. Capture
    print("📸 Capturing Screen State...")
    temp_path = "test_scenario_screen.jpg"
    screenshot = pyautogui.screenshot()
    screenshot.save(temp_path)
    
    # 3. Analyze
    # Let's try to find something universal like the "Start" button or any visible icon/text.
    goal = "Find the Windows Start button or any application icon on the taskbar."
    print(f"🎯 Goal: {goal}")
    print("⚙️ Analyzing... (VLM Consultation)")
    
    try:
        result = brain.analyze_screen(temp_path, goal)
        
        print("\n🏁 [BRAIN RESPONSE]")
        if "error" in result:
            print(f"❌ Error: {result['error']}")
        else:
            print(f"✅ Target: {result.get('description', 'Unknown')}")
            print(f"📍 Coordinates: ({result.get('x')}, {result.get('y')})")
            print(f"📊 JSON: {json.dumps(result)}")
            
            # 4. Optional: Simulation of Move (No Click for Safety)
            print("\n🛠️ Action Simulation:")
            print(f"   - Moving mouse to ({result.get('x')}, {result.get('y')}) slowly...")
            # We move it slowly so the user can see.
            pyautogui.moveTo(result.get('x'), result.get('y'), duration=2.0)
            print("   - [Simulated Click] (Not actually clicking for safety)")
            
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
    finally:
        # Cleanup
        if os.path.exists(temp_path):
            os.remove(temp_path)

if __name__ == "__main__":
    run_scenario()
