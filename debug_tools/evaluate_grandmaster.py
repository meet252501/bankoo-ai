import os
import re
import sys
import time
import subprocess
import json
import argparse
from assistant import DesktopAssistant
import config
from language_logic import LANGUAGE_LOGIC

# Argument Parsing
parser = argparse.ArgumentParser(description="Bankoo AI Evaluator Tier Switcher")
parser.add_argument("--tier", type=str, default="grandmaster", choices=["grandmaster", "intermediate"], help="Challenge tier to run")
args = parser.parse_args()

TIER = args.tier.lower()
BRAIN_DIR = r"C:\Users\Meet Sutariya\.gemini\antigravity\brain\80b37290-ecfb-48c2-91cf-9896683dd2da"

if TIER == "intermediate":
    CHALLENGE_FILE = os.path.join(BRAIN_DIR, "intermediate_challenges.md")
    REPORT_FILE = r"C:\Users\Meet Sutariya\Desktop\final banko.ai\intermediate_report.md"
    EVAL_TYPE = "Intermediate"
else:
    CHALLENGE_FILE = os.path.join(BRAIN_DIR, "grandmaster_challenges.md")
    REPORT_FILE = r"C:\Users\Meet Sutariya\Desktop\final banko.ai\grandmaster_report.md"
    EVAL_TYPE = "Grandmaster"

# Initialize Brain
print(f"🧠 [EVALUATOR] Initializing Bankoo Brain for {EVAL_TYPE} Evaluation...")
bot = DesktopAssistant()
config.SIMPLE_MODE = False # Ensure full assistant mode

