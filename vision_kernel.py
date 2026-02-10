import os
import time
import json
import logging
import pyautogui
import pyperclip
from vision_agent import VisionAgent
from vision_utils import VisionUtils

logger = logging.getLogger(__name__)

class VisionKernel:
    """The Mission Controller for Autonomous Screen Interaction"""
    
    def __init__(self, vision_agent: VisionAgent):
        self.agent = vision_agent
        self.max_steps = 20
        self.history = []
        self.stop_requested = False
        self.memory_path = "memory.json"
        self.memory = self._load_memory()
        
        # New System Prompt for Autonomous Loop (Zenith v4 - Surgical Precision & Shortcuts)
        self.kernel_prompt = (
            "You are the Autonomous Mission Controller for Bankoo AI (Zenith Ghost v4).\n"
            "You operate at the OS level using Visual-Action-Verify cycles.\n"
            "\n"
            "RULES FOR MISSION SUCCESS (ZENITH v6):\n"
            "0. VISUAL GRID: The image has a Red Grid (1-25). Use this to orient yourself.\n"
            "1. OBSERVATION: Carefully look at the screenshot. Identify all open windows and focused elements.\n"
            "2. PREFER SHORTCUTS: If you need to perform an app action (New File, Save, New Tab), use 'hotkey' instead of clicking menus.\n"
            "   (e.g., hotkey(['ctrl', 'n']) for New File in Notepad).\n"
            "3. FOCUS CHECK: Ensure the target app is in the foreground before typing. If not, CLICK it or use ALT+TAB.\n"
            "4. VERIFICATION: Verify your last action worked in the next screenshot before repeating it.\n"
            "5. NAVIGATION: Use 'win' key for searching apps. Do NOT type the goal into the chat window.\n"
            "6. IGNORE SELF-UI: Do NOT click on words or status messages belonging to the 'Mission Dashboard' or 'SAT-LINK' logs. Focus ONLY on desktop icons, taskbar, and application windows.\n"
            "\n"
            "ACTIONS available: \n"
            "   - click(nx, ny): Normalized 0-1000 coordinates. Use for focus/buttons.\n"
            "   - type(text): Type into active window.\n"
            "   - press(key): System keys ('win', 'enter', 'esc', 'tab', 'backspace').\n"
            "   - hotkey(keys): List of keys (e.g., ['ctrl', 'c'], ['alt', 'f4'], ['ctrl', 'n']).\n"
            "   - wait(): Smart wait until screen settles.\n"
            "   - read_clipboard(): Returns text from clipboard (for errors/context).\n"
            "   - scroll(direction): 'up' or 'down'.\n"
            "\n"
            "RETURN JSON ONLY: \n"
            "   {\n"
            "     \"thought\": \"[OBSERVATION] Found X. [VERIFICATION] Prev action ok? [INTENT] Use shortcut Y.\",\n"
            "     \"action\": \"hotkey/click/type/press/wait\",\n"
            "     \"params\": { ... },\n"
            "     \"status\": \"CONTINUE/DONE\"\n"
            "   }\n"
        )

    def _load_memory(self):
        try:
            if os.path.exists(self.memory_path):
                with open(self.memory_path, 'r') as f: return json.load(f)
        except: pass
        return {}

    def _save_memory(self):
        try:
            with open(self.memory_path, 'w') as f: json.dump(self.memory, f)
        except: pass

    def stop_mission(self):
        """Emergency Stop Signal"""
        self.stop_requested = True
        logger.warning("🚨 Emergency Stop Requested!")

    async def run_mission(self, goal, update_callback=None):
        """Execute a multi-step mission autonomously"""
        logger.info(f"🚀 Starting Mission: {goal}")
        self.stop_requested = False # Reset flag
        steps_taken = 0
        mission_status = "CONTINUE"
        last_success_path = None
        
        # Zenith v6: Hippocampus Check (Fast Path)
        # Check if the ENTIRE goal is just a known app launch (e.g., "open chrome")
        for app_name, coords in self.memory.items():
            if f"open {app_name}" in goal.lower():
                logger.info(f"🧠 Hippocampus Recall: Found {app_name} at {coords}")
                # Inject a fake "brain response" to skip the API call
                self.history.append({"step": 0, "thought": "Memory Retrieval", "action": "click", "params": coords})
                # Execute immediately
                nx, ny = coords['x'], coords['y']
                screen_w, screen_h = pyautogui.size()
                pyautogui.click(int((nx/1000)*screen_w), int((ny/1000)*screen_h))
                steps_taken += 1
                time.sleep(2) # Allow app to open
        
        while steps_taken < self.max_steps and mission_status == "CONTINUE":
            if self.stop_requested:
                return "🛑 Mission Aborted by User."
            steps_taken += 1
            temp_path = f"mission_step_{steps_taken}.jpg"
            
            try:
                # 1. Capture State & Draw Grid
                screen_w, screen_h = pyautogui.size()
                pyautogui.screenshot().save(temp_path)
                VisionUtils.draw_grid(temp_path, temp_path) # Overwrite with grid
                
                # 2. Consult Agent
                # Zenith v6: Self-Reflector (Did last action fail?)
                reflection_context = ""
                if last_success_path and steps_taken > 1:
                    diff = VisionUtils.calculate_diff(last_success_path, temp_path)
                    logger.info(f"🔍 Visual Delta: {diff}%")
                    if diff < 1.0 and self.history[-1]['action'] in ['click', 'type']:
                        reflection_context = "\n[WARNING]: The screen DID NOT CHANGE after your last action. It might have failed. ANALYZE WHY. Do not repeat the exact same coordinate."

                # User Context (State)
                state_info = (
                    f"MISSION GOAL: {goal}\n"
                    f"SCREEN RESOLUTION: {screen_w}x{screen_h}\n"
                    f"STEP: {steps_taken}/{self.max_steps}\n"
                    f"HISTORY: {self.history[-3:] if self.history else 'None'}\n"
                    f"{reflection_context}\n"
                )
                
                # We pass 'kernel_prompt' as the system override
                result = self.agent.analyze_screen(
                    image_path=temp_path, 
                    goal=state_info, 
                    system_prompt=self.kernel_prompt
                )
                
                if "error" in result:
                    logger.error(f"Mission Error: {result['error']}")
                    return f"Mission Failed: {result['error']}"

                # 3. Process Result
                thought = result.get("thought", "Thinking...")
                action = result.get("action", "none")
                params = result.get("params", {})
                mission_status = result.get("status", "CONTINUE")
                
                self.history.append({"step": steps_taken, "thought": thought, "action": action})
                
                if update_callback:
                    msg = (
                        f"🎯 **Goal:** {goal}\n"
                        f"🧠 **Step {steps_taken}:** {thought}\n"
                        f"🎬 Action: `{action}({params})`"
                    )
                    import asyncio
                    if asyncio.iscoroutinefunction(update_callback):
                        await update_callback(msg)
                    else:
                        update_callback(msg)

                # 4. Execute Action
                if action == "click":
                    nx, ny = params.get("x"), params.get("y")
                    # Scale normalized coordinates (0-1000) to actual screen resolution
                    screen_w, screen_h = pyautogui.size()
                    x = int((nx / 1000) * screen_w)
                    y = int((ny / 1000) * screen_h)
                    
                    # Zenith v6: Repeat Detection
                    last_action = self.history[-2] if len(self.history) > 1 else {}
                    if last_action.get("action") == "click" and last_action.get("params") == params and diff < 1.0:
                         logger.warning(f"🚫 BLOCKING repetitive click at ({nx}, {ny}) on frozen screen.")
                         # Force a small movement to jiggle it loose instead
                         pyautogui.moveTo(x + 10, y + 10, duration=0.5)
                         pyautogui.click()
                         time.sleep(1.0)
                         continue

                    logger.info(f"🖱️ Clicking: ({nx}, {ny}) -> Real: ({x}, {y}) on {screen_w}x{screen_h}")
                    pyautogui.moveTo(x, y, duration=0.8)
                    # Precision Jiggle
                    pyautogui.moveRel(5, 5, duration=0.1)
                    pyautogui.moveRel(-5, -5, duration=0.1)
                    pyautogui.click()
                    time.sleep(1.0) # Stability pause
                elif action == "type":
                    text = params.get("text")
                    pyautogui.typewrite(text, interval=0.1)
                    time.sleep(1.0) # Stability pause
                elif action == "press":
                    key = params.get("key")
                    pyautogui.press(key)
                    time.sleep(1.0) # Stability pause
                elif action == "hotkey":
                    keys = params.get("keys", [])
                    if isinstance(keys, list):
                        pyautogui.hotkey(*keys)
                        time.sleep(1.0) # Stability pause
                    else:
                        logger.warning(f"Invalid hotkey params: {keys}")
                elif action == "wait":
                    # Zenith v6: Smart Wait (Pixel Diff)
                    logger.info("⚡ Smart Waiting for pixels to settle...")
                    settled = VisionUtils.wait_for_settle(pyautogui.screenshot)
                    if not settled: logger.warning("⚠️ Screen didn't settle (animation loop?)")
                    
                elif action == "read_clipboard":
                    content = pyperclip.paste()
                    logger.info(f"📋 Visual Clipboard Read: {content[:50]}...")
                    # Inject into history for context
                    self.history.append({"step": steps_taken, "thought": "Read Clipboard", "action": f"DATA: {content}"})
                    
                elif action == "scroll":
                    direction = params.get("direction", "down")
                    pyautogui.scroll(-500 if direction == "down" else 500)
                
                # Short pause for UI update - replaced by Smart Wait in next loop implicitly
                # Time to settle is handled, but we need to track 'last_success_path' for diffing next time
                last_success_path = temp_path # Keep reference to THIS step's image for next comparison

            except Exception as e:
                logger.error(f"Mission Execution Error: {e}")
                return f"Mission Error: {str(e)}"
            finally:
                if os.path.exists(temp_path):
                    os.remove(temp_path)

        if mission_status == "DONE":
            return f"Mission Accomplished! ✅\nGoal: `{goal}`"
        else:
            return f"Mission Timed Out or Failed. ❌\nGoal: `{goal}`"
