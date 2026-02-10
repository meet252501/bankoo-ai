"""
================================================================================
  BANKOO CORE v12: UNIFIED SYSTEMS ARCHITECTURE
================================================================================
  The Master Core that merges Flask UI and Telegram Bridge.
  Single Command Execution: python bankoo_core.py
================================================================================
"""
import threading
import time
import sys
import os
import logging

# Configure Logging for Unified Output
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)
logger = logging.getLogger("BankooCore")

def run_flask():
    """Run the Main Bankoo UI Backend"""
    logger.info("🚀 [UI] Initializing Bankoo Flask Server...")
    from bankoo_main import app
    # Flask is blocking, so it runs in its own thread
    app.run(port=5001, debug=False, use_reloader=False)

def run_moltbot():
    """Run the Telegram Guardian Agent"""
    logger.info("🦞 [MOLTBOT] Initializing Telegram Guardian...")
    from bankoo_bridge import MoltbotAgent
    try:
        agent = MoltbotAgent()
        agent.run()
    except Exception as e:
        logger.error(f"❌ [MOLTBOT] Critical Failure: {e}")

def cleanup_conflicts():
    """Terminate other python processes to prevent Telegram bot conflicts"""
    import psutil
    curr_pid = os.getpid()
    logger.info("🧹 [CLEANUP] Scanning for conflicting processes...")
    conflicting_pids = []
    
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            info = proc.info
            name = (info.get('name') or "").lower()
            cmdline = " ".join(info.get('cmdline') or []).lower()
            
            if 'python' in name and info['pid'] != curr_pid:
                # Target anything related to bankoo
                if any(x in cmdline for x in ['bankoo', 'moltbot', 'assistant']):
                    conflicting_pids.append(info['pid'])
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    if conflicting_pids:
        logger.info(f"🛑 Found {len(conflicting_pids)} conflicting processes. Terminating...")
        for pid in conflicting_pids:
            try:
                p = psutil.Process(pid)
                p.kill()
            except: pass
        time.sleep(2) # Wait for ports to clear
    else:
        logger.info("✅ No conflicts found.")

def run_moltbot_with_retry():
    """Run Moltbot with auto-restart on conflict/crash"""
    while True:
        logger.info("🦞 [MOLTBOT] Launching Guardian Agent...")
        try:
            from bankoo_bridge import MoltbotAgent
            agent = MoltbotAgent()
            agent.run()
        except Exception as e:
            if "Conflict" in str(e):
                logger.warning("⚠️ [MOLTBOT] Conflict detected! Another instance might be starting. Retrying in 5s...")
                cleanup_conflicts()
            else:
                logger.error(f"❌ [MOLTBOT] Crash: {e}. Restarting...")
            time.sleep(5)

if __name__ == "__main__":
    print("\n" + "="*50)
    print("        🦞 BANKOO AI: ASCENSION CORE (v12) 🦞")
    print("="*50 + "\n")

    # 0. Auto-Cleanup Conflicts
    cleanup_conflicts()

    # 1. Start Flask UI in Thread
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()

    # 2. Wait for system to settle
    time.sleep(2)

    # 3. Start Moltbot (Main Thread / Auto-Restarting)
    run_moltbot_with_retry()
