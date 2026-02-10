import os
import time
import json
from agent_logger import trace_logger

def simulate_loop():
    print("🚀 [ZENITH SIMULATION] Starting Learning Cycle Demo...")
    time.sleep(1)

    # STEP 1: INITIAL STATE (The Error)
    print("\n--- STEP 1: THE logic GAP ---")
    user_query = "What is 2+2? Answer in Gujarati only."
    dumb_prompt = "You are a helpful assistant." # Missing the "Answer in Gujarati" enforcement
    ai_response = "2+2 is 4." # FAILED (Answered in English)
    
    print(f"USER: {user_query}")
    print(f"AI (Dumb): {ai_response}")
    print("❌ ERROR: AI ignored the language constraint.")

    # STEP 2: LOGGING THE FAILURE
    print("\n--- STEP 2: LOGGING TO TRACES ---")
    trace_logger.log_interaction(
        user_input=user_query,
        system_prompt=dumb_prompt,
        assistant_response=ai_response,
        reward=-1.0, # Negative reward flags this for the optimizer
        lang='english'
    )
    print("💾 Interaction saved with -1.0 Reward (Flagged for Optimization).")

    # STEP 3: THE FIX (Simulated APO)
    print("\n--- STEP 3: AGENT-LIGHTNING OPTIMIZATION ---")
    print("🔍 Analyzing traces...")
    time.sleep(2)
    print("🧠 [APO] Suggesting Prompt Modification: Added 'Target Language Enforcement'")
    
    optimized_prompt = "You are a helpful assistant. If the user specifies a language (like Gujarati), you MUST respond in that language only."
    
    # STEP 4: VERIFICATION
    print("\n--- STEP 4: PERMANENT KNOWLEDGE ---")
    print(f"RE-RUNNING QUERY: {user_query}")
    ai_response_fixed = "૨+૨ = ૪ (બે અને બે ચાર થાય છે)." # SUCCESS
    
    print(f"AI (Optimized): {ai_response_fixed}")
    print("✅ SUCCESS: AI correctly followed the new learned behavioral rule.")

    # STEP 5: FINAL LOG
    trace_logger.log_interaction(
        user_input=user_query,
        system_prompt=optimized_prompt,
        assistant_response=ai_response_fixed,
        reward=1.0, # Positive reward!
        lang='gujarati'
    )
    
    print("\n========================================")
    print("🟢 SIMULATION COMPLETE")
    print("Agent-Lightning has successfully turned a failure into a skill.")
    print("Check your 'Zenith Brain' in the Bankoo App Drawer to see the Reward Trend!")
    print("========================================\n")

if __name__ == "__main__":
    simulate_loop()
