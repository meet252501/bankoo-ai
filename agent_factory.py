import json
import os
import logging
import re
from assistant import DesktopAssistant
from api_hub import skill_hub

logger = logging.getLogger(__name__)

class AgentFactory:
    """The Mother-Ship brain for spawning specialized sub-agents."""
    
    def __init__(self, agent_dir="brain/agents"):
        self.agent_dir = agent_dir
        self.schema_path = os.path.join(agent_dir, "schema.json")
        self.assistant = DesktopAssistant()
        
        # Ensure directories exist
        if not os.path.exists(self.agent_dir):
            os.makedirs(self.agent_dir)

    async def spawn_agent(self, user_prompt):
        """
        Translates a user request into a structured Agent Blueprint.
        Returns (blueprint_dict, error_msg)
        """
        logger.info(f"🧬 [FACTORY] Receiving birth request: {user_prompt}")
        
        available_skills = skill_hub.list_skills()
        
        meta_prompt = f"""
        You are the Zenith Meta-Brain Agent Spawner. 
        Your task is to design a specialized AI sub-agent based on the user's requirement.
        
        REQUIRMENT: "{user_prompt}"
        
        AVAILABLE TOOLS (Choose only from these):
        {json.dumps(available_skills, indent=2)}
        
        SPECIAL INSTRUCTIONS:
        1. If the user mentions "local", "privacy", or "offline", ensure the 'local_crew' skill is included.
        2. If the agent requires a DESKTOP APPLICATION (e.g., Spotify, Chrome, Discord, VS Code, Notepad):
           - Include app-launch logic in the system_prompt
           - Add the app name to the 'required_apps' field (lowercase)
           - Format the system_prompt with these steps:
             STEP 1: "Check if <app> is running using process detection"
             STEP 2: "If not running, the system will auto-launch it"
             STEP 3: "Wait for app initialization (3-5 seconds)"
             STEP 4: "Proceed with main task"
        3. If the tool typically requires an API Key (e.g. Spotify Search, Weather, Cloud Services):
           - In the system_prompt, add: "If the user requests advanced features (e.g. searching specific songs), check for API keys. If missing, tell the user: 'I need API keys for that. Please use /setkey KEY_NAME value'."
        
        You must output a VALID JSON object adhering to this schema:
        - name: unique lowercase string (e.g. 'spotify_controller')
        - display_name: friendly title (e.g. 'Spotify Controller')
        - role: brief description of purpose
        - system_prompt: detailed persona, instructions, and constraints (include app-launch steps if needed)
        - tools: list of strings (Choose from the AVAILABLE TOOLS list above)
        - trigger_keywords: list of words that should activate this agent
        - required_apps: list of app names (lowercase) that must be running (e.g., ["spotify", "chrome"])
        
        JSON ONLY. NO EXPLANATION.
        """
        
        try:
            # Use the high-reasoning brain (get_ai_response bypasses tool routing)
            raw_reply = self.assistant.get_ai_response(meta_prompt)
            logger.info(f"🧬 [FACTORY] Raw LLM Reply: {raw_reply[:500]}...")
            
            # Extract JSON from potential markdown blocks
            json_match = re.search(r'\{.*\}', raw_reply, re.DOTALL)
            if not json_match:
                return None, "Factory failed to produce a structured blueprint."
            
            blueprint = json.loads(json_match.group())
            
            # Validation (Simple check against required fields)
            required = ["name", "display_name", "system_prompt"]
            for field in required:
                if field not in blueprint:
                    return None, f"Incomplete blueprint: Missing {field}"
            
            # Persist
            filename = f"{blueprint['name']}.json"
            save_path = os.path.join(self.agent_dir, filename)
            with open(save_path, 'w') as f:
                json.dump(blueprint, f, indent=4)
                
            logger.info(f"✨ [FACTORY] Agent '{blueprint['display_name']}' has been born.")
            return blueprint, None
            
        except Exception as e:
            logger.error(f"❌ [FACTORY] Birth Complications: {e}")
            return None, str(e)

    def list_agents(self):
        """Return a list of all instantiated blueprints."""
        agents = []
        for file in os.listdir(self.agent_dir):
            if file.endswith(".json") and file != "schema.json":
                try:
                    with open(os.path.join(self.agent_dir, file), 'r') as f:
                        agents.append(json.load(f))
                except:
                    pass
        return agents

if __name__ == "__main__":
    # Internal Unit Test (Sync wrapper if needed, but intended for async)
    import asyncio
    factory = AgentFactory()
    async def test():
        bp, err = await factory.spawn_agent("open spotify and play my recent playlist")
        if bp:
            print(f"Born: {bp['display_name']}")
            print(f"Required Apps: {bp.get('required_apps', 'None')}")
            if 'required_apps' in bp and 'spotify' in bp['required_apps']:
                print("✅ AUTO-LAUNCH TEST: PASS - required_apps field detected")
            else:
                print("⚠️ AUTO-LAUNCH TEST: FAIL - required_apps missing")
        else:
            print(f"Error: {err}")
    
    # asyncio.run(test()) # Uncomment to test
