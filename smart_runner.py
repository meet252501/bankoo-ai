import os
import sys
import subprocess
import threading
import time
import shutil
import json

def install_package(package_name):
    print(f"[SANDBOX] Auto-Installing missing library: {package_name}...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        print(f"SUCCESS: Installed {package_name}")
        return True
    except Exception as e:
        print(f"ERROR: Failed to install {package_name}: {e}")
        return False

try:
    import requests
except ImportError:
    install_package("requests")
    import requests
import shutil

def install_package(package_name):
    print(f"[SANDBOX] Auto-Installing missing library: {package_name}...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        print(f"SUCCESS: Installed {package_name}")
        return True
    except Exception as e:
        print(f"ERROR: Failed to install {package_name}: {e}")
        return False

def extract_imports(code_path):
    with open(code_path, "r", encoding="utf-8") as f:
        try:
            tree = ast.parse(f.read())
        except:
            return []
            
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name.split('.')[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(node.module.split('.')[0])
    return list(set(imports))

def main():
    if len(sys.argv) < 2:
        print("Usage: python smart_runner.py <script_path>")
        sys.exit(1)

    script_path = sys.argv[1]
    ext = os.path.splitext(script_path)[1].lower()
    filename = os.path.basename(script_path)
    
    # 1. PYTHON: Keep existing dependency check
    if ext == '.py':
        required_modules = extract_imports(script_path)
        std_lib = sys.stdlib_module_names if hasattr(sys, 'stdlib_module_names') else []
        for mod in required_modules:
            if mod in std_lib or mod in ['sys', 'os', 'math', 'time', 'json', 'random', 'asyncio']:
                continue
            spec = importlib.util.find_spec(mod)
            if spec is None:
                pkg_map = {'cv2': 'opencv-python', 'PIL': 'Pillow', 'bs4': 'beautifulsoup4', 'sklearn': 'scikit-learn', 'yaml': 'PyYAML'}
                pkg = pkg_map.get(mod, mod)
                install_package(pkg)
        run_cmd = [sys.executable, script_path]

    # 2. UNIVERSAL LANGUAGE MAPPING
    elif ext == '.js':
        run_cmd = ['node', script_path]
    elif ext == '.ts':
        run_cmd = ['ts-node', script_path] # Fallback if ts-node is installed, otherwise suggest tsc
    elif ext == '.go':
        run_cmd = ['go', 'run', script_path]
    elif ext in ['.cpp', '.cc', '.cxx']:
        run_cmd = ['g++', script_path, '-o', 'out.exe']
    elif ext == '.c':
        run_cmd = ['gcc', script_path, '-o', 'out.exe']
    elif ext == '.rs':
        run_cmd = ['rustc', script_path, '-o', 'out.exe']
    elif ext == '.java':
        run_cmd = ['java', script_path]
    elif ext == '.php':
        run_cmd = ['php', script_path]
    elif ext == '.rb':
        run_cmd = ['ruby', script_path]
    elif ext == '.cs':
        run_cmd = ['dotnet', 'run', '--project', script_path] if os.path.isdir(script_path) else ['csc', script_path]
    elif ext == '.sh':
        run_cmd = ['bash', script_path]
    elif ext == '.sql':
        run_cmd = ['sqlite3', ':memory:', f".read {script_path}"]
    else:
        # Fallback to direct execution
        run_cmd = [script_path]

    print(f"[SANDBOX] Executing {filename} ({ext.upper()})...\n" + "="*40)
    
    start_time = time.time()
    try:
        # For compiled languages, we need to compile first
        # For compiled languages, we need to compile first
        if ext in ['.cpp', '.c', '.rs']:
            compiler_exe = run_cmd[0]
            if not shutil.which(compiler_exe):
                raise FileNotFoundError(f"Compiler {compiler_exe} not found in PATH")

            print(f"[SANDBOX] Compiling {filename}...")
            compile_res = subprocess.run(run_cmd, capture_output=True, text=True)
            if compile_res.returncode != 0:
                print("\n[COMPILATION ERROR]:")
                print(compile_res.stderr)
                # AGGRESSIVE FALLBACK: If local compilation fails for ANY reason, try Cloud.
                print("⚠️  Local compilation failed. Attempting Cloud Fallback...")
                raise FileNotFoundError("Compilation failed - triggering Cloud Fallback")
            run_cmd = ['./out.exe'] # Change to run the binary

        process = subprocess.Popen(
            run_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )

        import threading
        def stream_output(pipe, prefix=""):
            for line in iter(pipe.readline, ''):
                print(f"{prefix}{line}", end='', flush=True)
            pipe.close()

        stdout_thread = threading.Thread(target=stream_output, args=(process.stdout,))
        stderr_thread = threading.Thread(target=stream_output, args=(process.stderr, "[STDERR] "))
        stdout_thread.start()
        stderr_thread.start()

        timeout = 60 
        while timeout > 0 and process.poll() is None:
            time.sleep(1)
            timeout -= 1

        if process.poll() is None:
            print("\n[SANDBOX] Terminating process (Timeout)...")
            process.terminate()
        
        stdout_thread.join()
        stderr_thread.join()
            
        if process.returncode == 0:
            print(f"\nSUCCESS: Execution Finished ({round(time.time() - start_time, 2)}s)")
        else:
            print(f"\nERROR: Execution Failed (Exit Code: {process.returncode})")
            
    except Exception as e:
        # Suggest installation if command not found
        if "FileNotFoundError" in str(type(e)):
            print(f"\n⚠️  [LOCAL MISSING] Compiler/Runtime for {ext} not found.")
            print(f"☁️  [CLOUD FALLBACK] Switching to Piston Sandbox...")
            
            # Map extension to Piston language
            lang_map = {
                '.js': 'javascript', '.ts': 'typescript', '.go': 'go',
                '.rs': 'rust', '.cpp': 'c++', '.c': 'c', 
                '.java': 'java', '.cs': 'csharp', '.php': 'php', 
                '.rb': 'ruby', '.sh': 'bash', '.sql': 'sqlite3',
                '.py': 'python'
            }
            piston_lang = lang_map.get(ext, 'python')
            
            try:
                # Read code content
                with open(script_path, 'r', encoding='utf-8') as f:
                    code_content = f.read()
                
                # Cleanup code (remove dependencies block if present)
                code_content = code_content.split("[dependencies]")[0].strip()
                code_content = code_content.split("# --- NEXT BLOCK ---")[0].strip()

                # Define correct filename for Piston (crucial for Java/Rust)
                piston_filename_map = {
                    'rust': 'main.rs', 'java': 'Main.java', 'go': 'main.go',
                    'c++': 'main.cpp', 'c': 'main.c', 'csharp': 'Program.cs',
                    'php': 'index.php', 'javascript': 'index.js', 'typescript': 'index.ts'
                }
                piston_filename = piston_filename_map.get(piston_lang, 'script' + ext)

                payload = {
                    "language": piston_lang,
                    "version": "*",
                    "files": [{"name": piston_filename, "content": code_content}]
                }
                
                if not requests:
                    print("❌ REQUESTS INSTALL FAILED: Cannot fallback to cloud.")
                    sys.exit(1)

                res = requests.post("https://emkc.org/api/v2/piston/execute", json=payload, timeout=20)
                data = res.json()
                
                if 'run' in data:
                    out = data['run'].get('output', '')
                    err = data['run'].get('stderr', '')
                    if out: print(out)
                    if err: print(f"Runtime Error: {err}")
                    
                    # Exit with 0 if no stderr, otherwise 1
                    sys.exit(0 if not err else 1)
                else:
                    print(f"❌ Cloud Error: {data}")
                    sys.exit(1)
                    
            except Exception as cloud_err:
                print(f"❌ Cloud Fallback Failed: {cloud_err}")
                sys.exit(1)
                
        else:
            print(f"\nERROR during execution: {e}")
            sys.exit(1)

    # Propagate exit code
    if 'process' in locals() and process.returncode != 0:
        sys.exit(process.returncode)

if __name__ == "__main__":
    main()
