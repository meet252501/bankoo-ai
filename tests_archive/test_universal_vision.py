import sys
import os
import time
import logging

# Add project root to path
sys.path.append(os.getcwd())

from assistant import DesktopAssistant, Intent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TestVision")

def test_vision_integration():
    print("🚀 [UNIVERSAL VISION TEST: DESKTOP BRAIN]")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    # 1. Initialize the Master Brain
    print("🧠 Initializing DesktopAssistant (Master Brain)...")
    assistant = DesktopAssistant()
    
    # 2. Test intent Routing (Logic Only)
    print("\n🔍 Testing Intent Routing Logic...")
    test_queries = [
        ("Click the search bar", Intent.VISION_CLICK),
        ("Where is the Windows icon?", Intent.VISION_NAV),
        ("Automate opening chrome and searching for Surat", Intent.VISION_AUTO),
        ("લોગિન બટન પર ક્લિક કર", Intent.VISION_CLICK) # Gujarati Click
    ]
    
    for query, expected_intent in test_queries:
        intent = assistant.route_intent(query)
        status = "✅ PASS" if intent == expected_intent else f"❌ FAIL (Got {intent})"
        print(f"   - Query: '{query}' -> Intent: {intent} [{status}]")

    # 3. Execution Test (Vision Navigation - NON-DESTRUCTIVE)
    print("\n👁️ Testing Real Vision Navigation...")
    nav_query = "Find the Windows Start button or any taskbar icon."
    print(f"   Query: {nav_query}")
    
    # We call execute_intent directly to avoid full assistant overhead (LLM chat)
    # This will take a screenshot and use the VisionAgent
    response = assistant.execute_intent(Intent.VISION_NAV, nav_query)
    
    print(f"🏁 Brain Result: {response}")
    
    if "Vision Error" in response:
        print("❌ Real Vision test failed (Check API keys or screen state)")
    else:
        print("✅ Real Vision test succeeded!")

if __name__ == "__main__":
    test_vision_integration()
