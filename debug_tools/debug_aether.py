import os
import sys
import socket
import subprocess
import time

def check_port(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def check_dependencies():
    print("[1] Checking Dependencies...")
    required = ['flask', 'flask_cors', 'psutil', 'requests']
    missing = []
    for lib in required:
        try:
            __import__(lib.replace('-', '_'))
            print(f"  [OK] {lib}")
        except ImportError:
            print(f"  [!!] Missing {lib}")
            missing.append(lib)
    return missing

def main():
    print("="*60)
    print("  BANKOO AETHER IDE: BACKEND DIAGNOSTIC")
    print("="*60)
    
    # Check Python
    print(f"[0] Python version: {sys.version}")
    
    # Check Dependencies
    missing = check_dependencies()
    if missing:
        print(f"\n[!] Missing libraries detected. Try running:")
        print(f"    pip install {' '.join(missing)}")
        input("\nPress Enter to continue anyway...")

    # Check Port 5001
    port = 5001
    if check_port(port):
        print(f"\n[!] Port {port} is ALREADY IN USE.")
        print("    Please close any other Bankoo windows or existing servers.")
        input("\nPress Enter to continue...")
    else:
        print(f"\n[OK] Port {port} is available.")

    # Try manual start
    print("\n[2] Attempting to start Backend Server (bankoo_main.py)...")
    print("    If it fails, a traceback will appear below.")
    print("-" * 60)
    
    try:
        # We try to import and run directly to see the traceback here
        from bankoo_main import app
        print("  [SUCCESS] Flask app imported correctly.")
        print("  [INFO] Starting app on localhost:5001...")
        app.run(host='127.0.0.1', port=5001, debug=False, threaded=True)
    except Exception as e:
        print("\n" + "!" * 60)
        print("  CRITICAL ERROR DURING STARTUP:")
        print("-" * 60)
        import traceback
        traceback.print_exc()
        print("!" * 60)

    print("\n[DIAGNOSTIC FINISHED]")
    input("Press Enter to close...")

if __name__ == "__main__":
    main()
