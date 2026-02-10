
import os
import sys

print("🔍 [DEBUG] Starting AI Diagnostics...")

try:
    import config
    print(f"✅ [DEBUG] Config Loaded.")
    print(f"   - OpenRouter Key Present: {bool(getattr(config, 'OPENROUTER_API_KEY', None))}")
    print(f"   - Groq Key Present: {bool(getattr(config, 'GROQ_API_KEY', None))}")
except Exception as e:
    print(f"❌ [DEBUG] Config Import Failed: {e}")

try:
    import assistant
    print(f"✅ [DEBUG] Assistant Module Imported.")
except Exception as e:
    print(f"❌ [DEBUG] Assistant Import Failed: {e}")

print("🔍 [DEBUG] Initializing DesktopAssistant...")
try:
    bot = assistant.DesktopAssistant()
    print(f"✅ [DEBUG] DesktopAssistant Initialized.")
    print(f"   - Client Status: {bot.client}")
    print(f"   - Provider: {bot.provider}")
    
    if bot.client is None:
        print("❌ [DEBUG] Client is NONE. Printing _init_ai logic trace:")
        # Attempt manual init to catch errors
        try:
            from openai import OpenAI
            print("   - OpenAI Module: Installed")
        except ImportError:
            print("   - OpenAI Module: MISSING (This is the cause!)")
            
        print("   - Attempting manual connection to OpenRouter...")
        try:
            client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=config.OPENROUTER_API_KEY,
            )
            print("   - Manual Connection: SUCCESS")
        except Exception as e:
            print(f"   - Manual Connection FAILED: {e}")

except Exception as e:
    print(f"❌ [DEBUG] Assistant Crash: {e}")

input("\nPres Enter to exit...")
