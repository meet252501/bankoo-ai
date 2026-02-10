
import sys
import logging
import time
import ai_council

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

def run_swe_bench_simulation():
    print("==================================================")
    print("   🧪 BANKOO INC - SWE-BENCH SIMULATION (HARD MODE)")
    print("==================================================")
    print("Objective: The 'VP of Engineering' must fix a subtle logic bug.")
    print("The Bug: A 'Bank Account' class that attempts to be thread-safe but fails.")
    print("Difficulty: HIGH (Requires understanding race conditions).")
    print("--------------------------------------------------\n")

    # 1. The Broken Code
    broken_code = """
class BankAccount:
    def __init__(self, balance=0):
        self.balance = balance
        self.transactions = []

    def withdraw(self, amount):
        # SIMULATING A RACE CONDITION VULNERABILITY
        if self.balance >= amount:
            # Simulate network latency causing a race window
            import time
            time.sleep(0.1) 
            self.balance -= amount
            self.transactions.append(f"Withdrew {amount}")
            return True
        return False
        
    def deposit(self, amount):
        print(f"Depositing {amount}")
        self.balance += amount
        return True
"""
    
    print("❌ [PROBLEM] Here is the buggy code submitted by a Junior Dev:")
    print(broken_code)
    print("\n--------------------------------------------------")
    print("🚀 SENDING TO VP OF ENGINEERING (DeepSeek V3)...")
    print("--------------------------------------------------")
    
    # 2. The Challenge Prompt
    prompt = f"""
    You are the VP of Engineering.
    Review this Python code for a Banking System.
    
    CODE:
    {broken_code}
    
    ISSUE:
    Users are reporting they can double-spend (withdraw more money than they have) when making concurrent requests.
    
    TASK:
    1. Identify the specific concurrency bug (Race Condition).
    2. Rewrite the code to be THREAD-SAFE.
    3. Use 'threading.Lock()' context manager.
    4. Return ONLY the fixed Python class.
    """
    
    # 3. Call the Council
    # We call 'VP_ENGINEERING' directly for this specific task
    response = ai_council.council._call_model("VP_ENGINEERING", prompt)
    
    print("\n✅ [SOLUTION] VP's Patch:")
    print(response)
    
    print("\n--------------------------------------------------")
    print("🏁 INTELLIGENCE REPORT:")
    if "Lock" in response or "lock" in response:
        print("PASS: The AI correctly identified the need for a Lock.")
    else:
        print("FAIL: The AI missed the race condition.")
    print("--------------------------------------------------")
    
    # Save Proof
    with open("swe_bench_result.py", "w", encoding="utf-8") as f:
        f.write("# FIXED BY BANKOO VP ENGINEERING\n")
        f.write(response)
        
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    run_swe_bench_simulation()
