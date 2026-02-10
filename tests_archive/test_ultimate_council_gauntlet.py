

import sys
import logging
import time
import ai_council

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

def run_ultimate_gauntlet():
    print("==================================================")
    print("   ⚔️ BANKOO ENTERPRISE: THE ALL-HANDS GAUNTLET ⚔️")
    print("==================================================")
    print("Testing ALL 16 Corporate Roles with Expert-Level Challenges.")
    print("--------------------------------------------------\n")

    current_score = 0
    total_challenges = 0

    def run_test(role, challenge_name, prompt, validator_keyword):
        nonlocal current_score, total_challenges
        total_challenges += 1
        print(f"\n🔹 [TEST {total_challenges}] ROLE: {role}")
        print(f"   CHALLENGE: {challenge_name}")
        print("   Thinking...", end="", flush=True)
        
        start = time.time()
        verdict = ai_council.council._call_model(role, prompt)
        elapsed = time.time() - start
        
        print(f" (Took {elapsed:.1f}s)")
        print(f"👉 VERDICT (Snippet):\n{verdict[:200].replace(chr(10), ' ')}...")
        
        if validator_keyword.lower() in verdict.lower():
            print("✅ PASS")
            current_score += 1
        else:
            print(f"⚠️ WARN: Expected keyword '{validator_keyword}' missing.")

    # === C-SUITE ===
    run_test("CEO", "Crisis Management", 
             "Our database was just leaked. Issue a press statement holding us accountable while reassuring investors.", "responsibility")
    
    run_test("CTO", "Netflix Architecture", 
             "Design a video streaming architecture for 10M concurrent users. Focus on CDNs and Sharding.", "CDN")
    
    run_test("CSO", "Market Disruption", 
             "Plan a strategy to disrupt the Generative AI market in 2026. Focus on 'Vertical Integration'.", "vertical")
    
    run_test("CISO", "Authentication Audit", 
             "Explain the security flaw in using JWTs without expiration. Mention 'Replay Attacks'.", "replay")
    
    run_test("CDO", "Avant-Garde UI", 
             "Describe a UI concept for a holographic OS. Use words like 'Spatial', 'Depth', 'Glass'.", "Image Generation")
    
    # === UPGRADED EXECUTIVE CHALLENGES (GRANDMASTER LEVEL) ===
    run_test("CCO", "Antitrust Defense", 
             "Draft a defense strategy for a DOJ Antitrust lawsuit regarding AI monopoly.", "strategy")

    # === UPGRADED ENGINEERING CHALLENGES ===
    run_test("SENIOR_ENGINEER", "Raft Consensus", 
             "Implement the 'Leader Election' phase of the Raft Consensus Protocol in Python.", "election")

    run_test("PLATFORM_ARCHITECT", "Zero-Trust Mesh", 
             "Design a Service Mesh architecture with mTLS and OPA policies for a banking cluster.", "mTLS")
    
    run_test("PERFORMANCE_ENGINEER", "SIMD Optimization", 
             "Explain how to optimize 4x4 Matrix Multiplication using AVX-512 SIMD instructions in C++.", "AVX")

    # === LEGACY & FUNCTIONAL (NOW HARD MODE) ===
    print("\n--- 🕰️ LEGACY & FUNCTIONAL KEYS (Now Expert Level) ---")
    
    run_test("ARCHITECT", "Legacy: Satellite Net", 
             "Design a low-latency routing protocol for a LEO satellite constellation (Starlink-like).", "routing")
             
    run_test("SENIOR_CODER", "Legacy: Kernel Driver", 
             "Write a skeleton Linux Kernel Module (Driver) in C that handles interrupts.", "module")

    # === FUNCTIONAL KEYS (HARD) ===
    run_test("PRIMARY_MODEL", "Universal Translator", 
             "Translate 'The quick brown fox' into Ancient Sanskrit and Linear B.", "Sanskrit")
             
    run_test("SECURITY_MODEL", "Zero-Day Analysis", 
             "Analyze the theoretical attack vector of a 'Rowhammer' exploit on DDR5 RAM.", "bit flip")

    print("\n==================================================")
    print(f"🏁 RESULTS: {current_score}/{total_challenges} PASSED")
    print("==================================================")
    
    input("Press Enter to exit...")

if __name__ == "__main__":
    run_ultimate_gauntlet()
