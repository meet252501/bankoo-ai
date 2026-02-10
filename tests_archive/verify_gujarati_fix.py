
import sys
import os

# Add project path to sys.path
sys.path.append(r"c:\Users\Meet Sutariya\Desktop\final banko.ai")

from assistant import DesktopAssistant
import config

def test_routing():
    print("--- Bankoo Routing Test ---")
    assistant = DesktopAssistant()
    
    # Test cases: Short Gujarati text
    test_texts = [
        "કેમ છો?", 
        "શું ચાલે છે?",
        "How are you?"
    ]
    
    print(f"Primary Model: {config.PRIMARY_MODEL}")
    print(f"Fast Model: {config.FAST_MODEL}")
    
    for text in test_texts:
        normalized, lang = assistant.normalize_input(text)
        intent = assistant.route_intent(normalized)
        
        # Simulate the model routing logic
        target_model_id = config.PRIMARY_MODEL
        if (intent == assistant.Intent.SMALL_TALK or len(normalized) < 30) and lang not in ['gujarati', 'hindi']:
            target_model_id = getattr(config, 'FAST_MODEL', config.PRIMARY_MODEL)
            
        print(f"Input: '{text}' | Lang: {lang} | Intent: {intent} | Routed Model: {target_model_id}")
        
        if lang == 'gujarati' and target_model_id == config.PRIMARY_MODEL:
            print("  ✅ SUCCESS: Gujarati routed to Primary Model.")
        elif lang == 'english' and target_model_id == config.FAST_MODEL:
            print("  ✅ SUCCESS: English Small Talk routed to Fast Model.")
        else:
            print("  ❌ FAILURE in routing logic.")

if __name__ == "__main__":
    test_routing()
