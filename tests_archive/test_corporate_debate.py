
import sys
import logging
import ai_council

# Setup simple logging to see the "Room" chatter
logging.basicConfig(level=logging.INFO, format='%(message)s')

def run_simulation():
    print("==================================================")
    print("   🏢 BANKOO CORP - BOARDROOM SIMULATION V1.0")
    print("==================================================")
    print("Scenario: The Board is meeting to discuss a new high-stakes project.")
    print("Project: 'Develop a Secure, Real-Time Chat Application with End-to-End Encryption'")
    print("--------------------------------------------------\n")
    
    print("💼 CEO calls the meeting to order...")
    print("⏳ The Executives are deliberating (This triggers the 4-Round Debate)...")
    print("(Please wait ~30-60 seconds for the full minutes of the meeting)\n")
    
    result = ai_council.council.debate("Create a Secure Real-Time Chat App with E2E Encryption using Python and WebSockets")
    
    print("\n--------------------------------------------------")
    print("✅ MEETING ADJOURNED. FINAL MINUTES:")
    print("--------------------------------------------------")
    print(result)
    
    # Save to file outcome
    with open("boardroom_minutes.md", "w", encoding="utf-8") as f:
        f.write("# 🏢 Boardroom Meeting Minutes\n\n")
        f.write(result)
    
    print("\n📄 Full report saved to: boardroom_minutes.md")
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    run_simulation()
