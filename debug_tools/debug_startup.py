import sys
import os
import traceback

project_path = r"C:\Users\Meet Sutariya\Desktop\final banko.ai"
sys.path.append(project_path)
os.chdir(project_path)

print("🔍 Debugging Startup...")

try:
    print("1. Importing Config...")
    import config
    print("✅ Config Loaded.")

    print("2. Importing API Hub (Backend Integration)...")
    import api_hub
    print("✅ API Hub Loaded.")

    print("3. Importing Bankoo Main...")
    import bankoo_main
    print("✅ Bankoo Main Importable.")

except Exception:
    print("\n❌ CRITICAL ERROR DURING STARTUP:")
    traceback.print_exc()

print("\n🏁 Debug Complete.")
