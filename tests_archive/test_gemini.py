import config
import google.generativeai as genai
import sys

print("--- ZENITH GEMINI DIAGNOSTIC ---")
print(f"API Key Present: {bool(config.GEMINI_API_KEY)}")

try:
    genai.configure(api_key=config.GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-2.0-flash-exp")
    
    print("Attempting to connect to Google Gemini 2.0 Flash...")
    response = model.generate_content("Hello! Are you online? Reply with exact code: 'SYSTEM_ONLINE'")
    
    print(f"Response Received: {response.text}")
    
    if "SYSTEM_ONLINE" in response.text:
        print("✅ SUCCESS: Gemini is active and responding.")
    else:
        print("⚠️ WARNING: Response received but content mismatched.")

except Exception as e:
    print(f"❌ ERROR: {e}")
    print("Hint: You may need to run 'pip install google-generativeai'")
