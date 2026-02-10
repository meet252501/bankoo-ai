import asyncio
import os
import sys
from unittest.mock import MagicMock

# Setup paths
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Mock Config before import
import config
config.TELEGRAM_BOT_TOKEN = "TEST_TOKEN"
config.GROQ_API_KEY = "TEST_KEY"
config.AUTHORIZED_USER_IDS = [12345]

from bankoo_bridge import MoltbotAgent
from skill_manager import skill_manager

async def run_test():
    print("🧪 **STARTING SKILL SYSTEM DIAGNOSTIC**")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    # 1. Verify Skill Loading
    print("\n🔍 **Step 1: Checking Skill Manager**")
    skill_manager.load_markdown_skills(os.path.join(os.path.dirname(__file__), "moltbot_skills"))
    
    skills_dict = skill_manager.list_skills()
    flat_skills = []
    
    print(f"\n📊 **Step 1.1: Verifying Categories (Deep)**")
    # Check if we have the dictionary structure
    if isinstance(skills_dict, dict):
        categories = list(skills_dict.keys())
        print(f"   📂 Found {len(categories)} categories.")
        print(f"   📝 Sample Categories: {categories[:5]}")
        
        # Verify specific categorization logic
        # 'bankoo' skill should be in 'bankoo' category or 'Core' depending on path
        # Let's see where it ended up
        bankoo_cat = "Unknown"
        for cat, s_list in skills_dict.items():
            for s in s_list:
                flat_skills.append(s['name'])
                if s['name'] == 'bankoo':
                    bankoo_cat = cat
        print(f"   🎯 Skill 'bankoo' is in category: '{bankoo_cat}'")
    else:
        print("   ❌ FAIL: list_skills() returned list, expected categorized dict.")
        flat_skills = [s['name'] for s in skills_dict]

    print(f"   📂 Total Loaded Skills: {len(flat_skills)}")
    if 'bankoo' in flat_skills:
        print("   ✅ Skill 'bankoo' found in library.")
        found_bankoo = True
    else:
        print("   ❌ Skill 'bankoo' NOT found.")
        return

    # 2. Verify Agent Logic (Mocked Brain)
    print("\n🧠 **Step 2: Simulating Brain Interaction (Deep)**")
    agent = MoltbotAgent()
    
    # Mock Groq Client to simulate LLM behavior
    mock_groq = MagicMock()
    
    # Scenario:
    # First call -> LLM requests skill
    # Second call -> System injects manual -> LLM confirms
    
    response_1 = MagicMock()
    response_1.choices[0].message.content = "[SKILL_REQUEST: bankoo]"
    
    response_2 = MagicMock()
    response_2.choices[0].message.content = "EXECUTE_COMMAND: python bankoo_skill.py"
    
    mock_groq.chat.completions.create.side_effect = [response_1, response_2]
    agent.groq_client = mock_groq
    
    print("   👤 User: 'Connect to Bankoo main brain please'")
    reply, media, mtype = await agent.chat_with_brain("Connect to Bankoo main brain please", "TestUser")
    
    print(f"   🤖 Final Agent Reply: {reply}")
    
    # Deep Inspection of the Mock CallArgs
    print("\n🔍 **Step 3: Verifying Prompt Injection**")
    # We expect 2 calls. 
    # Call 1: Standard Prompt
    # Call 2: Prompt + [SYSTEM INJECTED KNOWLEDGE ...]
    
    calls = mock_groq.chat.completions.create.call_args_list
    if len(calls) == 2:
        print("   ✅ Chain executed (2 LLM calls detected).")
        
        # Inspect the arguments of the SECOND call (index 1)
        # call_args is (args, kwargs) -> kwargs['messages'] -> list of dicts -> system prompt
        second_call_kwargs = calls[1].kwargs
        messages = second_call_kwargs['messages']
        system_content = messages[0]['content']
        
        # Check if the SKILL.md content was injected
        # The bankoo skill md contains "Internal Bridge to Bankoo Pro Neural Brain"
        if "Internal Bridge to Bankoo Pro Neural Brain" in system_content or "Bankoo Pro Bridge" in system_content:
             print("   ✅ **SUCCESS: Knowledge Injection Verified.**")
             print("      The system prompt correctly contained the manual from SKILL.md")
        else:
             print("   ❌ **FAIL: Knowledge Injection Missing.**")
             print(f"      System Prompt snippet: {system_content[:200]}...")
    else:
        print(f"   ❌ FAIL: Expected 2 LLM calls, got {len(calls)}.")

if __name__ == "__main__":
    asyncio.run(run_test())
