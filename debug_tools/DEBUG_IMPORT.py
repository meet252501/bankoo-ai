import sys
import traceback

print("🔍 Testing bankoo_main import...")
try:
    import bankoo_main
    print("✅ Import SUCCESS")
except Exception:
    print("❌ Import FAILED")
    traceback.print_exc()
