import sys
import os
import asyncio
import logging

# Add project root to path
PROJECT_ROOT = r"C:\Users\Meet Sutariya\Desktop\final banko.ai"
sys.path.append(PROJECT_ROOT)
os.chdir(PROJECT_ROOT)

from vision_kernel import VisionKernel
from vision_agent import VisionAgent
import config

# Configure logging to see the thoughts
logging.basicConfig(level=logging.INFO)

async def run_complex_task():
    print("🚀 [MISSION: ZENITH v7 COMPLEX GAUNTLET]")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    # 1. Initialize (Dual-Engine)
    brain = VisionAgent(
        primary_key=config.GEMINI_API_KEY,
        backup_key=getattr(config, 'OPENROUTER_API_KEY', None)
    )
    kernel = VisionKernel(brain)
    
    # 2. Define Goal
    goal = "Open the Calculator app, type '123 + 456 =', then wait 2 seconds."
    
    print(f"🎯 Goal: {goal}")
    
    # 3. Define Callback to show live progress
    def status_callback(msg):
        print(f"\n📡 [GHOST THOUGHT]:\n{msg}\n")

    # 4. Execute
    print("🎬 Starting Autonomous Loop...")
    result = await kernel.run_mission(goal, update_callback=status_callback)
    
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"🏁 FINAL MISSION STATUS: {result}")

if __name__ == "__main__":
    asyncio.run(run_complex_task())
