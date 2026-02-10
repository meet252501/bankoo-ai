import asyncio
import os
import json
import sys

# Ensure we can import local modules
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_dir)

from agent_factory import AgentFactory
from api_hub import skill_hub

async def test_agent_spawner():
    print("🧬 [TEST] Initializing Zenith v16 System Test...")
    factory = AgentFactory()
    
    # 1. Test Skill Hub
    print("\n⚙️ [TEST] Checking Skill Hub Registry...")
    skills = skill_hub.list_skills()
    print(f"✅ Found {len(skills)} skills: {[s['skill'] for s in skills]}")
    
    # 2. Test Spawning (The "Birth" Event)
    test_prompt = "Create a stock market news agent that focuses on tech stocks and dividends."
    print(f"\n✨ [TEST] Spawning agent with prompt: '{test_prompt}'...")
    
    blueprint, error = await factory.spawn_agent(test_prompt)
    
    if error:
        print(f"❌ [TEST] Factory Error: {error}")
        return

    print(f"✅ [TEST] Agent Born: {blueprint['display_name']} ({blueprint['name']})")
    print(f"🎭 [TEST] Role: {blueprint['role']}")
    print(f"🛠️ [TEST] Tools Assigned: {blueprint['tools']}")
    
    # 3. Verify Persistence
    save_path = f"brain/agents/{blueprint['name']}.json"
    if os.path.exists(save_path):
        print(f"📂 [TEST] Persistence Verified: {save_path} exists.")
    else:
        print("❌ [TEST] Persistence Failed: JSON file not found.")
        
    # 4. Simulate a Persona Query
    print(f"\n🧠 [TEST] Simulating a consultation with {blueprint['name']}...")
    context_prompt = f"### AGENT INSTRUCTIONS: {blueprint['system_prompt']}\n\nUSER REQUEST: What is the current trend for Nvidia?"
    
    from assistant import DesktopAssistant
    assistant = DesktopAssistant()
    
    # Note: This might make a real API call if keys are present
    try:
        reply = assistant.ask_ai(context_prompt)
        print(f"💬 [TEST] Agent Response Preview: {reply[:100]}...")
        print("✅ [TEST] Brain Routing Success.")
    except Exception as e:
        print(f"⚠️ [TEST] Brain call failed (Expected if offline/no keys): {e}")

if __name__ == "__main__":
    asyncio.run(test_agent_spawner())
