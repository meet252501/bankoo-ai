import sys
import os
import asyncio
import logging

# Add project root to path
sys.path.append(os.getcwd())

from vision_kernel import VisionKernel
from vision_agent import VisionAgent
import config

async def test_v6_lifecycle():
    print("🧪 Testing Zenith v6 Lifecycle...")
    
    # 1. Initialize
    brain = VisionAgent(config.OPENROUTER_API_KEY)
    kernel = VisionKernel(brain)
    kernel.max_steps = 1 # Keep it short
    
    # 2. Run goal
    print("🚀 Triggering mission...")
    # Using a fake goal that should fail or end quickly
    result = await kernel.run_mission("Diagnostic: Just check screen once.")
    
    print(f"🏁 Result: {result}")
    
    # 3. Check for leftover 'missions' folder
    missions_dir = os.path.join(os.getcwd(), "missions")
    if os.path.exists(missions_dir):
        children = os.listdir(missions_dir)
        if not children:
            print("✅ SUCCESS: Missions folder is empty.")
        else:
            print(f"⚠️ WARNING: Cleanup failed. Leftover: {children}")
    else:
        print("✅ SUCCESS: Missions folder removed or never created.")

if __name__ == "__main__":
    asyncio.run(test_v6_lifecycle())
