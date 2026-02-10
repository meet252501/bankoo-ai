import os
import sys
import google.generativeai as genai
from PIL import Image
import pyautogui

# Add project root
sys.path.append(os.getcwd())
import config

def test_native_gemini():
    print("🚀 Testing Native Gemini Vision...")
    
    if not hasattr(config, 'GEMINI_API_KEY'):
        print("❌ No GEMINI_API_KEY")
        return

    genai.configure(api_key=config.GEMINI_API_KEY)
    
    # List models to ensure we pick a vision one
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods and 'gemini' in m.name:
            print(f"Found Model: {m.name}")

    model = genai.GenerativeModel('gemini-2.0-flash-exp') # Or flash
    
    print("📸 Snap...")
    pyautogui.screenshot("test_native.jpg")
    
    try:
        with Image.open("test_native.jpg") as img:
            print("🧠 Sending to Brain...")
            response = model.generate_content(["Describe this image briefly.", img])
            print("✅ Response:", response.text)
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if os.path.exists("test_native.jpg"):
            os.remove("test_native.jpg")

if __name__ == "__main__":
    test_native_gemini()
