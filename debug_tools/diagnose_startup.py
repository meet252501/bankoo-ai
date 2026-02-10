"""
Bankoo Startup Diagnostic Tool
Checks all dependencies and identifies startup blockers.
"""
import sys
import os
import shutil

print("🔍 BANKOO STARTUP DIAGNOSTIC")
print("=" * 50)

# Show Python Installation Info
print(f"\n🐍 Python Context:")
print(f"   Executable: {sys.executable}")
print(f"   Version: {sys.version.split()[0]}")
print(f"   CWD: {os.getcwd()}")

# Test 1: Core Dependencies
print("\n1️⃣ Checking Dependencies...")
dependencies = {
    "pandas": "Data Processing",
    "yfinance": "Finance APIs",
    "requests": "HTTP Client",
    "PyPDF2": "PDF Processing", 
    "langchain_community": "RAG Engine",
    "civitai": "Image Generation"
}

# Pre-inject Civitai Key for Diagnostic to prevent crash
try:
    import config
    if hasattr(config, "CIVITAI_API_TOKEN"):
        os.environ["CIVITAI_API_TOKEN"] = config.CIVITAI_API_TOKEN
except:
    pass

missing = []
for module, purpose in dependencies.items():
    try:
        __import__(module)
        print(f"   ✅ {module:<20} - OK")
    except ImportError:
        print(f"   ❌ {module:<20} - MISSING ({purpose})")
        missing.append(module)

# Test 2: Internal Modules
print("\n2️⃣ Testing Internal Modules...")
for mod in ['api_hub', 'assistant', 'config']:
    try:
        __import__(mod)
        print(f"   ✅ {mod:<20} - OK")
    except Exception as e:
        print(f"   ❌ {mod:<20} - FAILED: {e}")

# Summary
print("\n" + "=" * 50)
if missing:
    print("❌ MISSING DEPENDENCIES FOUND")
    print(f"\nRun this command to fix it:")
    print(f'"{sys.executable}" -m pip install {" ".join(missing)}')
else:
    print("✅ SYSTEM READY")
    print("\nYou can now run: START_BANKOO.bat")

print("\nPress Enter to exit...")
if sys.platform == 'win32':
    input()
