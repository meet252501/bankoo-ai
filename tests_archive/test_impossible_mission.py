import asyncio
import os
import sys
import logging
import config

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("ImpossibleTest")

# Add path
sys.path.append(os.getcwd())

from vision_agent import VisionAgent
from vision_kernel import VisionKernel

async def test_impossible_mission():
    print("🚀 Starting Zenith v6 IMPOSSIBLE Mission...")
    
    # 1. Setup
    api_key = config.OPENROUTER_API_KEY
    agent = VisionAgent(api_key)
    kernel = VisionKernel(agent)
    
    # 2. Define Goal
    goal = "Open notepad, type 'Zenith v6 is Unstoppable', select all, copy it, and read the clipboard to confirm."
    
    print(f"🎯 Goal: {goal}")
    print("------------------------------------------------")
    
    # 3. Validation Callback
    def update_callback(msg):
        print(f"\n📢 PROGRESS: {msg}\n")
        
    # 4. Run Message Loop
    result = await kernel.run_mission(goal, update_callback=update_callback)
    
    print("------------------------------------------------")
    print(f"🏁 Final Result: {result}")

if __name__ == "__main__":
    try:
        asyncio.run(test_impossible_mission())
    except KeyboardInterrupt:
        print("\n🛑 Test Aborted by User.")
    except Exception as e:
        print(f"\n❌ Test Failed: {e}")
