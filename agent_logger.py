
import json
import os
import time
import datetime
import logging

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("BankooTrace")

class BankooTraceLogger:
    """
    Captures traces for Agent-Lightning optimization.
    Format is designed to be compatible with Agent-Lightning's TraceToMessages logic.
    """
    def __init__(self, log_dir=None):
        if log_dir is None:
            # Set absolute path to the project directory/logs/traces
            base_dir = os.path.dirname(os.path.abspath(__file__))
            self.log_dir = os.path.join(base_dir, "logs", "traces")
        else:
            self.log_dir = log_dir
            
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        
        self.current_trace_file = os.path.join(self.log_dir, f"trace_{datetime.datetime.now().strftime('%Y%b%d_%H%M%S')}.jsonl")
        logger.info(f"Initialized High-Fidelity Trace Logger: {self.current_trace_file}")

    def log_interaction(self, user_input, system_prompt, assistant_response, tools_used=None, reward=0, latency=0, complexity=0, lang='english'):
        """
        Logs a single high-fidelity interaction trace.
        """
        trace_data = {
            "timestamp": datetime.datetime.now().isoformat(),
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input},
                {"role": "assistant", "content": assistant_response}
            ],
            "tools": tools_used or [],
            "reward": reward,
            "metrics": {
                "latency_sec": latency,
                "complexity_score": complexity,
                "language": lang
            },
            "metadata": {
                "version": "3.3.0-ZENITH-ADVANCED",
                "client": "StandardAssistant"
            }
        }
        
        try:
            with open(self.current_trace_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(trace_data, ensure_ascii=False) + "\n")
        except Exception as e:
            logger.error(f"Failed to write trace: {e}")

    def log_tool_result(self, tool_name, tool_input, tool_output, success):
        """
        Helper to format tool call traces.
        """
        return {
            "tool": tool_name,
            "input": tool_input,
            "output": tool_output,
            "success": success
        }

# Global Instance
trace_logger = BankooTraceLogger()
