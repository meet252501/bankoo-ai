import socket
import psutil
import subprocess
import time
import requests
import os
import sys
import threading

# Native Window Engine
try:
    import webview
except ImportError:
    print("[Setup] Installing Native UI Engine (pywebview)...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pywebview"])
    import webview

# Telegram Bridge Engine
try:
    import telegram
except ImportError:
    print("[Setup] Installing Telegram Bridge Engine (python-telegram-bot)...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "python-telegram-bot"])

# FIX: Force UTF-8 Encoding for Windows Console to prevent crashes
sys.stdout.reconfigure(encoding='utf-8')

def cleanup_port(port):
    """Clean up any process running on the specified port."""
    print(f"[*] [0/3] Scouring port {port} for legacy sessions...")
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            for conn in proc.net_connections(kind='inet'):
                if conn.laddr.port == port:
                    print(f"   - Terminating orphaned process: {proc.info['name']} (PID: {proc.info['pid']})")
                    proc.terminate()
                    proc.wait(timeout=3)
        except:
            pass

def create_desktop_shortcut():
    """Create a professional shortcut on the user's desktop."""
    try:
        desktop = os.path.join(os.environ["USERPROFILE"], "Desktop")
        shortcut_path = os.path.join(desktop, "Bankoo AI.lnk")
        
        print("[+] [Extra] Synthesizing Desktop Shortcut...")
        script_dir = os.path.dirname(os.path.abspath(__file__))
        target = os.path.join(script_dir, "START_BANKOO.bat")
        
        # Use Custom Logo if available
        icon_path = os.path.join(script_dir, "bankoo_icon.ico")
        if os.path.exists(icon_path):
            icon = icon_path
        else:
            icon = sys.executable

        powershell_cmd = f"$s=(New-Object -COM WScript.Shell).CreateShortcut('{shortcut_path}');$s.TargetPath='{target}';$s.WorkingDirectory='{script_dir}';$s.IconLocation='{icon}';$s.Save()"
        subprocess.run(["powershell", "-Command", powershell_cmd], capture_output=True)
        print(f"   [OK] Shortcut updated at: {shortcut_path}")
    except Exception as e:
        print(f"   [!] Shortcut creation failed: {e}")

def run_server():
    """Starts the backend server in a background thread for unified memory access."""
    print("[>>] [1/2] Starting bankoo.ai Native Engine [Unified]...")
    print("[*] Studio Arch: v3.6 Pro [Direct Bridge Mode]")
    try:
        from bankoo_main import run_backend_server
        server_thread = threading.Thread(target=run_backend_server, daemon=True)
        server_thread.start()
        return server_thread
    except Exception as e:
        print("[X] Failed to initialize Brain Thread: " + str(e))
        return None

def start_telegram_bridge():
    """Starts the Telegram Zenith Bridge in a background thread."""
    import config
    if not hasattr(config, "TELEGRAM_BOT_TOKEN") or not config.TELEGRAM_BOT_TOKEN:
        return
        
    print("[>>] [Bridge] Initiating Zenith Telegram Link...")
    def bridge_runner():
        try:
            from bankoo_bridge import BankooTelegramBridge
            bridge = BankooTelegramBridge()
            bridge.run()
        except Exception as e:
            print(f"[!] [Bridge] Link Failure: {e}")

    bridge_thread = threading.Thread(target=bridge_runner, daemon=True)
    bridge_thread.start()
    return bridge_thread

def wait_for_server_ready():
    """Wait until the Flask server is actually responding to requests."""
    print("[...] [Wait] Calibrating Neural Engine...")
    max_wait = 30 
    for i in range(max_wait):
        try:
            r = requests.get("http://127.0.0.1:5001/api/ping", timeout=1)
            if r.status_code == 200:
                print("[OK] Engine Calibration: OPTIMAL")
                return True
        except:
            pass
        time.sleep(1)
    return False

def start_native_ui():
    """Launch the app in its own dedicated window with premium settings."""
    print("[UI]  [2/2] Launching Neural Workspace...")
    
    # Create the window
    window = webview.create_window(
        'Bankoo AI | Neural Workspace', 
        'http://127.0.0.1:5001',
        width=1280,
        height=800,
        min_size=(1000, 700),
        background_color='#050810',
        confirm_close=True
    )
    
    # IMMEDIATE BRIDGE REGISTRATION
    try:
        from bankoo_main import register_native_window
        register_native_window(window)
    except Exception as e:
        print(f"[!] [BRIDGE] Could not link window: {e}")
    
    # Start the engine
    webview.start(private_mode=False, user_agent="BankooDesktop/3.6")

def cleanup_on_exit():
    """Kill all associated processes including self."""
    print("\n[💀] AUTO-KILL: Terminating all Bankoo processes...")
    try:
        # Kill Node (Moltbot remnants)
        subprocess.run("taskkill /F /IM node.exe /T", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Kill Python (Self & Others) - This is the last thing that happens
        # We start a separate detached process to kill python, so this script has time to exit cleanly-ish
        # or we just commit suicide right here.
        subprocess.run("taskkill /F /IM python.exe /T", shell=True) 
    except:
        pass

def main():
    import shutil
    
    os.system('cls' if os.name == 'nt' else 'clear')
    print("="*60)
    print("          BANKOO AI: NEXT-GEN PROFESSIONAL v3.6")
    print("="*60)
    
    # Auto-clear Python cache
    print("[🧹] Clearing Python cache...")
    cache_cleared = 0
    for root, dirs, files in os.walk('.'):
        if '__pycache__' in dirs:
            try:
                shutil.rmtree(os.path.join(root, '__pycache__'))
                cache_cleared += 1
            except:
                pass
    if cache_cleared > 0:
        print(f"   ✓ Cleared {cache_cleared} cache directories\n")
    
    cleanup_port(5001)
    # create_desktop_shortcut()  # Disabled: Manual shortcut already exists
    
    # Start server in thread
    if not run_server():
        return

    # Start Telegram Bridge
    start_telegram_bridge()
        
    if not wait_for_server_ready():
        print("[X] CRITICAL: Engine synchronization failed.")
        return

    try:
        start_native_ui()
    finally:
        print("\n[!] Commencing System Shutdown...")
        cleanup_on_exit()

if __name__ == "__main__":
    main()
