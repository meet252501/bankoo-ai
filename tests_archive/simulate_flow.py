
import sys
import os

# Simulate Bankoo Environment
sys.path.append(os.getcwd())

try:
    print("--- [SIMULATION START] ---")
    
    # 1. Simulate User Prompt
    user_prompt = "Create a calculator in Python"
    print(f"USER: {user_prompt}")
    
    # 2. Simulate AI Processing (Assistant)
    import code_templates
    lang = "python"
    print("AI: Detecting intent... [CREATE_GUI]")
    print(f"AI: Generating {lang} code...")
    
    code, source = code_templates.generate_code(user_prompt, lang)
    
    if "tkinter" in code:
        print("✅ SUCCESS: GUI Code Generated!")
        print(f"Source: {source}")
        print("-" * 20)
        print(code[:100] + "...\n[...rest of code...]")
        print("-" * 20)
    else:
        print("❌ FAILED: Code generation error")
        
    print("--- [SIMULATION END] ---")

except ImportError as e:
    print(f"❌ ERROR: Could not import modules: {e}")
except Exception as e:
    print(f"❌ ERROR: {e}")
