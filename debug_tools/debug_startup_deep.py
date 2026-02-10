import sys
import os
import traceback

project_path = r"C:\Users\Meet Sutariya\Desktop\final banko.ai"
sys.path.append(project_path)
os.chdir(project_path)

print("🔍 Debugging Runtime Initialization...")

try:
    print("1. Importing Dependencies...")
    import config
    import api_hub
    import bankoo_main
    print("✅ Imports Successful.")

    print("2. Initializing AI Brain (DesktopAssistant)...")
    # This is the heavy lifting step that likely hangs or crashes
    from assistant import DesktopAssistant
    assistant = DesktopAssistant()
    print("✅ AI Brain Initialized Successfully.")

    print("3. Checking Flask App...")
    if bankoo_main.app:
        print("✅ Flask App Object is ready.")
    
except Exception:
    print("\n❌ CRITICAL RUNTIME ERROR:")
    traceback.print_exc()

print("\n🏁 Debug Complete.")
