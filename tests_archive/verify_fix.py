import sys
import os

# Add project dir to path
sys.path.append(r"C:\Users\Meet Sutariya\Desktop\final banko.ai")

import config
from assistant import DesktopAssistant

def test_routing():
    print("Testing Model Routing Logic...")
    assistant = DesktopAssistant()
    
    # Mocking config models to test routing
    models_to_test = [
        config.PRIMARY_MODEL,
        config.CODING_MODEL,
        config.REASONING_MODEL,
        "groq/llama-3.3-70b-versatile",
        "cerebras/llama-3.3-70b",
        "fireworks/llama-v3-70b"
    ]
    
    for m in models_to_test:
        client, resolved_model = assistant._get_brain_client(m)
        print(f"Original: {m} -> Resolved: {resolved_model}")
        
        # Verify prefix stripping
        if "/" in m and m.split("/")[0] in ["groq", "cerebras", "fireworks"]:
            expected = m.split("/")[-1]
            if resolved_model != expected:
                print(f"  ❌ FAILED: Expected {expected}, got {resolved_model}")
            else:
                print(f"  ✅ SUCCESS")
        else:
            print(f"  ℹ️ Default routing for {m}")

if __name__ == "__main__":
    test_routing()
