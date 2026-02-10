import os
import logging
from crewai import Agent, Task, Crew, Process
from langchain_community.llms import Ollama
import config

logger = logging.getLogger(__name__)

class ZenithCrewEngine:
    """Multi-Agent Orchestrator for local autonomous crews."""
    
    def __init__(self, model=None):
        self.model = model or getattr(config, 'OLLAMA_MODEL', 'llama3.2:3b')
        self.base_url = getattr(config, 'OLLAMA_BASE_URL', 'http://localhost:11434')
        self.llm = None
        
        # Initialize Local LLM
        try:
            from langchain_community.llms import Ollama
            self.llm = Ollama(model=self.model, base_url=self.base_url)
            logger.info(f"🧬 [CREW] Core connected to local Ollama ({self.model})")
        except Exception as e:
            logger.error(f"❌ [CREW] Connection failed: {e}")

    def create_simple_crew(self, task_description, agent_role="General Specialist"):
        """Spawn a quick single-agent crew for a local task."""
        if not self.llm:
            return "Error: Local LLM not initialized. Please ensure Ollama is installed and running."

        try:
            # Lazy Import of heavy CrewAI libs to prevent startup panic
            from crewai import Agent, Task, Crew, Process
            
            # 1. Define Agent
            expert = Agent(
                role=agent_role,
                goal=f'Complete the following task accurately: {task_description}',
                backstory=f'You are a high-performance sub-agent of Bankoo Zenith, running locally for maximum privacy.',
                llm=self.llm,
                allow_delegation=False,
                verbose=True
            )

            # 2. Define Task
            task = Task(
                description=task_description,
                agent=expert,
                expected_output="A detailed and helpful response based on the task."
            )

            # 3. Form and Execute Crew
            crew = Crew(
                agents=[expert],
                tasks=[task],
                process=Process.sequential
            )

            logger.info(f"🚀 [CREW] Launching local mission: {task_description[:50]}...")
            result = crew.kickoff()
            return result
        except Exception as e:
            logger.error(f"❌ [CREW] Crew Execution Failed: {e}")
            return f"Local Crew Error: {str(e)}. This is likely a dependency issue (chromadb/rust) on your system."

# --- SKILL HUB INTEGRATION ---
def run_local_task(task_desc):
    """Bridge for api_hub to trigger local crews."""
    engine = ZenithCrewEngine()
    return engine.create_simple_crew(task_desc)
