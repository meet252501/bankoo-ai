
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.yfinance import YFinanceTools
from agno.tools.duckduckgo import DuckDuckGoTools

import os

# --- CONFIGURATION ---
# We use LiteLLM running locally on port 4000
LITELLM_BASE_URL = "http://localhost:4000/v1"
MODEL_NAME = "gpt-4o" # LiteLLM maps this to the actual provider (e.g., GitHub Models)

print("🧠 [NEXUS] Initializing Enterprise Agent Council...")

class AgentNexus:
    def __init__(self):
        self.agents = {}
        self._initialize_agents()

    def _initialize_agents(self):
        try:
            # 1. System Architect (Cloud & Infrastructure)
            self.agents['architect'] = Agent(
                name="System Architect",
                model=OpenAIChat(id=MODEL_NAME, base_url=LITELLM_BASE_URL, api_key="sk-fake-key"),
                instructions=[
                    "You are a Principal System Architect.",
                    "Design scalable, fault-tolerant cloud systems.",
                    "Always prefer modern stack (Kubernetes, Serverless, Event-Driven).",
                    "Output clean Mermaid diagrams where appropriate."
                ],
                markdown=True
            )

            # 2. VC Analyst (Finance & Market Research)
            self.agents['vc'] = Agent(
                name="VC Analyst",
                model=OpenAIChat(id=MODEL_NAME, base_url=LITELLM_BASE_URL, api_key="sk-fake-key"),
                tools=[
                    YFinanceTools(stock_price=True, analyst_recommendations=True, company_info=True),
                    DuckDuckGoTools()
                ],
                instructions=[
                    "You are a Venture Capital Analyst.",
                    "Analyze startups, markets, and financial data.",
                    "Be critical, data-driven, and succinct.",
                    "Use tools to fetch real-time data."
                ],
                show_tool_calls=True,
                markdown=True
            )

            # 3. Senior Engineer (Coding & Implementation)
            self.agents['coder'] = Agent(
                name="Senior Engineer",
                model=OpenAIChat(id=MODEL_NAME, base_url=LITELLM_BASE_URL, api_key="sk-fake-key"),
                instructions=[
                    "You are a Senior Staff Software Engineer.",
                    "Write high-performance, production-grade code.",
                    "Focus on clean architecture, types, and error handling.",
                    "Review code for security vulnerabilities."
                ],
                markdown=True
            )
            
            print("✅ [NEXUS] Agents Initialized: Architect, VC, Coder")
            
        except Exception as e:
            print(f"❌ [NEXUS] Initialization Failed: {e}")

    def ask_agent(self, agent_key, query):
        """
        Routes a query to a specific agent.
        agent_key: 'architect', 'vc', 'coder'
        """
        agent = self.agents.get(agent_key)
        if not agent:
            return f"⚠️ Agent '{agent_key}' not found or not initialized."
        
        try:
            # Run the agent
            response = agent.run(query)
            return response.content
        except Exception as e:
            return f"❌ Agent Error: {e}"

# Global Instance
nexus = AgentNexus()