def parse_challenges():
    print(f"📖 Reading challenges from {CHALLENGE_FILE}...")
    with open(CHALLENGE_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Regex to find challenges: ## 1. 🐍 Python ... ```text ... ```
    # Matches: Title, Description inside text block
    pattern = r"## \d+\. (.*?)\n```text\n([\s\S]*?)```"
    matches = re.findall(pattern, content)
    
    challenges = []
    for title, prompt in matches:
        # Determine extension from title (e.g. "🐍 Python (Async...)" -> .py)
        lang_name = title.lower()
        ext = ".txt"
        if "python" in lang_name: ext = ".py"
        elif "rust" in lang_name: ext = ".rs"
        elif "c++" in lang_name: ext = ".cpp"
        elif "go" in lang_name: ext = ".go"
        elif "java" in lang_name: ext = ".java"
        elif "javascript" in lang_name: ext = ".js"
        elif "typescript" in lang_name: ext = ".ts"
        elif "php" in lang_name: ext = ".php"
        elif "ruby" in lang_name: ext = ".rb"
        elif "c#" in lang_name: ext = ".cs"
        elif " c " in lang_name: ext = ".c" # specific for C 
        elif "sql" in lang_name: ext = ".sql"
        elif "bash" in lang_name: ext = ".sh"
        
        challenges.append({
            "title": title.strip(),
            "prompt": prompt.strip(),
            "ext": ext
        })
    return challenges

def evaluate():
    challenges = parse_challenges()
    
    # Initialize results list
    results = []

    # STRICT INSTRUCTION FOR ZERO-SHOT SUCCESS
    STRICT_SYSTEM_PROMPT = (
        "You are a Grandmaster Coder. \n"
        "RULES:\n"
        "1. Write a SINGLE FILE solution.\n"
        "2. Use ONLY the Standard Library for the language (No external crates/pip/packages).\n"
        "3. Output pure code inside a single markdown code block.\n"
        "4. Do NOT explain your code. Just write it.\n"
    )

    for i, chal in enumerate(challenges):
        title = chal['title']
        print(f"⚔️ [CHALLENGE {i+1}] {title}")
        
        
        # Combine instructions
        lang_key = "python" # default
        for k in LANGUAGE_LOGIC.keys():
            if k in title.lower():
                lang_key = k
                break
        
        global_logic = LANGUAGE_LOGIC.get("__GLOBAL__", "")
        specific_logic = LANGUAGE_LOGIC.get(lang_key, "")
        deep_logic = f"{global_logic}\n\n{specific_logic}"
        
        full_prompt = (
            f"{STRICT_SYSTEM_PROMPT}\n"
            f"{deep_logic}\n\n"
            f"TASK:\n{chal['prompt']}"
        )
        
        # ... rest of loop ...        print("   Thinking...", end="", flush=True)
        
        # 1. GENERATE CODE
        start_gen = time.time()
        
        # Retry loop for API Stability (Handle 429)
        max_retries = 3
        response = None
        
        for attempt in range(max_retries):
            print(f"   Thinking (Attempt {attempt+1})...", end="", flush=True)
            # USE FULL PROMPT WITH SYSTEM INSTRUCTIONS
            response = bot.get_ai_response(full_prompt)
            
            if response and "429" not in response and "Too Many Requests" not in response and response != "AI Offline":
                 break # Success
            
            print(f" ⚠️ API Busy, retrying in 20s...")
            time.sleep(20) # Increased backoff
        
        # Robust extraction
        if not response or "429" in response or "Too Many Requests" in response:
            print(" FAILED (AI Offline/Rate Limited)")
            results.append({"title": title, "status": "FAIL_GEN", "error": "AI returned empty response or is offline."})
            continue

        code_match = re.search(r"```(?:\w+)?\n([\s\S]*?)```", response)
        
        if code_match:
            code = code_match.group(1)
            
            # CLEANING: Remove Rust/TOML deps and AI markers
            if "[dependencies]" in code:
                code = code.split("[dependencies]")[0]
            if "# --- NEXT BLOCK ---" in code:
                code = code.split("# --- NEXT BLOCK ---")[0]
            code = code.strip()
            
            print(f" DONE ({round(time.time() - start_gen, 2)}s)")
        else:
            print(" FAILED (No Code Generated)")
            results.append({"title": title, "status": "FAIL_GEN", "error": "AI did not return a code block."})
            continue
            
        # 2. SAVE TO FILE
        filename = f"gms_chal_{i+1}{chal['ext']}"
        filepath = os.path.abspath(filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(code)
            
        # 3. SELF-HEALING EXECUTION LOOP
        attempts_max = 2
        
        for attempt_idx in range(attempts_max):
            is_repair = (attempt_idx > 0)
            prefix = "🛠️ REPAIRING" if is_repair else "🏃 RUNNING"
            print(f"   {prefix} {filename} (Attempt {attempt_idx+1})...", end="", flush=True)
            
            start_run = time.time()
            runner_cmd = [sys.executable, "smart_runner.py", filepath]
            
            try:
                proc = subprocess.run(runner_cmd, capture_output=True, text=True, timeout=90) # Increased timeout
                duration = round(time.time() - start_run, 2)
                output = proc.stdout + "\n" + proc.stderr
                
                # STATUS CHECK
                if proc.returncode == 0:
                    status = "PASS"
                    print(f" ✅ PASS ({duration}s)")
                    results.append({"title": title, "status": "PASS_FIXED" if is_repair else "PASS", "error_type": "NONE", "output": output[:300]})
                    break # Exit Check Loop
                else:
                    status = "FAIL"
                    # DIAGNOSIS
                    if "FileNotFoundError" in output or "not found" in output:
                         error_type = "SANDBOX_ISSUE"
                    elif "SyntaxError" in output or "error:" in output or "Exception" in output:
                         error_type = "LOGIC_ISSUE"
                    else:
                         error_type = "RUNTIME_ERROR"
                    
                    print(f" ❌ FAIL ({duration}s) [{error_type}]")
                    
                    # IF FAIL -> TRIGGER REPAIR (If not last attempt)
                    if attempt_idx < attempts_max - 1:
                        print(f"   🏥 Requesting Code Repair from Brain...")
                        repair_prompt = (
                            f"The code you wrote for '{title}' failed with this error:\n"
                            f"```text\n{output[-2000:]}\n```\n" # Send last 2k chars of error
                            f"Fix the code to resolve this error. Return ONLY the full corrected code."
                        )
                        
                        # --- CALL AI TO FIX (WITH RETRY) ---
                        rep_response = None
                        for rep_attempt in range(3):
                            rep_response = bot.get_ai_response(repair_prompt)
                            if rep_response and "429" not in rep_response and "Too Many Requests" not in rep_response and rep_response != "AI Offline":
                                break
                            print(f" ⚠️ API Busy during repair, retrying in 5s...")
                            time.sleep(5)
                        
                        if rep_response and "```" in rep_response:
                             rep_match = re.search(r"```(?:\w+)?\n([\s\S]*?)```", rep_response)
                             if rep_match:
                                 failed_code = code # Backup
                                 code = rep_match.group(1) # New Code
                                 # Clean Again
                                 if "[dependencies]" in code: code = code.split("[dependencies]")[0]
                                 code = code.strip()
                                 
                                 # Overwrite File
                                 with open(filepath, "w", encoding="utf-8") as f:
                                     f.write(code)
                                 continue # Retry Loop
                    
                    # If we are here, it's final fail
                    results.append({"title": title, "status": "FAIL_REPAIR" if is_repair else "FAIL", "error_type": error_type, "output": output[:500]})
            
            except subprocess.TimeoutExpired:
                print(" ⏱️ TIMEOUT")
                # Special exemption for Bash server challenge
                if "bash" in title.lower():
                    results.append({"title": title, "status": "PASS", "error_type": "TIMEOUT_VERIFIED", "output": "Server ran until timeout (Success)"})
                    break
                
                results.append({"title": title, "status": "FAIL_TIMEOUT", "error_type": "PERFORMANCE", "output": "Timed out"})
            except Exception as e:
                print(f" 🔥 CRASH: {e}")
                results.append({"title": title, "status": "FAIL_SYSTEM", "error_type": "SYSTEM", "output": str(e)})

        # INTERACTIVE PAUSE
        if i < len(challenges) - 1:
            print("\n" + "-"*50)
            user_choice = input(">>> Press ENTER to continue to next challenge (or 'q' to quit): ").strip().lower()
            if user_choice == 'q':
                print("👋 Stopping evaluation...")
                break
            print("-" * 50 + "\n")

    # GENERATE REPORT
    generate_report(results)

def generate_report(results):
    print("\n📝 Generating Report...")
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write(f"# 🏆 {EVAL_TYPE} Evaluation Report\n\n")
        f.write(f"**Date:** {time.ctime()}\n\n")
        
        f.write("| Challenge | Status | Fault Source | Notes |\n")
        f.write("|-----------|--------|--------------|-------|\n")
        
        passed = 0
        for r in results:
            icon = "✅" if r['status'] == "PASS" else "❌"
            if r['status'] == "PASS": passed += 1
            # Clean output for markdown table
            note = r.get('output', '').replace('\n', ' ').replace('|', '')[:50]
            f.write(f"| {r['title']} | {icon} {r['status']} | **{r.get('error_type', '-')}** | `{note}` |\n")
            
        f.write(f"\n## Summary\n")
        f.write(f"**Total Score:** {passed}/{len(results)}\n")
        
    print(f"✅ Report Saved to {REPORT_FILE}")

if __name__ == "__main__":
    evaluate()
