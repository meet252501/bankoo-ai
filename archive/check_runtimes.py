"""
Bankoo AI - Runtime Environment Checker
Detects which programming languages are installed and ready to use
"""
import subprocess
import sys
import os

def check_command(command, name, version_flag="--version"):
    """Check if a command exists and get its version"""
    try:
        result = subprocess.run(
            [command, version_flag],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            version = result.stdout.split('\n')[0]
            return True, version
        else:
            return False, None
    except (FileNotFoundError, subprocess.TimeoutExpired, Exception):
        return False, None

def main():
    print("=" * 70)
    print(" " * 15 + "BANKOO AI - RUNTIME ENVIRONMENT CHECKER")
    print("=" * 70)
    print()
    
    runtimes = [
        # (command, display_name, version_flag, tier)
        ("python", "Python", "--version", 1),
        ("node", "Node.js (JavaScript)", "--version", 1),
        ("java", "Java (JDK)", "--version", 1),
        ("php", "PHP", "--version", 1),
        ("gcc", "C Compiler (GCC)", "--version", 2),
        ("g++", "C++ Compiler (G++)", "--version", 2),
        ("dotnet", ".NET SDK (C#)", "--version", 2),
        ("go", "Go (Golang)", "version", 2),
        ("rustc", "Rust", "--version", 3),
        ("ruby", "Ruby", "--version", 3),
        ("tsc", "TypeScript", "--version", 3),
        ("bash", "Bash", "--version", 3),
        ("Rscript", "R Programming", "--version", 3),
        ("mysql", "MySQL Client", "--version", 1),
    ]
    
    installed = []
    missing = []
    
    # Define absolute fallback paths for common tools
    fallback_paths = {
        "php": [r"C:\xampp\php\php.exe"],
        "mysql": [r"C:\xampp\mysql\bin\mysql.exe"],
        "java": [r"C:\Program Files\Java\jdk-17\bin\java.exe", r"C:\Program Files\Microsoft\jdk-17.0.13.11-hotspot\bin\java.exe", r"C:\Program Files\Java\jdk-17.0.17\bin\java.exe"],
        "go": [r"C:\Program Files\Go\bin\go.exe", r"C:\Go\bin\go.exe"],
        "node": [r"C:\Program Files\Nodejs\node.exe"],
        "git": [r"C:\Program Files\Git\cmd\git.exe"],
        "bash": [r"C:\Program Files\Git\bin\bash.exe"],
        "ruby": [r"C:\Ruby32-x64\bin\ruby.exe", r"C:\Ruby33-x64\bin\ruby.exe"],
        "rustc": [os.path.expanduser(r"~\.cargo\bin\rustc.exe")],
        "gcc": [r"C:\MinGW\bin\gcc.exe", r"C:\mingw64\bin\gcc.exe", r"C:\TDM-GCC-64\bin\gcc.exe", r"C:\Program Files\LLVM\bin\clang.exe"],
        "g++": [r"C:\MinGW\bin\g++.exe", r"C:\mingw64\bin\g++.exe", r"C:\Program Files\LLVM\bin\clang++.exe"],
        "tsc": [os.path.expanduser(r"~\AppData\Roaming\npm\tsc.cmd")]
    }

    for cmd, name, flag, tier in runtimes:
        is_installed, version = check_command(cmd, name, flag)
        
        # If not found in PATH, check absolute fallbacks
        if not is_installed and cmd in fallback_paths:
            for path in fallback_paths[cmd]:
                if os.path.exists(path):
                    is_installed = True
                    # Try to get version from absolute path
                    ver_ok, ver_str = check_command(path, name, flag)
                    version = ver_str if ver_ok else "(Detected at path)"
                    version += " [Manual]"
                    break

        if is_installed:
            print(f"✅ {name:<25} | {version[:50]}")
            installed.append(name)
        else:
            print(f"❌ {name:<25} | NOT INSTALLED")
            missing.append((name, tier))
    
    print()
    print("=" * 70)
    print(f"SUMMARY: {len(installed)}/{len(runtimes)} runtimes detected")
    print("=" * 70)
    print()
    
    if missing:
        print("📦 MISSING RUNTIMES:\n")
        
        tier1 = [n for n, t in missing if t == 1]
        tier2 = [n for n, t in missing if t == 2]
        tier3 = [n for n, t in missing if t == 3]
        
        if tier1:
            print("🔴 HIGH PRIORITY (Install First):")
            for name in tier1:
                print(f"   - {name}")
            print()
        
        if tier2:
            print("🟡 MEDIUM PRIORITY (Common Use):")
            for name in tier2:
                print(f"   - {name}")
            print()
        
        if tier3:
            print("🟢 LOW PRIORITY (Advanced Features):")
            for name in tier3:
                print(f"   - {name}")
            print()
        
        print("📖 Installation Guide: See RUNTIME_SETUP_GUIDE.md")
    else:
        print("🎉 ALL RUNTIMES INSTALLED! You're ready to code!")
    
    print()
    print("=" * 70)
    
    # Check XAMPP specifically
    print("\n🔍 XAMPP DETECTION:\n")
    
    xampp_paths = [
        r"C:\xampp\php\php.exe",
        r"C:\xampp\mysql\bin\mysql.exe",
        r"C:\xampp\apache\bin\httpd.exe"
    ]
    
    xampp_components = ["PHP", "MySQL", "Apache"]
    
    for path, component in zip(xampp_paths, xampp_components):
        if os.path.exists(path):
            print(f"✅ XAMPP {component:<10} | {path}")
        else:
            print(f"❌ XAMPP {component:<10} | Not found at {path}")
    
    print()
    
    # Check if XAMPP is in PATH
    php_in_path, _ = check_command("php", "PHP", "--version")
    mysql_in_path, _ = check_command("mysql", "MySQL", "--version")
    
    if os.path.exists(r"C:\xampp") and (not php_in_path or not mysql_in_path):
        print("⚠️  WARNING: XAMPP is installed but not in system PATH!")
        print("   Add these to your PATH environment variable:")
        print("   - C:\\xampp\\php")
        print("   - C:\\xampp\\mysql\\bin")
        print("   Then restart your computer.")
    
    print()

if __name__ == "__main__":
    main()
    input("\nPress Enter to exit...")
