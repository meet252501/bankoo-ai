import os
import sys
import time
import json
from agent_logger import trace_logger

# Get the base directory (where this script is located)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def verify_instrumentation():
    print("🔍 [1/3] Testing Instrumentation (Logger)...")
    
    # Log a test trace
    trace_logger.log_interaction(
        user_input="Test Zenith Connection",
        system_prompt="You are a test agent.",
        assistant_response="Connection confirmed.",
        tools_used=[],
        reward=1.0
    )
    
    # Check if a trace file was created in logs/traces/
    trace_dir = os.path.join(BASE_DIR, "logs", "traces")
    if not os.path.exists(trace_dir):
        print(f"❌ FAILED: Trace directory not found at {trace_dir}")
        return False
        
    traces = os.listdir(trace_dir)
    if not traces:
        print("❌ FAILED: No trace files found.")
        return False
        
    print(f"✅ SUCCESS: Instrumentation is recording (Found {len(traces)} sessions).")
    return True

def verify_dependencies():
    print("\n🔍 [2/3] Checking Optimization Dependencies...")
    try:
        import agentlightning
        print("✅ SUCCESS: 'agentlightning' is installed in this environment.")
    except ImportError:
        print("⚠️  NOTE: 'agentlightning' not found in Windows environment.")
        print("   (This is normal if you plan to run the optimizer in WSL as recommended).")
    
    # Check for zenith_optimizer.py
    optimizer_path = os.path.join(BASE_DIR, "zenith_optimizer.py")
    if os.path.exists(optimizer_path):
        print("✅ SUCCESS: 'zenith_optimizer.py' is present.")
    else:
        print(f"❌ FAILED: 'zenith_optimizer.py' is missing at {optimizer_path}.")
        return False
    return True

def verify_dashboard():
    print("\n🔍 [3/3] Checking Visual Dashboard...")
    dashboard_path = os.path.join(BASE_DIR, "logs", "brain_dashboard.html")
    if os.path.exists(dashboard_path):
        mtime = os.path.getmtime(dashboard_path)
        last_gen = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mtime))
        print(f"✅ SUCCESS: Dashboard exists (Last updated: {last_gen}).")
    else:
        print("⚠️  NOTE: Dashboard not generated yet. Run 'gen_dashboard.bat' first.")
    return True

if __name__ == "__main__":
    print("========================================")
    print("   ZENITH LIGHTNING AGENT: DIAGNOSTIC   ")
    print("========================================\n")
    
    s1 = verify_instrumentation()
    s2 = verify_dependencies()
    s3 = verify_dashboard()
    
    print("\n========================================")
    if s1 and s2:
        print("🟢 STATUS: ZENITH SYSTEM READY")
        print("   Bankoo is learning from every interaction.")
    else:
        print("🔴 STATUS: ISSUES DETECTED")
    print("========================================")
