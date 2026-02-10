import os
import sys
import subprocess
import time
import platform
import shutil

# --- CONFIGURATION ---
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
LEGACY_DIR = os.path.join(ROOT_DIR, "_legacy_utils")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    clear_screen()
    print("="*60)
    print("      💎 BANKOO AI: SOVEREIGN DESKTOP COMMANDER")
    print("="*60)
    print(f"Working Directory: {ROOT_DIR}")
    print("="*60)

def run_command(command, wait=True):
    print(f"\n[EXEC] {command}...")
    try:
        if wait:
            subprocess.run(command, shell=True, check=False)
            print("\n[DONE] Press Enter to continue...")
            input()
        else:
            subprocess.Popen(command, shell=True)
            print("\n[LAUNCHED] Process started in background.")
            time.sleep(2)
    except Exception as e:
        print(f"\n[ERROR] {e}")
        input("Press Enter to continue...")

def start_bankoo():
    print_header()
    print("🚀 Starting Bankoo AI System...")
    print("   - Backend Port: 5000/5001")
    print("   - Interface: Localhost")
    
    # Check for virtual environment if needed (optional logic here)
    
    # Launch Main
    cmd = f'python "{os.path.join(ROOT_DIR, "bankoo_main.py")}"'
    run_command(cmd, wait=True)

def run_diagnostics():
    print_header()
    print("🔧 Running System Diagnostics...")
    
    scripts = [
        "verify_system_integrity.py",
        "debug_ai.py",
        "check_runtimes.py"
    ]
    
    for script in scripts:
        path = os.path.join(ROOT_DIR, script)
        if os.path.exists(path):
            print(f"\n--- Running {script} ---")
            subprocess.run(f'python "{path}"', shell=True)
        else:
            # Check legacy folder
            legacy_path = os.path.join(LEGACY_DIR, script)
            if os.path.exists(legacy_path):
                print(f"\n--- Running {script} (Legacy) ---")
                subprocess.run(f'python "{legacy_path}"', shell=True)
            else:
                print(f"⚠️ Script not found: {script}")
    
    print("\n[DONE] Diagnostics complete. Press Enter.")
    input()

def install_dependencies():
    print_header()
    print("📦 Dependency Management")
    print("1. Install Python Requirements (pip)")
    print("2. Check/Install System Runtimes (FFmpeg, git, etc.)")
    print("3. Back")
    
    c = input("\nSelect Option: ")
    
    if c == '1':
        cmd = 'pip install -r requirements.txt'
        run_command(cmd)
    elif c == '2':
        # logic or call old script
        cmd = f'python "{os.path.join(ROOT_DIR, "check_runtimes.py")}"'
        run_command(cmd)

def quick_clean():
    print_header()
    print("🧹 Cleaning Temporary Files...")
    
    targets = ['__pycache__', 'logs', 'temp']
    count = 0
    for t in targets:
        path = os.path.join(ROOT_DIR, t)
        if os.path.exists(path) and os.path.isdir(path):
            try:
                # Don't delete logs folder itself, just content? or skip logs
                if t == 'logs': continue 
                shutil.rmtree(path)
                print(f"   - Removed {t}")
                count += 1
            except:
                print(f"   - Failed to remove {t}")
    
    print(f"\nCleaned {count} items.")
    time.sleep(1)

def main_menu():
    while True:
        print_header()
        print("1. 🚀 Start Bankoo AI (Main)")
        print("2. 🔧 Run Diagnostics")
        print("3. 📦 Install/Updates")
        print("4. 🧹 Clean Temp Files")
        print("5. ❌ Exit")
        print("-" * 60)
        
        choice = input("Select Option [1-5]: ")
        
        if choice == '1': start_bankoo()
        elif choice == '2': run_diagnostics()
        elif choice == '3': install_dependencies()
        elif choice == '4': quick_clean()
        elif choice == '5': sys.exit()

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\nGoodbye!")
