"""
OWL Brain - CAMEL-AI Multi-Agent Integration for Bankoo
Uses hybrid model strategy for optimal performance.
"""
import os
import sys
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

# Model Configuration (Hybrid Strategy)
OWL_MODEL_CONFIG = {
    "user_agent": "groq/llama-3.3-70b-versatile",      # Planning (Fast)
    "assistant_agent": "deepseek/deepseek-chat",       # Execution (Smart)
    "browsing_agent": "google/gemini-2.0-flash-exp",   # Vision (Multimodal)
    "planning_agent": "groq/llama-3.3-70b-versatile",  # Quick decisions
}

class OWLBrain:
    """
    Lightweight OWL integration for Bankoo AI.
    Orchestrates multi-agent task execution using CAMEL framework.
    """
    
    def __init__(self):
        self.enabled = False
        self.camel_available = False
        self._check_dependencies()
    
    def _check_dependencies(self):
        """Check if CAMEL framework is available."""
        try:
            # Add OWL path to sys.path
            owl_path = os.path.join(
                os.path.dirname(__file__), 
                "resources", "external_research", "owl"
            )
            if os.path.exists(owl_path) and owl_path not in sys.path:
                sys.path.insert(0, owl_path)
            
            # Try importing CAMEL
            from camel.models import ModelFactory
            from camel.societies import RolePlaying
            
            # Set up API keys from config
            self._setup_api_keys()
            
            self.camel_available = True
            self.enabled = True
            logger.info("✅ OWL Brain initialized successfully")
        except ImportError as e:
            logger.warning(f"⚠️ CAMEL not available: {e}")
            logger.info("OWL features disabled. Install with: pip install camel-ai")
            self.enabled = False
    
    def _setup_api_keys(self):
        """Set up API keys from config.py as environment variables."""
        try:
            # Import config to get API keys
            parent_dir = os.path.dirname(os.path.dirname(__file__))
            if parent_dir not in sys.path:
                sys.path.insert(0, parent_dir)
            
            import config
            
            # Map Groq API key to OPENAI_API_KEY for CAMEL compatibility
            # CAMEL uses OpenAI-compatible endpoints for Groq
            if hasattr(config, 'GROQ_API_KEY') and config.GROQ_API_KEY:
                os.environ['OPENAI_API_KEY'] = config.GROQ_API_KEY
                os.environ['GROQ_API_KEY'] = config.GROQ_API_KEY
                logger.info("✅ Groq API key configured for OWL")
            
            # Set DeepSeek/OpenRouter key
            if hasattr(config, 'OPENROUTER_API_KEY') and config.OPENROUTER_API_KEY:
                os.environ['OPENROUTER_API_KEY'] = config.OPENROUTER_API_KEY
                logger.info("✅ OpenRouter API key configured for OWL")
            
            # Set Gemini key
            if hasattr(config, 'GEMINI_API_KEY') and config.GEMINI_API_KEY:
                os.environ['GEMINI_API_KEY'] = config.GEMINI_API_KEY
                logger.info("✅ Gemini API key configured for OWL")
                
        except Exception as e:
            logger.warning(f"Could not load API keys from config: {e}")
    
    def execute_task(
        self, 
        task: str, 
        model_override: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Execute a complex task using multi-agent collaboration.
        
        Args:
            task: The task description
            model_override: Optional model to use instead of defaults
        
        Returns:
            Dict with 'answer', 'steps', and 'tokens_used'
        """
        if not self.enabled:
            return {
                "answer": "OWL multi-agent mode is not available. Please install CAMEL framework.",
                "steps": [],
                "tokens_used": 0,
                "error": "CAMEL not installed"
            }
        
        try:
            from camel.models import ModelFactory
            from camel.societies import RolePlaying
            from camel.toolkits import SearchToolkit, CodeExecutionToolkit
            from camel.types import ModelPlatformType, ModelType
            
            # Create models using hybrid strategy
            models = self._create_models(model_override)
            
            # Configure minimal toolkits (no browser for now to avoid Playwright dependency)
            tools = [
                SearchToolkit().search_duckduckgo,
                SearchToolkit().search_wiki,
                *CodeExecutionToolkit(sandbox="subprocess", verbose=False).get_tools(),
            ]
            
            # Configure agents
            user_agent_kwargs = {"model": models["user"]}
            assistant_agent_kwargs = {"model": models["assistant"], "tools": tools}
            
            # Create society
            society = RolePlaying(
                task_prompt=task,
                with_task_specify=False,
                user_role_name="planner",
                user_agent_kwargs=user_agent_kwargs,
                assistant_role_name="executor",
                assistant_agent_kwargs=assistant_agent_kwargs,
            )
            
            # Execute with limited iterations
            max_iterations = 10
            chat_history = []
            
            for i in range(max_iterations):
                user_msg = society.step()
                if user_msg.terminated:
                    break
                chat_history.append({"role": "user", "content": user_msg.content})
                
                assistant_msg = society.step()
                if assistant_msg.terminated:
                    break
                chat_history.append({"role": "assistant", "content": assistant_msg.content})
            
            # Extract final answer
            final_answer = chat_history[-1]["content"] if chat_history else "No answer generated"
            
            return {
                "answer": final_answer,
                "steps": chat_history,
                "tokens_used": len(str(chat_history)) // 4,  # Rough estimate
                "iterations": len(chat_history) // 2
            }
            
        except Exception as e:
            logger.error(f"OWL execution error: {e}")
            return {
                "answer": f"Multi-agent execution failed: {str(e)}",
                "steps": [],
                "tokens_used": 0,
                "error": str(e)
            }
    
    def _create_models(self, override: Optional[str] = None):
        """Create model instances using hybrid strategy."""
        from camel.models import ModelFactory
        from camel.types import ModelPlatformType, ModelType
        
        if override:
            # Use override for all agents
            model = self._parse_model_string(override)
            return {
                "user": model,
                "assistant": model,
                "browsing": model,
                "planning": model,
            }
        
        # Hybrid strategy
        return {
            "user": self._parse_model_string(OWL_MODEL_CONFIG["user_agent"]),
            "assistant": self._parse_model_string(OWL_MODEL_CONFIG["assistant_agent"]),
            "browsing": self._parse_model_string(OWL_MODEL_CONFIG["browsing_agent"]),
            "planning": self._parse_model_string(OWL_MODEL_CONFIG["planning_agent"]),
        }
    
    def _parse_model_string(self, model_str: str):
        """Parse model string like 'groq/llama-3.3-70b-versatile' into CAMEL model."""
        from camel.models import ModelFactory
        from camel.types import ModelPlatformType, ModelType
        
        # Map provider to CAMEL platform
        provider_map = {
            "groq": ModelPlatformType.OPENAI,  # Groq uses OpenAI-compatible API
            "deepseek": ModelPlatformType.OPENAI,  # DeepSeek via OpenRouter
            "google": ModelPlatformType.GEMINI,
            "anthropic": ModelPlatformType.ANTHROPIC,
        }
        
        if "/" in model_str:
            provider, model_name = model_str.split("/", 1)
            platform = provider_map.get(provider, ModelPlatformType.OPENAI)
        else:
            platform = ModelPlatformType.OPENAI
            model_name = model_str
        
        # Create model
        try:
            if platform == ModelPlatformType.GEMINI:
                return ModelFactory.create(
                    model_platform=platform,
                    model_type=model_name,
                    model_config_dict={"temperature": 0}
                )
            else:
                # For OpenAI-compatible (Groq, DeepSeek via OpenRouter)
                return ModelFactory.create(
                    model_platform=platform,
                    model_type=model_name,
                    model_config_dict={"temperature": 0}
                )
        except Exception as e:
            logger.warning(f"Failed to create model {model_str}: {e}")
            # Fallback to default
            return ModelFactory.create(
                model_platform=ModelPlatformType.OPENAI,
                model_type=ModelType.GPT_4O_MINI,
                model_config_dict={"temperature": 0}
            )

# Global instance
owl_brain = OWLBrain()

if __name__ == "__main__":
    # Test
    print("Testing OWL Brain...")
    result = owl_brain.execute_task("What is 2+2? Explain step by step.")
    print(f"Answer: {result['answer']}")
    print(f"Tokens: {result['tokens_used']}")
