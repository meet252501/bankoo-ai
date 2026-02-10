
import sys
import os
import time

# Add project path to sys.path
sys.path.append(r"c:\Users\Meet Sutariya\Desktop\final banko.ai")

from assistant import DesktopAssistant

def test_traces():
    print("--- Bankoo Trace Verification ---")
    assistant = DesktopAssistant()
    
    # Trigger a local intent (e.g., lock pc bypass)
    # We won't actually lock it, just check if the logic triggers the logger
    print("Simulating 'lock pc' request...")
    assistant.ask_ai("lock pc")
    
    # Check if logs/traces directory exists and has a file
    trace_dir = "logs/traces"
    if os.path.exists(trace_dir):
        files = os.listdir(trace_dir)
        if files:
            print(f"✅ SUCCESS: Trace file generated: {files[-1]}")
            # Peek into the file
            with open(os.path.join(trace_dir, files[-1]), "r", encoding="utf-8") as f:
                last_line = f.readlines()[-1]
                print(f"Trace Content: {last_line[:200]}...")
        else:
            print("❌ FAILURE: No trace files found in directory.")
    else:
        print("❌ FAILURE: logs/traces directory not created.")

if __name__ == "__main__":
    test_traces()
