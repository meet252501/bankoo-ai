import sys
import os
import traceback

print("🔍 DIAGNOSTIC: Testing Brain Load...")

try:
    print("1. Importing config...")
    import config
    print("   ✅ Config OK")

    print("2. Importing api_hub...")
    import api_hub
    print("   ✅ API Hub OK")

    print("3. Importing assistant...")
    from assistant import DesktopAssistant
    print("   ✅ Assistant Module Imported")

    print("4. Initializing Assistant (Light Mode)...")
    # Determine if we can init
    bot = DesktopAssistant()
    print("   ✅ Assistant Initialized Successfully!")

    print("\n🎉 DIAGNOSIS: BRAIN IS HEALTHY.")

except Exception as e:
    print("\n❌ CRITICAL FAILURE DETECTED!")
    print("-" * 40)
    traceback.print_exc()
    print("-" * 40)
    print(f"Error: {e}")
