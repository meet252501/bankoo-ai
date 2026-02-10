import asyncio
import os
import sys
import logging
import config

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("DeepResearchTest")

# Add path
sys.path.append(os.getcwd())

from vision_agent import VisionAgent
from vision_kernel import VisionKernel

async def test_research_flow():
    print("🚀 Starting Zenith v6 Research Mission...")
    
    # 1. Setup
    api_key = config.OPENROUTER_API_KEY
    if not api_key:
        print("❌ Connect Error: No API Key.")
        return

    agent = VisionAgent(api_key)
    kernel = VisionKernel(agent)
    
    # 2. Define Research Goal
    # This tests:
    # - Spatial Memory ("Open Chrome")
    # - Visual Grid (Clicking search bar)
    # - Smart Wait (Waiting for page load)
    # - Cognitive Reasoning (Reading and Summarizing text from pixels)
    goal = (
        "Open Chrome (or Edge). "
        "Type 'latest breakthrough in AI agents 2025' and press Enter. "
        "Wait for the results to load. "
        "Look at the screen and tell me the titles of the top 3 search results."
    )
    
    print(f"🎯 Research Goal: {goal}")
    print("------------------------------------------------")
    
    # 3. Validation Callback
    def update_callback(msg):
        print(f"\n📢 FEEDBACK: {msg}\n")
        
    # 4. Run Message Loop
    result = await kernel.run_mission(goal, update_callback=update_callback)
    
    print("------------------------------------------------")
    print(f"🏁 Final Result: {result}")

if __name__ == "__main__":
    try:
        asyncio.run(test_research_flow())
    except KeyboardInterrupt:
        print("\n🛑 Test Aborted.")
