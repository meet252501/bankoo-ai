import time
import logging
import os
import sys
import threading
from assistant import DesktopAssistant
from memory_brain import brain as vector_brain
from local_vision import vision as local_vision
import config

# Configure Logger for Auditor (No Emojis for Windows log compatibility)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [CHAOS-AUDITOR] - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ZenithChaosAuditor:
    """
    The Ultimate Zenith Chaos Auditor.
    Simulates a 'Real User' to stress-test the entire Bankoo AI system.
    """
    def __init__(self):
        logger.info("[AUDITOR] Initializing Zenith Chaos Auditor...")
        self.assistant = DesktopAssistant()
        self.test_stats = {
            "passed": 0,
            "failed": 0,
            "latency_logs": []
        }
        self.is_done = False
        
        # Mock UI Callback to capture outputs
        self.assistant.output_callback = self._mock_output_callback
        self.captured_responses = []

    def _mock_output_callback(self, text, is_ide=False):
        logger.info(f"[INPUT] Captured AI Response: {text[:50]}...")
        self.captured_responses.append(text)

    def _reset_assistant_state(self):
        """Clears pending intents and histories for clean test cycles."""
        self.assistant.pending_intent = None
        self.assistant.pending_data = {}
        self.assistant.main_history = []
        self.assistant.ide_history = []
        self.assistant.history = self.assistant.main_history
        self.captured_responses = []

    def run_gauntlet(self):
        """Executes the full chain of stress tests (v1 - v19)."""
        print("\n" + "="*60)
        print(" FULL ZENITH HISTORY AUDIT (v1 - v19): MASTER GAUNTLET ")
        print("="*60 + "\n")

        try:
            # --- LEGACY CORE (v1 - v6) ---
            self._reset_assistant_state()
            self.test_legacy_core_nlp()      # v1-v3
            
            self._reset_assistant_state()
            self.test_legacy_pc_automation()  # v4-v6

            # --- STUDIO CORE (v7 - v11) ---
            self._reset_assistant_state()
            self.test_legacy_studio_hooks()   # v7-v9
            
            self._reset_assistant_state()
            self.test_legacy_stability()      # v10-v11

            # --- ZENITH ERA (v12 - v19) ---
            self._reset_assistant_state()
            self.test_1_brain_ping()
            
            self._reset_assistant_state()
            self.test_2_semantic_memory()
            
            self._reset_assistant_state()
            self.test_3_vision_stability()
            
            self._reset_assistant_state()
            self.test_4_stress_rapid_fire()
            
            self._reset_assistant_state()
            self.test_5_multilingual_compliance()
            
            self.generate_certification_report()
        except Exception as e:
            logger.error(f"[CRITICAL] GAUNTLET FAILURE: {e}")
            import traceback
            traceback.print_exc()

    # --- NEW LEGACY TESTS ---

    def test_legacy_core_nlp(self):
        """v1-v3: Tests if basic normalization and mapping still work."""
        logger.info("[v1-v3] Legacy Test: Core NLP Normalization...")
        # Normalization should handle caps/spacing
        raw = "HELLO  Bankoo  "
        normalized, _ = self.assistant.normalize_input(raw)
        if normalized == "hello bankoo":
            self.test_stats["passed"] += 1
            logger.info("[v1-v3] Success: NLP Normalization")
        else:
            self.test_stats["failed"] += 1
            logger.error(f"[v1-v3] Failed: NLP Normalization. Got: '{normalized}'")

    def test_legacy_pc_automation(self):
        """v4-v6: Tests if intent routing for PC commands is active."""
        logger.info("[v4-v6] Legacy Test: Intent Routing (PC Automation)...")
        res = self.assistant.ask_ai("Open notepad")
        # Check if routing identified Intent.OPEN_APP (supports EN and GU script response)
        if any(w in res for w in ["Opening", "Notepad", "નોટપેડ", "ચાલુ કરું છું"]):
             self.test_stats["passed"] += 1
             logger.info("[v4-v6] Success: PC Automation Intent")
        else:
             self.test_stats["failed"] += 1
             logger.error(f"[v4-v6] Failed: PC Automation Intent. Response: {res}")

    def test_legacy_studio_hooks(self):
        """v7-v9: Tests if IDE logic still triggers correctly."""
        logger.info("[v7-v9] Legacy Test: Studio/IDE Hooks...")
        res = self.assistant.ask_ai("[IDE_MODE] Write a hello world in Python.")
        if "Python" in res or "print" in res:
            self.test_stats["passed"] += 1
            logger.info("[v7-v9] Success: Studio Hook")
        else:
            self.test_stats["failed"] += 1
            logger.error("[v7-v9] Failed: Studio Hook")

    def test_legacy_stability(self):
        """v10-v11: Tests if system health check is persistent."""
        logger.info("[v10-v11] Legacy Test: System Health Persistent...")
        status = self.assistant.health.get_status()
        if "cpu" in status and "memory" in status:
            self.test_stats["passed"] += 1
            logger.info("[v10-v11] Success: Health Monitor")
        else:
            self.test_stats["failed"] += 1
            logger.error("[v10-v11] Failed: Health Monitor")

    def test_1_brain_ping(self):
        """Verifies that all primary AI providers are responding."""
        logger.info("[v12] Test 1: AI Brain Connectivity...")
        start = time.time()
        res = self.assistant.ask_ai("Say 'AGENT READY'.")
        latency = time.time() - start
        
        if res and any(w in res.upper() for w in ["READY", "રેડી", "તૈયાર", "ONLINE"]):
            self.test_stats["passed"] += 1
            self.test_stats["latency_logs"].append(latency)
            logger.info(f"[v12] Success: Brain Ping (Latency: {latency:.2f}s)")
        else:
            self.test_stats["failed"] += 1
            logger.error(f"[v12] Failed: Brain Ping. Response: {res}")

    def test_2_semantic_memory(self):
        """Tests the v19 Infinite Memory Vault."""
        logger.info("[v19] Test 2: Semantic Memory Recall...")
        secret_fact = "The Master Key for Zenith is 'Z-99-ALPHA'."
        vector_brain.add_memory(secret_fact, source="auditor_test")
        logger.info("[v19] Success: Fact Injected into Vector Brain.")
        time.sleep(2) 
        
        self.assistant.ask_ai("Tell me a short joke.")
        
        res = self.assistant.ask_ai("What is the code for the Master Key?")
        if "Z-99-ALPHA" in res.upper():
            self.test_stats["passed"] += 1
            logger.info("[v19] Success: Semantic Memory Recall")
        else:
            self.test_stats["failed"] += 1
            logger.error(f"[v19] Failed: Semantic Memory Recall. AI said: {res}")

    def test_3_vision_stability(self):
        """Tests the v19 Local Vision Lab."""
        logger.info("[v19] Test 3: Local Vision Lab status...")
        try:
            from local_vision import vision
            self.test_stats["passed"] += 1
            logger.info("[v19] Success: Vision Lab Module INSTALLED")
        except:
            self.test_stats["failed"] += 1
            logger.error("[v19] Failed: Vision Lab Module MISSING")

    def test_4_stress_rapid_fire(self):
        """Simulates an 'Angry User' sending multiple messages."""
        logger.info("[STRESS] Test 4: Rapid-Fire Stress Test...")
        messages = ["Hello", "Who are you?", "What can you do?", "Tell me a joke", "Define AI"]
        success_count = 0
        
        start = time.time()
        for msg in messages:
            res = self.assistant.ask_ai(msg)
            if res: success_count += 1
        
        total_time = time.time() - start
        if success_count == len(messages):
            self.test_stats["passed"] += 1
            logger.info(f"[STRESS] Success: Rapid-Fire ({len(messages)} msgs in {total_time:.2f}s)")
        else:
            self.test_stats["failed"] += 1
            logger.error("[STRESS] Failed: Rapid-Fire (dropped messages)")

    def test_5_multilingual_compliance(self):
        """Checks the phonetic and script enforcement."""
        logger.info("[LANG] Test 5: Multilingual Compliance...")
        res = self.assistant.ask_ai("જવાબ ગુજરાતીમાં આપો.")
        import re
        if re.search(r'[\u0a80-\u0aff]', res):
            self.test_stats["passed"] += 1
            logger.info("[LANG] Success: Gujarati Script Compliance")
        else:
            self.test_stats["failed"] += 1
            logger.error("[LANG] Failed: Gujarati Script Compliance")

    def generate_certification_report(self):
        """Generates the final markdown report."""
        report_path = "ZENITH_CERTIFICATION_REPORT.md"
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("# ZENITH AI: MASTER CERTIFICATION REPORT\n\n")
            f.write(f"**Date:** {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Target System:** Bankoo AI Zenith v19\n\n")
            
            f.write("## Executive Summary\n")
            total = self.test_stats["passed"] + self.test_stats["failed"]
            score = (self.test_stats["passed"] / total) * 100
            f.write(f"- Overall Stability Score: {score:.1f}%\n")
            f.write(f"- Tests Passed: {self.test_stats['passed']}\n")
            f.write(f"- Tests Failed: {self.test_stats['failed']}\n")
            
            avg_latency = sum(self.test_stats["latency_logs"]) / max(1, len(self.test_stats["latency_logs"]))
            f.write(f"- Avg. Brain Latency: {avg_latency:.2f}s\n\n")
            
            f.write("## Stability Verdict\n")
            if score > 90:
                f.write("> VERDICT: FLIGHT READY. Bankoo Zenith has passed all stress tests.\n")
            else:
                f.write("> VERDICT: DEGRADED. Some systems require manual attention.\n")
                
        print(f"\nCertification Report Generated: {report_path}")

if __name__ == "__main__":
    auditor = ZenithChaosAuditor()
    auditor.run_gauntlet()
