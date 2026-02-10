import os
import sys
import logging

# Setup logging to stdout
logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger("Debug")

import config
from vision_agent import VisionAgent

def debug_native():
    print("🐞 Debugging VisionAgent Fallback...")
    agent = VisionAgent(config.OPENROUTER_API_KEY)
    
    # We need a fake image path
    with open("dummy.jpg", "wb") as f:
        f.write(b"fake image data")
        
    try:
        # This will fail on OpenRouter (402) and trigger fallbacks
        result = agent.analyze_screen("dummy.jpg", "find start button")
        print("\n✅ Result:", result)
    except Exception as e:
        print("\n❌ Script Error:", e)
    finally:
        if os.path.exists("dummy.jpg"):
            os.remove("dummy.jpg")

if __name__ == "__main__":
    debug_native()
