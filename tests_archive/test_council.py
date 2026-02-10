
import sys
import os

# Simulate Bankoo Environment
sys.path.append(os.getcwd())

try:
    print("--- [COUNCIL TEST START] ---")
    
    # Simulate User Prompt triggering the Council
    user_prompt = "debate: Create a high-performance Python scraper for e-commerce"
    print(f"USER: {user_prompt}")
    
    # Mocking config and requests if needed, but we want to see if it triggers
    from assistant import Intent
    # We can't easily mock the whole assistant here, but we can test ai_council directly
    import ai_council
    
    # Note: This will make real API calls to Groq/OpenRouter if keys are valid
    print("🏛️ Starting Council Debate...")
    result = ai_council.council.debate(user_prompt)
    
    print("-" * 30)
    print(result)
    print("-" * 30)
    
    print("✅ SUCCESS: Council Debate Simulation Completed!")
    print("--- [COUNCIL TEST END] ---")

except Exception as e:
    print(f"❌ ERROR: {e}")
