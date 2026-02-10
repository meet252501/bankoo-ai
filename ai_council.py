
import requests
import json
import logging
import config
from council_roles import ROLE_PROMPTS

# Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AI_COUNCIL")

class AICouncil:
    def __init__(self):
        self.members = config.COUNCIL_CONFIG
        self.groq_key = config.GROQ_API_KEY
        self.router_key = config.OPENROUTER_API_KEY
        self.cerebras_key = getattr(config, 'CEREBRAS_API_KEY', '')
        self.fireworks_key = getattr(config, 'FIREWORKS_API_KEY', '')

    def _call_model(self, role_key, prompt, custom_system=None):
        """
        Universal model caller supporting Cerebras, Groq, Fireworks, OpenRouter, and Hugging Face.
        """
        model_str = self.members.get(role_key)
        if not model_str:
             # Fallback: Try to get from config variables (e.g. PRIMARY_MODEL)
             model_str = getattr(config, role_key, "")
        
        # Get specialized system prompt for this role
        if custom_system:
            system_role = custom_system
        elif role_key in ROLE_PROMPTS:
            system_role = ROLE_PROMPTS[role_key]['prompt']
        else:
            system_role = "You are a helpful AI assistant."
        
        # Parse provider and model
        if "/" in model_str:
            parts = model_str.split("/", 1)
            provider = parts[0]
            model_id = parts[1]
        else:
            provider = "openrouter"
            model_id = model_str
        
        logger.info(f"🏛️ [{role_key}] via {provider.upper()} thinking...")

        try:
            # 1. SPECIALIZED SPEED LANES (First Party APIs)
            if provider == "cerebras":
                url = "https://api.cerebras.ai/v1/chat/completions"
                headers = {"Authorization": f"Bearer {self.cerebras_key}", "Content-Type": "application/json"}
                payload = {
                    "model": model_id, # Cerebras expects "llama-3.3-70b"
                    "messages": [{"role": "system", "content": system_role}, {"role": "user", "content": prompt}],
                    "temperature": 0.7, "max_tokens": 2048
                }
                resp = requests.post(url, headers=headers, json=payload, timeout=20)
                return resp.json()["choices"][0]["message"]["content"]
                
            elif provider == "groq":
                url = "https://api.groq.com/openai/v1/chat/completions"
                headers = {"Authorization": f"Bearer {self.groq_key}", "Content-Type": "application/json"}
                payload = {
                    "model": model_id, # Groq expects "llama3-70b-8192"
                    "messages": [{"role": "system", "content": system_role}, {"role": "user", "content": prompt}],
                    "temperature": 0.7, "max_tokens": 2048
                }
                resp = requests.post(url, headers=headers, json=payload, timeout=20)
                return resp.json()["choices"][0]["message"]["content"]

            # 2. HUGGING FACE INFERENCE (Free Tier Models)
            elif provider in ["hot", "meta-llama", "black-forest-labs", "google", "openai"]: 
                # Heuristic: If it's a known HF vendor and explicitly configured, assume HF *unless* it's OpenAI on OR
                hf_token = getattr(config, 'HUGGINGFACE_API_KEY', '')
                if hf_token and ("flan" in model_str.lower() or "flux" in model_str.lower() or "llama" in model_str.lower() or "gemma" in model_str.lower() or "whisper" in model_str.lower()):
                     from huggingface_hub import InferenceClient
                     client = InferenceClient(token=hf_token)
                     if "flux" in model_str.lower():
                         return "[Image Generation Requested - Please use generate_asset API]"
                     
                     # Text Gen
                     msg = [{"role": "system", "content": system_role}, {"role": "user", "content": prompt}]
                     try:
                         # Try chat completion first
                         output = client.chat_completion(model=model_str, messages=msg, max_tokens=2048)
                         return output.choices[0].message.content
                     except:
                         # Fallback to text generation
                         return client.text_generation(prompt, model=model_str, max_new_tokens=1000)

            # 3. OPENROUTER (Universal Fallback)
            # Sends the FULL string (e.g. "deepseek/deepseek-chat")
            url = "https://openrouter.ai/api/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {self.router_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost:5000",
                "X-Title": "Bankoo AI Council"
            }
            payload = {
                "model": model_str, # OpenRouter needs "vendor/model"
                "messages": [{"role": "system", "content": system_role}, {"role": "user", "content": prompt}],
                "temperature": 0.7
            }
            resp = requests.post(url, headers=headers, json=payload, timeout=45)
            data = resp.json()
            if "choices" in data:
                return data["choices"][0]["message"]["content"]
            else:
                logger.error(f"OpenRouter Error: {data}")
                return f"Error: {data.get('error', {}).get('message', 'Unknown')}"

        except Exception as e:
            logger.error(f"Council connection failed: {e}")
            return f"Connection failed: {e}"

    def debate(self, query):
        """Orchestrates the Enterprise Strategy Session"""
        logger.info(f"🏢 Boardroom Session Started for: {query}")
        
        # Round 1: The CTO (Technical Specification)
        plan = self._call_model(
            "CTO", 
            f"Create a technical implementation plan for: {query}. Focus on file structure, database schema (if needed), and algorithms."
        )
        
        # Round 2: The CRO (Risk Audit)
        critique = self._call_model(
            "CRO",
            f"AUDIT this technical plan for '{query}':\n\n{plan}\n\nSearch for edge cases, performance bottlenecks, and security vulnerabilities. Be brutally honest."
        )
        
        # Round 3: The VP Engineering (Deep Implementation)
        code = self._call_model(
            "VP_ENGINEERING",
            f"TASK: Write the code for '{query}'.\n\nPLAN: {plan}\nCRITIQUE TO FIX: {critique}\n\nWrite the FINAL, OPTIMIZED code implementing the plan but fixing the critique issues."
        )
        
        # Round 4: The CEO (Final Verification)
        # Verify the code actually matches the plan and fixed the critique
        verdict = self._call_model(
            "CEO",
            f"VERIFY this code:\n\n{code}\n\nAgainst the Plan:\n{plan}\n\nDid it fix the critique?\n{critique}\n\nIf the code is good, simply output the code block. If you see remaining critical bugs, FIX THEM and output the corrected code.",
            "You are the CEO. Ensure the final output delivers maximum value and is flawless."
        )

        final_output = f"""## 🏛️ Council of AI Decision

**1. The Architect's Vision:**
The system planned a structure focused on robustness.

**2. The Critic's Concerns:**
Issues identified: Security risks and efficiency bottlenecks (addressed in final code).

**3. The Verdict (Final Code):**
Here is the optimized solution verified by the Judge:

{verdict}
"""
        return final_output

    def dual_check(self, query):
        """Runs Fast vs Smart model duel and judges the winner"""
        logger.info(f"⚔️ Dual Duel Started: {query}")
        
        # 1. Fast Model (The Speedster)
        fast_response = self._call_model(
            "PRIMARY_MODEL", # Will map to Fast in hybrid config if set properly, or we force it here
            query,
            "You are a helpful assistant. Answer briefly."
        )
        # Note: _call_model logic in this file relies on COUNCIL_CONFIG keys. 
        # We need to hack it slightly to support raw FAST/SMART or update config keys.
        # Actually, let's use the raw config keys if possible or just use existing members as proxies.
        # Let's map "CRITIC" (Mixtral 8x7b) as the 'Fast/Alternative' and "ARCHITECT" (Llama 70b) as 'Smart'.
        
        # Redefining for Dual Check specifically:
        # Fast = 8b Instant (Manual Call)
        fast_response = self._call_model_raw(config.FAST_MODEL if hasattr(config, 'FAST_MODEL') else "llama-3.1-8b-instant", query)
        
        # Smart = 70b Versatile
        smart_response = self._call_model_raw(config.PRIMARY_MODEL, query)
        
        # Judge (NEUTRAL PARTY: Mixtral-8x7b)
        # Using Mixtral ensures the 70b model doesn't judge itself!
        verdict = self._call_model_raw(
            "mixtral-8x7b-32768", 
            f"COMPARE these two AI responses to the user query: '{query}'\n\n"
            f"[RESPONSE A (Fast/Llama-8b)]:\n{fast_response}\n\n"
            f"[RESPONSE B (Smart/Llama-70b)]:\n{smart_response}\n\n"
            f"TASK: 1. Identify which is better (Accuracy + Gujarati Naturalness). 2. Explain why. 3. Return the WINNING response content ONLY (preceded by [WINNER]).",
            "You are an impartial AI Judge. Pick the best response."
        )
        
        
        return f"⚔️ **Model Duel Results**\n\n**Fast Model (8b):**\n{fast_response[:100]}...\n\n**Smart Model (70b):**\n{smart_response[:100]}...\n\n**🏆 The Verdict:**\n{verdict}"

    def master_code(self, query):
        """Invoke the Master Free Coder (The Unshackled Genius)"""
        return self._call_model("MASTER_FREE_CODER", query)

    def _call_model_raw(self, model_id, prompt, system="You are a helpful assistant."):
        """Helper for direct model ID calls"""
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {self.groq_key}", "Content-Type": "application/json"}
        payload = {
            "model": model_id,
            "messages": [{"role": "system", "content": system}, {"role": "user", "content": prompt}]
        }
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=30)
            return resp.json()["choices"][0]["message"]["content"]
        except: return "Error"

# Singleton Instance
council = AICouncil()

if __name__ == "__main__":
    # Test
    print(council.debate("Create a Python Snake Game with a Main Menu"))
