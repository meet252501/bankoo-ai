import os
import sys
import threading
import time
import base64
import webbrowser
import webview
import subprocess

def auto_install(package):
    print(f"📦 [AUTO-INSTALL] Missing dependency: {package}. Initializing fix...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

try:
    from flask import Flask, jsonify, request, send_from_directory
except ImportError:
    auto_install('flask')
    from flask import Flask, jsonify, request, send_from_directory

try:
    from flask_cors import CORS
except ImportError:
    auto_install('flask-cors')
    from flask_cors import CORS

import config
from assistant import DesktopAssistant
from api_hub import doc_brain, analytics_brain
from airllm_brain import air_brain
from scraper_brain import ScraperBrain

# New Advanced Features
try:
    from bankoo_memory import memory
    MEMORY_AVAILABLE = True
    print("✅ [MEMORY] Persistent memory system loaded")
except Exception as e:
    MEMORY_AVAILABLE = False
    print(f"⚠️ [MEMORY] Not available: {e}")

try:
    from browser_skill import browser_skill
    BROWSER_AVAILABLE = True
    print("✅ [BROWSER] Browser automation loaded")
except Exception as e:
    BROWSER_AVAILABLE = False
    print(f"⚠️ [BROWSER] Not available: {e}")

try:
    from skill_manager import skill_manager
    SKILLS_AVAILABLE = True
    print("✅ [SKILLS] Skill system loaded")
except Exception as e:
    SKILLS_AVAILABLE = False
    print(f"⚠️ [SKILLS] Not available: {e}")
from brain_dashboard import BrainDashboard

# Initialize Scraper
scraper = ScraperBrain()
dashboard_engine = BrainDashboard()

# Initialize Nexus (Agent Hub)
try:
    from agent_nexus import nexus
    NEXUS_AVAILABLE = True
    print("✅ [NEXUS] Enterprise Agent Council loaded")
except Exception as e:
    NEXUS_AVAILABLE = False
    print(f"⚠️ [NEXUS] Not available: {e}")

app = Flask(__name__, static_folder=".")
CORS(app)

# Silence Flask Access Logs (Heartbeat Spam)
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
logging.getLogger('httpx').setLevel(logging.WARNING) # Silence Telegram Polling

# 🚀 INSTANT BOOT: Lazy Assistant Loading
assistant = None
brain_ready = False

def delayed_init():
    global assistant, brain_ready
    try:
        print("🧠 [SYSTEM] Deep-Loading Neural Brain in background...")
        from assistant import DesktopAssistant
        assistant = DesktopAssistant()
        
        # 🔗 SYNC: Register Bridges after Brain is Online
        assistant.output_callback = on_brain_text
        assistant.audio_callback = on_brain_audio
        assistant.ui_callback = on_ui_cmd
        
        # 🛡️ START BUTLER: (v19 Grand Finale feature)
        assistant.start_butler()
        
        # Sync with Document/Other Managers if needed
        
        
        brain_ready = True
        print("✅ [SYSTEM] Neural Brain ONLINE & Connected")
    except Exception as e:
        print(f"❌ [CORE] Brain Failure: {e}")

threading.Thread(target=delayed_init, daemon=True).start()

# Zenith Multi-Agent Bridge State
message_queue = []
queue_lock = threading.Lock()
native_window = None # Global reference for PyWebView bridge

# --- YOUTUBE ANALYSIS STATE (Managed by YouTubeJobManager) ---
# Legacy globals removed.


# --- CALLBACK REGISTRATION ---
def on_brain_text(text, is_ide=False, source="internal"):
    if text is None: text = "" # Prevent crash on empty response
    try:
        print(f"DEBUG: on_brain_text called. text='{text[:20]}...', is_ide={is_ide}")
    except:
        pass
    with queue_lock:
        m_type = "ide_msg" if is_ide else "msg"
        message_queue.append({
            "type": m_type, 
            "role": "BOT", 
            "content": text, 
            "source": source,
            "timestamp": time.time()
        })

def on_brain_audio(b64, is_ide=False):
    with queue_lock:
        a_type = "ide_audio" if is_ide else "audio"
        message_queue.append({"type": a_type, "content": b64, "timestamp": time.time()})

def on_ui_cmd(type, **kwargs):
    with queue_lock:
        payload = {"type": type}
        payload.update(kwargs)
        payload["timestamp"] = time.time()
        message_queue.append(payload)

def on_user_text(text, source="mic"):
    """Helper to push user messages to the UI queue."""
    with queue_lock:
        message_queue.append({
            "type": "msg", 
            "role": "USER", 
            "content": text, 
            "source": source,
            "timestamp": time.time()
        })

# --- API ACTIVITY LOGGING ---
@app.route('/api/bridge/telegram', methods=['POST'])
def bridge_telegram():
    data = request.json
    text = data.get('message', '')
    
    if not text:
        return jsonify({"error": "No message provided"}), 400
        
    print(f"🤖 [TELEGRAM BRIDGE] Received: {text[:80]}...")
    
    if assistant:
        response = assistant.ask_ai(text)
        if response is None: response = "⚠️ AI Brain Malfunction (No Response)"
        
        # --- MEDIA RETURN LOGIC ---
        media_path = None
        media_type = None
        
        if "SCREENSHOT_CAPTURED::" in response:
            try:
                # Format: SCREENSHOT_CAPTURED::path::message
                parts = response.split("::")
                media_path = parts[1]
                response = parts[2] # The user-friendly message
                media_type = "image"
            except:
                pass
                
        on_brain_text(response, source="telegram")
        
        return jsonify({
            "status": "processed", 
            "response": response,
            "media_path": media_path,
            "media_type": media_type
        })
    else:
        return jsonify({"status": "error", "message": "Brain not ready"}), 503

@app.route('/api/ping', methods=['GET'])
def ping():
    if not brain_ready:
        return jsonify({"status": "loading"}), 202
    return jsonify({"status": "ready"})

@app.route('/api/zenith/generate', methods=['POST'])
def generate_zenith_dashboard():
    try:
        dashboard_engine.generate_report()
        return jsonify({"status": "success", "file": "logs/brain_dashboard.html"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/zenith/mistakes', methods=['GET'])
def get_zenith_mistakes():
    try:
        import glob
        import json
        traces = []
        files = glob.glob("logs/traces/*.jsonl")
        for file in files:
            with open(file, "r", encoding="utf-8") as f:
                for line in f:
                    try:
                        traces.append(json.loads(line))
                    except: continue
        
        traces.sort(key=lambda x: x["timestamp"])
        mistakes = [t for t in traces if t.get("reward", 0) < 0][-5:]
        
        formatted = []
        for m in mistakes:
            user_input = m["messages"][1]["content"] if len(m["messages"]) > 1 else "Unknown"
            bad_ans = m["messages"][2]["content"] if len(m["messages"]) > 2 else "Empty"
            # Try to find a fix
            fix = next((t for t in traces if t.get("reward", 0) > 0 and t["timestamp"] > m["timestamp"] and t["messages"][1]["content"] == user_input), None)
            
            formatted.append({
                "id": m["timestamp"],
                "input": user_input,
                "mistake": bad_ans,
                "fix": fix["messages"][2]["content"] if fix else None,
                "status": "Fixed" if fix else "Pending"
            })
            
        return jsonify(formatted[::-1]) # Newest first
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.before_request
def log_request():
    if request.path.startswith('/api/') and request.path != '/api/get_updates':
        print(f"📨 [API IN] {request.method} {request.path}")
        # Only check JSON for methods that typically send JSON bodies
        if request.method in ['POST', 'PUT', 'PATCH'] and request.is_json:
            try:
                print(f"   Data: {str(request.json)[:100]}...")
            except:
                pass  # Ignore JSON parsing errors

@app.after_request
def log_response(response):
    if request.path.startswith('/api/') and request.path != '/api/get_updates':
        print(f"📤 [API OUT] {request.path} → Status {response.status_code}")
    return response

# --- FLASK ENDPOINTS ---
@app.route('/')
def index(): 
    return send_from_directory('.', 'bankoo_ui.html')


@app.route('/smart_notes_v3.js')
def serve_notes_js():
    return send_from_directory('.', 'smart_notes_v3.js', mimetype='application/javascript')

@app.route('/scraper')
def serve_scraper():
    return send_from_directory('.', 'web_scraper_advanced.html')

@app.route('/web_scraper.js')
def serve_scraper_js():
    return send_from_directory('.', 'web_scraper.js', mimetype='application/javascript')

# NEW: Serve Scraper UI for iframe integration
@app.route('/scraper')
def serve_scraper_ui():
    return send_from_directory('.', 'web_scraper_advanced.html')

@app.route('/ide')
def serve_ide():
    """Serves the Master IDE interface"""
    return send_from_directory('.', 'bankoo_ide.html')

@app.route('/api/get_updates')
def get_updates():
    with queue_lock:
        if message_queue:
            cmds = [m for m in message_queue if m.get('type') == 'ui_cmd']
            if cmds:
                print(f"🚀 [DISPATCH] Sending commands: {[c['cmd'] for c in cmds]}")
        
        updates = list(message_queue)
        message_queue.clear()
        return jsonify(updates)

@app.route('/api/send_input', methods=['POST'])
def flask_input():
    data = request.json
    text = data.get('text', '')
    if text:
        print(f"💬 [USER INPUT] {text[:80]}...")
        
        if assistant:
            print("🤖 [AI PROCESSING] Starting inference thread...")
            try:
                threading.Thread(target=assistant.ask_ai, args=(text,), daemon=True).start()
                print("✅ [THREAD] Thread launched.")
            except Exception as e:
                print(f"❌ [THREAD ERROR] Could not start thread: {e}")
        else:
            print("⏳ [SYSTEM] Input received while brain is still loading.")
            with queue_lock:
                message_queue.append({
                    "type": "msg", 
                    "role": "BOT", 
                    "content": "I am just waking up! 🧠 Give me 5 more seconds to initialize my neural pathways, then ask me again.",
                    "timestamp": time.time()
                })
    return jsonify({"status": "received"})

@app.route('/api/send_ide_input', methods=['POST'])
def flask_ide_input():
    """IDE Studio Input - Always routes to coding context"""
    print(f"📨 [API IN] POST /api/send_ide_input")
    data = request.json
    text = data.get('text', '')
    if text:
        print(f"💻 [IDE INPUT] {text[:80]}...")
        
        if assistant:
            print("🤖 [AI PROCESSING] Starting IDE inference thread...")
            try:
                # Force IDE context
                threading.Thread(target=assistant.ask_ai, args=(text,), kwargs={"context": "ide"}, daemon=True).start()
                print("✅ [THREAD] IDE Thread launched.")
            except Exception as e:
                print(f"❌ [THREAD ERROR] Could not start IDE thread: {e}")
        else:
            print("⌛ [SYSTEM] IDE input received while brain is still loading.")
            with queue_lock:
                message_queue.append({
                    "type": "ide_msg", 
                    "role": "BOT", 
                    "content": "IDE is initializing... Please wait.",
                    "timestamp": time.time()
                })
    print(f"📤 [API OUT] /api/send_ide_input → Status 200")
    return jsonify({"status": "received"})

@app.route('/api/run_code', methods=['POST'])
def run_code_endpoint():
    """Direct Code Execution Endpoint for Studio"""
    data = request.json
    code = data.get('code', '')
    lang = data.get('lang', 'python')
    stdin = data.get('stdin', '')

    print(f"⚡ [EXEC] Running {lang} code...")

    if lang == 'python':
        try:
            # Create a temp runner script
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
                f.write(code)
                temp_path = f.name
            
            # Run via subprocess
            cmd = [sys.executable, temp_path]
            process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate(input=stdin, timeout=10) # 10s timeout
            
            os.remove(temp_path)
            
            return jsonify({
                "output": stdout + stderr,
                "status": "success" if process.returncode == 0 else "error"
            })
        except Exception as e:
            return jsonify({"output": f"Execution Error: {e}", "status": "error"})
    
    return jsonify({"output": f"Language '{lang}' execution not supported yet.", "status": "error"})

# --- NEW: BANKOO AETHER BRIDGE ---
@app.route('/api/ide/ask', methods=['POST'])
def ide_ask():
    """Direct Request-Response for AETHER Mode (Better API Experience)"""
    data = request.json
    text = data.get('text', '')
    
    if not brain_ready or not assistant:
        return jsonify({"answer": "Brain still loading...", "code": ""}), 503
        
    print(f"✨ [AETHER COMMAND] {text[:50]}...")
    
    # We call assistant.ask_ai synchronously here for the 'Better API' experience
    # Since ask_ai is designed to return the text, we can use it directly.
    # Note: This might block for a while, but for IDE tasks, it's often preferred over polling.
    response = assistant.ask_ai(text)
    
    # Extract Agentic Metadata
    import re
    
    # 🔗 Target File Detection (e.g., "TARGET_FILE: index.html")
    target_file_match = re.search(r"TARGET_FILE:\s*([a-zA-Z0-9_\-\.]+)", response)
    target_file = target_file_match.group(1).strip() if target_file_match else ""

    # 🛠️ Action Detection (e.g., "ACTION: RUN_SYSTEM")
    action_match = re.search(r"ACTION:\s*([A-Z_]+)", response)
    action = action_match.group(1).strip() if action_match else ""

    # 💻 Code Block Extraction (supports multiple, but takes first for editor injection)
    code_match = re.search(r"```(?:\w+)?\n([\s\S]*?)```", response)
    code = code_match.group(1).strip() if code_match else ""
    
    # Extract Clean Answer
    answer = re.sub(r"```(?:\w+)?\n([\s\S]*?)```", "", response).strip()
    answer = re.sub(r"TARGET_FILE:.*", "", answer).strip()
    answer = re.sub(r"ACTION:.*", "", answer).strip()
    answer = answer.replace("[CODE_MODE_ACTIVATED]", "").strip()
    
    # 🧬 Agentic Persistence: If AI suggests a target file, ensure it exists if requested
    if target_file and code:
         print(f"🧬 [AGENTIC] AI suggested target file: {target_file}")

    return jsonify({
        "answer": answer,
        "code": code,
        "target_file": target_file,
        "action": action,
        "raw": response
    })

@app.route('/api/ide/debate', methods=['POST'])
def ide_debate():
    """Triggers the AI Council Boardroom for a high-fidelity refactor/debate"""
    data = request.json
    query = data.get('text', '')
    
    if not brain_ready:
        return jsonify({"error": "Brain loading..."}), 503
        
    print(f"🏛️ [COUNCIL DEBATE] Starting session: {query[:50]}...")
    
    # We use a custom response wrapper to capture the debate phases
    # In a real streaming app, we'd use Server-Sent Events (SSE)
    # For now, we'll return the final result and the debate phases
    from ai_council import council
    result = council.debate(query)
    
    # Send result to UI history
    on_brain_text(result, is_ide=True)
    
    # Return structured result for the IDE
    return jsonify({
        "status": "success",
        "result": result
    })

@app.route('/api/ide/sync_ai', methods=['POST'])
def ide_sync_ai():
    """Initializes AirLLM Local Brain"""
    print("🛰️ [AirLLM] Sync Request Received...")
    success = air_brain.initialize_model()
    if success:
        return jsonify({"status": "success"})
    else:
        return jsonify({"status": "error", "message": "AirLLM engine failed to start. Check terminal."}), 500

@app.route('/api/ide/ghost_complete', methods=['POST'])
def ghost_complete():
    """Fast-lane endpoint for inline code completion"""
    data = request.json
    context = data.get('context', '')
    language = data.get('language', 'python')
    
    # Lazy Init the GhostPilot
    if assistant and not hasattr(assistant, 'ghost_pilot'):
        from assistant import GhostPilot
        assistant.ghost_pilot = GhostPilot(assistant.client)
    
    if assistant and hasattr(assistant, 'ghost_pilot'):
        completion = assistant.ghost_pilot.complete(context, language)
        # Filter markdown checks just in case
        completion = completion.replace("```python", "").replace("```", "").strip()
        return jsonify({"completion": completion})
        
    return jsonify({"completion": ""})

@app.route('/api/ide/save', methods=['POST'])
def ide_save():
    data = request.json
    filename = data.get('filename', 'untitled.py')
    code = data.get('code', '')
    
    try:
        # Save to current workspace
        filepath = os.path.join(os.getcwd(), filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(code)
        print(f"💾 [IDE SAVE] {filename}")
        return jsonify({"status": "success", "path": filepath})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/ide/files', methods=['GET'])
def ide_list_files():
    """List project files (Python, Rust, JS, MD, JSON)"""
    try:
        allowed_exts = {'.py', '.rs', '.js', '.md', '.json', '.html', '.css', '.bat'}
        files = []
        for f in os.listdir(os.getcwd()):
            if os.path.isfile(f) and any(f.endswith(ext) for ext in allowed_exts):
                files.append(f)
        return jsonify({"files": sorted(files)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/ide/read_file', methods=['POST'])
def ide_read_file():
    data = request.json
    filename = data.get('filename')
    if not filename: return jsonify({"error": "No filename"}), 400
    
    try:
        file_path = os.path.join(os.getcwd(), filename)
        if not os.path.exists(file_path):
            return jsonify({"error": "File not found"}), 404
            
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return jsonify({"content": content, "filename": filename})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/debug_code', methods=['POST'])
def debug_code():
    data = request.json
    code = data.get('code', '')
    error = data.get('error', '')
    lang = data.get('lang', 'python')
    
    if not assistant:
        return jsonify({"error": "Brain loading..."}), 503
        
    print(f"🐞 [DEBUG REQUEST] Analyzing {lang} snippet...")
    result = assistant.debug_code(code, error, lang)
    
    # Send result to UI history/sidebar as well
    on_brain_text(result, is_ide=True)
    
    return jsonify({"status": "success", "analysis": result})

@app.route('/api/voice_input', methods=['POST'])
def flask_voice():
    data = request.json
    b64 = data.get('audio', '')
    mode = data.get('mode', 'chat')
    lang = data.get('lang', 'python')
    source = data.get('source', 'mic')
    user = data.get('user', 'User')

    if b64:
        if "base64," in b64:
            b64 = b64.split("base64,")[1]
        
        try:
            if mode == "ide":
                with queue_lock:
                    message_queue.append({"type": "ide_msg", "role": "USER", "content": "(Voice Studio Input)", "timestamp": time.time()})
            elif source == 'telegram':
                 # Push visual indicator of Voice Note
                 on_user_text("[🎤 Voice Note Processing...]", source=f"telegram ({user})")

            audio_bytes = base64.b64decode(b64)
            # Pass SOURCE extracted from payload (e.g. 'telegram')
            threading.Thread(target=assistant.process_mobile_audio, args=(audio_bytes, mode, lang, source), daemon=True).start()
        except Exception as e:
            print(f"Audio Decode Error: {e}")
            
    return jsonify({"status": "processing"})

@app.route('/api/vision/upload_telegram', methods=['POST'])
def flask_vision_telegram():
    """Handle images sent from Telegram"""
    try:
        data = request.json
        b64_img = data.get('image', '')
        user = data.get('user', 'User')
        
        if not b64_img:
            return jsonify({"status": "error", "response": "No image data"}), 400
            
        print(f"👁️ [VISION] Analyzing Telegram Image from {user}...")
        
        # Notify UI
        on_user_text("[🖼️ Image Analysis]", source=f"telegram ({user})")
        
        # Save temp file for analysis
        import uuid
        temp_filename = f"telegram_vision_{uuid.uuid4().hex[:6]}.jpg"
        temp_path = os.path.join(os.getcwd(), temp_filename)
        
        with open(temp_path, "wb") as f:
            f.write(base64.b64decode(b64_img))
            
        # Use Hub to process
        from api_hub import hub
        analysis = hub.tag_image(f"file:///{temp_path}") # Use local file URI logic if supported, or adapt 
        
        # If hub.tag_image expects a URL, we might need a different method or just use the assistant's vision capability directly
        # Let's use simple assistant vision flow:
        # Actually, let's just ask the assistant about the image
        
        # Clean up
        if os.path.exists(temp_path):
            os.remove(temp_path)
            
        return jsonify({"status": "success", "response": f"analysis: {analysis}"})
        
    except Exception as e:
        print(f"❌ Vision Error: {e}")
        return jsonify({"status": "error", "response": "I couldn't analyze that image."}), 500

@app.route('/api/voice/toggle', methods=['POST'])
def flask_voice_toggle():
    """External trigger for Voice UI (e.g. from Vision Lab)"""
    data = request.json
    active = data.get('active', False)
    
    # PATH A: Direct Native Injection (Zero Latency)
    global native_window
    if native_window:
        try:
            cmd = f"toggleVoice({'true' if active else 'false'})"
            native_window.evaluate_js(cmd)
            print(f"🚀 [BRIDGE] Instant UI Trigger: {cmd}")
        except Exception as e:
            print(f"⚠️ [BRIDGE] Direct injection failed: {e}")

    # PATH B: Queue System (Reliability Fallback)
    cmd_type = "voice_start" if active else "voice_stop"
    with queue_lock:
        message_queue.append({
            "type": "ui_cmd", 
            "cmd": cmd_type, 
            "content": f"External Trigger: {active}",
            "timestamp": time.time()
        })
    
    return jsonify({"status": "success", "mode": "native" if native_window else "polling"})

@app.route('/api/upload_pdf', methods=['POST'])
def upload_pdf():
    """Endpoint for Doc-Genius PDF uploads."""
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
        
    if file and file.filename.endswith('.pdf'):
        # Ensure a storage directory exists
        upload_dir = os.path.join(os.getcwd(), "knowledge_base")
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
            
        file_path = os.path.join(upload_dir, file.filename)
        file.save(file_path)
        
        # Process with Doc-Genius RAG Engine
        print(f"📥 [PDF UPLOAD] Received {file.filename}. Processing...")
        result_msg = doc_brain.load_pdf(file_path)
        
        if "Success" in result_msg:
            # Notify UI of status
            with queue_lock:
                message_queue.append({
                    "type": "sys", 
                    "content": f"✅ Document Active: {file.filename}", 
                    "timestamp": time.time()
                })
            return jsonify({"status": "success", "message": result_msg})
        else:
            return jsonify({"status": "error", "message": result_msg}), 500
            
    return jsonify({"error": "Invalid file type. Only PDFs allowed."}), 400

@app.route('/api/upload_dataset', methods=['POST'])
def upload_dataset():
    """Endpoint for Zenith Analytics Hub CSV uploads."""
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
        
    if file and file.filename.endswith('.csv'):
        # Ensure a data directory exists
        data_dir = os.path.join(os.getcwd(), "data_hub")
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
            
        file_path = os.path.join(data_dir, file.filename)
        file.save(file_path)
        
        # Process with Zenith Analytics Engine
        print(f"📥 [DATA UPLOAD] Received {file.filename}. Analyzing...")
        result_msg = analytics_brain.load_dataset(file_path)
        
        if "Success" in result_msg:
            with queue_lock:
                message_queue.append({
                    "type": "sys", 
                    "content": f"📊 Dataset Analyzed: {file.filename}", 
                    "timestamp": time.time()
                })
            return jsonify({"status": "success", "message": result_msg})
        else:
            return jsonify({"status": "error", "message": result_msg}), 500
            
    return jsonify({"error": "Invalid file type. Only CSV allowed."}), 400

# --- MARKET INTELLIGENCE ENDPOINTS ---
from api_hub import market_brain

@app.route('/api/market/stock_summary', methods=['POST'])
def get_stock_summary():
    data = request.json
    symbol = data.get('symbol', 'AAPL')
    print(f"📈 [MARKET] Fetching summary for {symbol}...")
    res = market_brain.get_stock_summary(symbol)
    return jsonify(res)

@app.route('/api/market/financials', methods=['POST'])
def get_financials():
    data = request.json
    symbol = data.get('symbol', 'AAPL')
    rtype = data.get('type', 'income')
    print(f"📈 [MARKET] Fetching {rtype} for {symbol}...")
    res = market_brain.get_financials(symbol, rtype)
    return jsonify(res)

@app.route('/api/market/analyst_recs', methods=['POST'])
def get_analyst_recs():
    data = request.json
    symbol = data.get('symbol', 'AAPL')
    print(f"📈 [MARKET] Fetching recommendations for {symbol}...")
    res = market_brain.get_analyst_recommendations(symbol)
    return jsonify(res)

# --- MOVIE SEARCH ENDPOINT ---
from api_hub import movie_brain

@app.route('/api/movies/search', methods=['POST'])
def search_movies():
    data = request.json
    query = data.get('query', '')
    print(f"🎬 [MOVIES] Searching for: {query}...")
    res = movie_brain.find_movie(query)
    # If the response is a string (markdown), return it wrapped
    if isinstance(res, str):
        return jsonify({"results": res})
    return jsonify(res)

# --- ASSET DESIGNER ENDPOINT ---
from api_hub import creative_brain

@app.route('/api/generate_asset', methods=['POST'])
def generate_asset():
    data = request.json
    prompt = data.get('prompt', 'A futuristic logo')
    style = data.get('style', 'futuristic neon')
    provider = data.get('provider', 'auto')
    print(f"🎨 [DESIGNER] Generating asset: {prompt} ({style}) via {provider}...")
    res = creative_brain.generate_creative_asset(prompt, style, provider)
    return jsonify(res)

# --- AGENT NEXUS ENDPOINT ---
@app.route('/api/nexus/chat', methods=['POST'])
def nexus_chat():
    data = request.json
    agent = data.get('agent', '') # 'architect', 'vc', 'coder'
    query = data.get('query', '')
    
    if not NEXUS_AVAILABLE:
        return jsonify({"response": "⚠️ Agent Nexus is offline (Backend Error)."}), 503
        
    print(f"🧠 [NEXUS] {agent.upper()} Query: {query[:50]}...")
    
    # Run in thread if needed, but Agno might conflict with Flask memory if not careful.
    # For now, synchronous call to ensure answer is returned immediately.
    # If slow, we might need async, but let's keep it simple for now.
    response = nexus.ask_agent(agent, query)
    return jsonify({"response": response})



@app.route('/api/run_code', methods=['POST'])
def flask_run_code():
    data = request.json
    code = data.get('code', '')
    lang = data.get('lang', 'python')
    stdin = data.get('stdin', '')

    wait_for_result = data.get('wait', False)

    if code:
        # Define execution logic
        def get_result():
             if not wait_for_result:
                 on_ui_cmd("ui_cmd", cmd="console_log", content=f"Initializing Native Sandbox for {lang}...", log_type="sys")
                 if stdin:
                     on_ui_cmd("ui_cmd", cmd="console_log", content=f"Input provided: {stdin}", log_type="sys")
             
             return assistant.run_piston_code(code, lang, stdin)

        if wait_for_result:
             # Synchronous Execution for Test Suite
             res = get_result()
             return jsonify(res)
        else:
             # Asynchronous Execution for UI (Non-blocking)
             def _async_exec():
                 res = get_result()
                 l_type = "success" if res['success'] else "err"
                 on_ui_cmd("ui_cmd", cmd="console_log", content=res['output'], log_type=l_type)
             
             threading.Thread(target=_async_exec, daemon=True).start()
             return jsonify({"status": "executing"})
             
    return jsonify({"status": "no_code"})



@app.route('/api/session/reset', methods=['POST'])
def flask_session_reset():
    if not assistant: return jsonify({"error": "AI not online"}), 500
    msg = assistant.reset_session()
    return jsonify({"status": "cleared", "message": msg})

@app.route('/api/vision/launch', methods=['POST'])
def launch_vision_lab():
    """Launches the Vision Lab in a separate process"""
    try:
        print("👁️ [VISION LAB] Launching standalone Vision window...")
        batch_file = os.path.join(os.getcwd(), "LAUNCH_VISION_LAB.bat")
        
        if not os.path.exists(batch_file):
            return jsonify({"status": "error", "message": "Vision Lab batch file not found"}), 404
        
        # Launch the batch file in a new process
        import subprocess
        subprocess.Popen([batch_file], shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)
        
        return jsonify({"status": "success", "message": "Vision Lab window launching..."})
    except Exception as e:
        print(f"❌ Vision Lab launch error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/moltbot/launch', methods=['POST'])
def launch_moltbot_nexus():
    """Launches the Moltbot/Zenith Bridge universal script"""
    try:
        print("🦞 [MOLTBOT NEXUS] Triggering Universal Bridge... (DISABLED to prevent conflict)")
        # batch_file = os.path.join(os.getcwd(), "START_BANKOO_ZENITH.bat")
        # subprocess.Popen([batch_file], shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)
        return jsonify({"status": "disabled", "message": "Zenith Bridge Disabled (ClawdBot Active)"})
    except Exception as e:
        print(f"❌ Moltbot Nexus launch error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/hooks/agent', methods=['POST'])
def moltbot_webhook():
    """Unified Moltbot Gateway - Receives messages from ANY platform"""
    try:
        data = request.json
        print(f"🦞 [MOLTBOT WEBHOOK] Received: {data}")
        
        # Extract message and metadata
        message = data.get('message', data.get('text', ''))
        channel = data.get('channel', 'unknown')  # telegram/discord/slack/whatsapp
        user_data = data.get('from', {})
        user = user_data.get('username', user_data.get('name', 'User'))
        
        if not message:
            return jsonify({"error": "No message"}), 400
        
        print(f"💬 [MOLTBOT → BANKOO] [{channel}] {user}: {message[:50]}...")
        
        # Route to Bankoo Brain
        if assistant and brain_ready:
            # Use threading to avoid blocking
            def process_and_respond():
                response = assistant.ask_ai(message)
                print(f"✅ [BANKOO → MOLTBOT] Response ready ({len(response)} chars)")
                
                # Send back to Moltbot for delivery
                # Moltbot will handle sending to the correct platform
                return response
            
            response = process_and_respond()
            
            return jsonify({
                "response": response,
                "deliver": True,  # Tell Moltbot to send it
                "channel": channel
            })
        else:
            return jsonify({
                "response": "⏳ Bankoo Brain is still initializing...",
                "deliver": True
            })
            
    except Exception as e:
        print(f"❌ [MOLTBOT WEBHOOK] Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/github/push', methods=['POST'])
def flask_github_push():
    if not assistant: return jsonify({"success": False, "error": "AI not online"}), 500
    data = request.json
    repo_name = data.get('repo_name', 'Bankoo-Project')
    code = data.get('code', '')
    filename = data.get('filename', 'main.py')
    commit_msg = data.get('commit_msg', 'Pushed from Bankoo.ai')
    pat = data.get('pat', '')

    if not pat:
         return jsonify({"success": False, "error": "GitHub Personal Access Token (PAT) is required."}), 400
    
    res = assistant.push_to_github(repo_name, code, filename, commit_msg, pat)
    return jsonify(res)

# --- PYTHON REPL ENDPOINTS ---
from repl_manager import repl_manager

@app.route('/api/repl/execute', methods=['POST'])
def flask_repl_execute():
    """Execute a line in the Python REPL"""
    data = request.json
    code = data.get('code', '')
    session_id = data.get('session_id', 'default')
    
    if not code:
        return jsonify({"error": "No code provided"}), 400
    
    try:
        repl = repl_manager.get_session(session_id)
        result = repl.execute_line(code)
        return jsonify(result)
    except Exception as e:
        return jsonify({
            "output": "",
            "error": str(e),
            "prompt": ">>> ",
            "success": False
        })

@app.route('/api/repl/reset', methods=['POST'])
def flask_repl_reset():
    """Reset a REPL session"""
    data = request.json
    session_id = data.get('session_id', 'default')
    
    try:
        repl_manager.reset_session(session_id)
        return jsonify({"status": "reset", "session_id": session_id})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/repl/sessions', methods=['GET'])
def flask_repl_sessions():
    """List all active REPL sessions"""
    try:
        sessions = repl_manager.list_sessions()
        return jsonify({"sessions": sessions})
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route('/api/system/stats', methods=['GET'])
def get_system_stats():
    """Real-time system monitoring stats"""
    try:
        import psutil
        import platform
        
        # CPU
        cpu_percent = psutil.cpu_percent(interval=0.1)
        cpu_freq = psutil.cpu_freq()
        
        # RAM
        ram = psutil.virtual_memory()
        ram_used_gb = ram.used / (1024**3)
        ram_total_gb = ram.total / (1024**3)
        
        # Disk
        disks = []
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disks.append({
                    "name": partition.device,
                    "mountpoint": partition.mountpoint,
                    "total_gb": usage.total / (1024**3),
                    "used_gb": usage.used / (1024**3),
                    "free_gb": usage.free / (1024**3),
                    "percent": usage.percent
                })
            except:
                pass
        
        # Network
        net_io = psutil.net_io_counters()
        
        return jsonify({
            "cpu": {
                "percent": round(cpu_percent, 1),
                "freq_mhz": round(cpu_freq.current, 0) if cpu_freq else 0,
                "cores": psutil.cpu_count()
            },
            "ram": {
                "used_gb": round(ram_used_gb, 2),
                "total_gb": round(ram_total_gb, 2),
                "percent": round(ram.percent, 1)
            },
            "disks": disks,
            "network": {
                "bytes_sent": net_io.bytes_sent,
                "bytes_recv": net_io.bytes_recv,
                "packets_sent": net_io.packets_sent,
                "packets_recv": net_io.packets_recv
            },
            "system": {
                "platform": platform.system(),
                "release": platform.release()
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# --- SMART NOTES 3.0 ENGINE (REBUILT) ---
from smart_notes_3 import notes_engine_v3

@app.route('/api/notes/v3/all', methods=['GET'])
def notes_v3_all():
    return jsonify(notes_engine_v3.get_all())

@app.route('/api/notes/v3/create', methods=['POST'])
def notes_v3_create():
    d = request.json
    print(f"📝 [NOTES V3] Creating: {d.get('title')}")
    note = notes_engine_v3.create_note(
        d.get('title', 'New Note'),
        d.get('content', ''),
        d.get('folderId', 'f_default'),
        d.get('language', 'english')
    )
    return jsonify(note)

@app.route('/api/notes/v3/update/<id>', methods=['PUT'])
def notes_v3_update(id):
    note = notes_engine_v3.update_note(id, request.json)
    return jsonify(note) if note else (jsonify({"error": "Note not found"}), 404)

@app.route('/api/notes/v3/delete/<id>', methods=['DELETE'])
def notes_v3_delete(id):
    success = notes_engine_v3.delete_note(id)
    return jsonify({"success": success})

@app.route('/api/notes/v3/export/native', methods=['POST'])
def notes_v3_export_native():
    """Triggers a native Save File dialog via PyWebView Bridge."""
    global native_window
    if not native_window:
        return jsonify({"error": "Native bridge not active. Please use the Desktop Launcher."}), 500
    
    try:
        data = request.json
        title = data.get('title', 'note')
        content = data.get('content', '')
        
        # Open Native Dialog (This blocks till user picks)
        save_path = native_window.create_file_dialog(
            webview.SAVE_DIALOG, 
            directory=os.path.join(os.path.expanduser("~"), "Desktop"),
            save_filename=f"{title}.txt"
        )
        
        if save_path:
            # save_path comes back as a list/tuple or string depending on version
            actual_path = save_path[0] if isinstance(save_path, (list, tuple)) else save_path
            
            with open(actual_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"💎 [NATIVE SAVE] Note exported to: {actual_path}")
            return jsonify({"status": "success", "path": actual_path})
        else:
            return jsonify({"status": "cancelled"})
            
    except Exception as e:
        print(f"❌ Native Export Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/notes/v3/ai/summarize', methods=['POST'])
def notes_v3_ai_sum():
    if not assistant or not assistant.client: 
        return jsonify({"error": "AI Offline (No API Key)"}), 500
    try:
        content = request.json.get('content', '')
        prompt = f"Summarize this note in 2-3 concise sentences:\n\n{content[:2000]}"
        
        # Resolve correct client and model
        client, model = assistant._get_brain_client(config.PRIMARY_MODEL)
        res = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        return jsonify({"summary": res.choices[0].message.content.strip()})
    except Exception as e: return jsonify({"error": str(e)}), 500


# --- WEB SCRAPER STUDIO ENDPOINTS ---

@app.route('/api/notes/v3/ai/tag/<id>', methods=['POST'])
def notes_v3_ai_tag(id):
    """Directly triggers the intelligence brain for a specific note."""
    try:
        from smart_notes_3 import notes_engine_v3
        from smart_notes_brain import BackgroundBrain
        
        # Instantiate a temporary brain for synchronous processing
        brain = BackgroundBrain(notes_engine_v3)
        note = next((n for n in notes_engine_v3.data["notes"] if str(n["id"]) == str(id)), None)
        
        if note:
            # Run all intelligence modules including Neural Tagging
            brain.sorter.process(note)
            brain.extractor.process(note)
            brain.tagger.process(note)
            return jsonify({"status": "success", "tags": note.get("tags", [])})
        return jsonify({"error": "Note not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/notes/v3/ai/generate', methods=['POST'])
def notes_v3_ai_generate():
    """Generates a detailed, professional note based on a prompt."""
    if not assistant or not assistant.client:
        return jsonify({"error": "AI Brain Offline"}), 500
    try:
        topic = request.json.get('topic', '')
        language = request.json.get('language', 'english')
        print(f"✍️ [BANKOO WRITE] Drafting research on: {topic} (Language: {language})")
        
        # Language mapping for AI instructions
        lang_instructions = {
            'hindi': 'IMPORTANT: Generate ALL content in Hindi (हिंदी) language. Use Devanagari script.',
            'gujarati': 'IMPORTANT: Generate ALL content in Gujarati (ગુજરાતી) language. Use Gujarati script.',
            'english': 'Generate content in English.'
        }
        
        lang_instruction = lang_instructions.get(language, lang_instructions['english'])
        
        prompt = f"""{lang_instruction}
        
        You are the Bankoo High-Performance Content Architect. 
        Create an EXTREMELY COMPREHENSIVE and DETAILED technical dossier on: {topic}.
        
        CONTENT LENGTH REQUIREMENTS:
        - Minimum 2000 words of actual content
        - Create AT LEAST 8-10 major sections
        - Each section should have multiple subsections with detailed explanations
        - Include extensive examples, use cases, and real-world applications
        - Add detailed explanations for every concept
        
        STRUCTURE REQUIREMENTS:
        1. **Introduction** (300+ words)
           - Comprehensive overview
           - Historical context
           - Why this topic matters
           - Current relevance
        
        2. **Core Concepts** (500+ words)
           - Fundamental principles
           - Key terminology with detailed definitions
           - Theoretical foundations
        
        3. **Detailed Breakdown** (500+ words)
           - Deep dive into components
           - Technical specifications
           - Architecture/Structure
        
        4. **Practical Applications** (300+ words)
           - Real-world use cases
           - Industry applications
           - Common scenarios
        
        5. **Advanced Topics** (300+ words)
           - Complex concepts
           - Advanced techniques
           - Best practices
        
        6. **Challenges & Solutions** (200+ words)
           - Common problems
           - Solutions and workarounds
           - Troubleshooting tips
        
        7. **Future Trends** (200+ words)
           - Emerging developments
           - Predictions
           - Evolution of the field
        
        8. **Summary & Conclusion** (200+ words)
           - Key takeaways
           - Final thoughts
           - Recommendations
        
        ADAPTIVE CONTENT RULES:
        1. If the user is asking for THEORY or CONCEPTS:
           - Focus on profound explanations, history, and impact
           - Include philosophical implications
           - NO code blocks
        
        2. If the user is asking for CODE or IMPLEMENTATION:
           - Include MULTIPLE code examples
           - Show different approaches
           - Explain each code section in detail
           - Include comments in code
        
        QUALITY REQUIREMENTS:
        - Use professional, technical language
        - Be extremely thorough and detailed
        - Include numbered/bulleted lists where appropriate
        - Use markdown formatting (headers, bold, italic, lists, tables)
        - Make it encyclopedic in depth
        
        Format as JSON: {{"title": "...", "content": "markdown_here"}}."""
        
        # Resolve correct client and model
        client, model = assistant._get_brain_client(config.PRIMARY_MODEL)
        res = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are Bankoo's Expert Drafter. Return only raw JSON."},
                {"role": "user", "content": prompt}
            ]
        )
        
        raw_text = res.choices[0].message.content.strip()
        print(f"📦 [BANKOO WRITE] Raw response: {raw_text[:100]}...")
        
        # Robust JSON Extraction with Control Character Handling
        import json
        import re
        
        # 1. Extract JSON block
        json_str = raw_text
        if "```json" in raw_text:
            json_str = raw_text.split("```json")[1].split("```")[0].strip()
        elif "```" in raw_text:
            json_str = raw_text.split("```")[1].split("```")[0].strip()
        else:
            # Find first { and last }
            start = raw_text.find('{')
            end = raw_text.rfind('}') + 1
            if start != -1 and end != 0:
                json_str = raw_text[start:end]
        
        # 2. Sanitize control characters within JSON strings
        # Replace literal newlines/tabs/returns with escaped versions
        def sanitize_json_string(match):
            content = match.group(1)
            content = content.replace('\n', '\\n')
            content = content.replace('\r', '\\r')
            content = content.replace('\t', '\\t')
            return f'"{content}"'
        
        # Apply sanitization to content between quotes
        json_str = re.sub(r'"((?:[^"\\]|\\.)*)"', sanitize_json_string, json_str)

        # 3. Validate and return
        data = json.loads(json_str)
        print(f"✅ [BANKOO WRITE] Drafted: {data['title']}")
        return jsonify(data)
            
    except Exception as e:
        print(f"❌ [BANKOO WRITE] Error: {e}")
        return jsonify({"error": str(e)}), 500


# --- HEALTH MONITORING ENDPOINTS ---
@app.route('/api/health', methods=['GET'])
def flask_health():
    """Returns real-time system performance statistics"""
    try:
        import psutil
        import platform
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory()
        net_io = psutil.net_io_counters()

        ram_used_gb = ram.used / (1024 ** 3)
        ram_total_gb = ram.total / (1024 ** 3)

        # Get Disk Info
        disks = []
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disks.append({
                    "device": partition.device,
                    "mountpoint": partition.mountpoint,
                    "percent": usage.percent
                })
            except: continue

        return jsonify({
            "cpu": cpu,
            "ram": {
                "used_gb": round(ram_used_gb, 2),
                "total_gb": round(ram_total_gb, 2),
                "percent": round(ram.percent, 1)
            },
            "disks": disks,
            "network": {
                "bytes_sent": net_io.bytes_sent,
                "bytes_recv": net_io.bytes_recv
            },
            "system": {
                "platform": platform.system(),
                "release": platform.release()
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/notes/v3/ai/refine', methods=['POST'])
def notes_v3_ai_refine():
    """Conversational refinement of an existing note."""
    if not brain_ready: return jsonify({"error": "Neural Brain warming up..."}), 503
    try:
        data = request.json
        instruction = data.get('instruction', '')
        current_content = data.get('content', '')
        note_title = data.get('title', '')
        language = data.get('language', 'english')
        
        print(f"🧠 [NEURAL REFINE] Instruction: {instruction} (Language: {language})")
        
        # Language-specific instructions
        lang_instructions = {
            'hindi': 'CRITICAL: Maintain ALL content in Hindi (हिंदी). Use Devanagari script.',
            'gujarati': 'CRITICAL: Maintain ALL content in Gujarati (ગુજરાતી). Use Gujarati script.',
            'english': 'Maintain content in English.'
        }
        
        lang_instruction = lang_instructions.get(language, lang_instructions['english'])
        
        prompt = f"""{lang_instruction}
        
        You are refining a technical note titled '{note_title}'.
        Current Content:
        {current_content}
        
        User Instruction: "{instruction}"
        
        TASK:
        1. Fully incorporate the user's request into the note.
        2. Maintain the existing high-end "Studio" style (MD).
        3. If they ask for "more detail", "add code", or "specific diagrams", do it extensively.
        4. Return the ENTIRE updated content in markdown.
        5. Use LoremFlickr URLs for any new images: ![Illustration](https://loremflickr.com/1024/768/keyword,tech/all)
        
        Return ONLY the raw updated markdown string."""
        
        # Resolve correct client and model
        client, model = assistant._get_brain_client(config.REASONING_MODEL)
        res = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a Senior Technical Editor. You perfect and expand dossiers."},
                {"role": "user", "content": prompt}
            ]
        )
        
        updated_content = res.choices[0].message.content.strip()
        # Clean potential markdown block formatting
        if updated_content.startswith("```markdown"): updated_content = updated_content[11:].strip()
        if updated_content.startswith("```"): updated_content = updated_content[3:].strip()
        if updated_content.endswith("```"): updated_content = updated_content[:-3].strip()
            
        print(f"✅ [NEURAL REFINE] Update Applied.")
        return jsonify({"content": updated_content})
    except Exception as e:
        print(f"❌ [NEURAL REFINE] Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/notes/v3/ai/translate', methods=['POST'])
def notes_v3_ai_translate():
    """Translates note content between languages."""
    if not brain_ready: return jsonify({"error": "Neural Brain warming up..."}), 503
    try:
        data = request.json
        content = data.get('content', '')
        title = data.get('title', '')
        from_lang = data.get('fromLang', 'english')
        to_lang = data.get('toLang', 'english')
        
        lang_names = {
            'english': 'English',
            'hindi': 'Hindi (हिंदी, Devanagari script)',
            'gujarati': 'Gujarati (ગુજરાતી, Gujarati script)'
        }
        
        print(f"🌐 [TRANSLATE] {lang_names[from_lang]} → {lang_names[to_lang]}")
        
        prompt = f"""Translate the following technical note from {lang_names[from_lang]} to {lang_names[to_lang]}.

CRITICAL RULES:
1. Preserve ALL markdown formatting (headings, lists, code blocks, links, images)
2. Keep technical terms and code unchanged
3. Translate natural language content accurately
4. Maintain professional tone

Title: {title}

Content:
{content}

Return a JSON object with:
{{"title": "translated_title", "content": "translated_content_in_markdown"}}
"""
        
        # Resolve correct client and model
        client, model = assistant._get_brain_client(config.REASONING_MODEL)
        res = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a professional technical translator. You preserve formatting and technical accuracy."},
                {"role": "user", "content": prompt}
            ]
        )
        
        raw = res.choices[0].message.content.strip()
        
        # Extract JSON
        import json, re
        json_str = raw
        if "```json" in raw:
            json_str = raw.split("```json")[1].split("```")[0].strip()
        elif "```" in raw:
            json_str = raw.split("```")[1].split("```")[0].strip()
        
        # Sanitize control characters
        def sanitize_json_string(match):
            content = match.group(1)
            content = content.replace('\n', '\\n')
            content = content.replace('\r', '\\r')
            content = content.replace('\t', '\\t')
            return f'"{content}"'
        
        json_str = re.sub(r'"((?:[^"\\]|\\.)*)"', sanitize_json_string, json_str)
        result = json.loads(json_str)
        return jsonify(result)
    except Exception as e:
        print(f"❌ [TRANSLATE] Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/vision/analyze', methods=['POST'])
def vision_analyze():
    """Neural Vision Analyzer for Telekinesis/Clicking"""
    if not brain_ready: return jsonify({"error": "Neural Brain warming up..."}), 503
    try:
        data = request.json
        image_b64 = data.get('image')
        prompt = data.get('prompt', 'Look at this screenshot and identify the target.')

        # 1. Setup Gemini Client (VLM Capable with Fallback)
        import google.generativeai as genai
        genai.configure(api_key=config.GEMINI_API_KEY)
        
        # 2. Decode Image
        import base64, io
        from PIL import Image
        img_data = base64.b64decode(image_b64)
        img = Image.open(io.BytesIO(img_data))

        # 3. Vision API Call (with robust model fallback)
        logger.info(f"👁️ [VISION] Analyzing screen for: {prompt[:30]}...")
        
        candidates = ['gemini-1.5-flash-latest', 'gemini-1.5-flash', 'gemini-1.5-pro-latest', 'gemini-pro-vision']
        response = None
        error_log = []
        
        for cand in candidates:
            try:
                model = genai.GenerativeModel(cand)
                response = model.generate_content([prompt, img])
                if response:
                    logger.info(f"✅ [VISION] Success with model: {cand}")
                    break
            except Exception as e:
                logger.warning(f"⚠️ [VISION] Model {cand} failed: {e}")
                error_log.append(f"{cand}: {str(e)}")
                continue
        
        if not response:
            return jsonify({"error": "All Vision models failed.", "details": error_log}), 500
            
        text = response.text.strip()

        # 4. Parse JSON Output
        import json, re
        coords = {"x": 0, "y": 0}
        description = text # Default to raw text
        
        match = re.search(r'{.*}', text, re.DOTALL)
        if match:
            try:
                coords = json.loads(match.group())
                logger.info(f"🎯 [VISION] Target found at: {coords}")
                # Clean up description to remove the JSON part
                description = text.replace(match.group(), "").strip()
            except: pass
        
        return jsonify({
            "coordinates": coords, 
            "description": description or "Analysis complete.",
            "raw": text
        })

    except Exception as e:
        print(f"❌ [VISION] Analysis Error: {e}")
        return jsonify({"error": str(e)}), 500

# === WEB SCRAPER STUDIO (v2.0) ===

@app.route('/api/scraper/extract', methods=['POST'])
def scraper_extract():
    data = request.json
    return jsonify(scraper.extract(data.get('url'), data.get('options')))

@app.route('/api/scraper/ai/universal', methods=['POST'])
def scraper_magic():
    data = request.json
    return jsonify(scraper.ai_universal(data.get('url'), data.get('query')))

@app.route('/api/scraper/spider', methods=['POST'])
def scraper_spider():
    data = request.json
    return jsonify(scraper.spider(data.get('url'), data.get('max_pages', 5), data.get('options')))

@app.route('/api/scraper/batch', methods=['POST'])
def scraper_batch():
    data = request.json
    return jsonify(scraper.batch(data.get('urls'), data.get('options')))

@app.route('/api/scraper/graph', methods=['POST'])
def scraper_graph():
    data = request.json
    return jsonify(scraper.generate_graph(data.get('data')))

@app.route('/api/scraper/deduplicate', methods=['POST'])
def scraper_dedup():
    data = request.json
    return jsonify(scraper.deduplicate(data.get('data')))

@app.route('/api/scraper/schedule/add', methods=['POST'])
def scraper_sched_add():
    data = request.json
    return jsonify(scraper.add_schedule(data.get('url'), data.get('interval')))

@app.route('/api/scraper/schedule/list', methods=['GET'])
def scraper_sched_list():
    return jsonify(scraper.list_schedules())

@app.route('/api/scraper/schedule/remove', methods=['POST'])
def scraper_sched_remove():
    data = request.json
    return jsonify(scraper.remove_schedule(data.get('id')))

@app.route('/api/scraper/export/csv', methods=['POST'])
def scraper_export_csv():
    data = request.json
    csv = scraper.export_csv(data.get('data'))
    return jsonify({"csv": csv})

@app.route('/api/scraper/export/native', methods=['POST'])
def scraper_export_native():
    try:
        data = request.json
        content = data.get('content')
        fmt = data.get('format', 'json')
        
        # Save to Desktop by default
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        filename = f"Bankoo_Scrape_{int(time.time())}.{fmt}"
        path = os.path.join(desktop, filename)
        
        mode = 'w'
        if not isinstance(content, str):
             content = json.dumps(content, indent=2)

        with open(path, mode, encoding='utf-8') as f:
            f.write(content)
            
        return jsonify({"status": "success", "path": path})
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)})

@app.route('/api/scraper/ai/analyze', methods=['POST'])
def scraper_ai_analyze():
    # Analyze scraped data (Generic)
    try:
        data = request.json
        scraped_data = data.get('data', {})
        stype = data.get('type', 'summary')
        
        # Format context
        ctx = str(scraped_data)[:4000]
        prompt = f"Analyze this web data ({stype}):\n{ctx}"
        
        # Determine strict output based on type
        if stype == "sentiment": prompt += "\nProvide sentiment analysis in 3 bullet points."
        else: prompt += "\nProvide a concise executive summary."

        response = assistant.ask_ai(prompt)
        return jsonify({"result": response})
    except Exception as e:
         return jsonify({"error": str(e)})
# --- MAIN ENTRY POINT ---

def run_backend_server():
    """Main entry point for starting the Flask server (called by launcher thread)."""
    import socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
    except:
        local_ip = "127.0.0.1"

    print("="*60)
    print("  💎 BANKOO AI: SOVEREIGN DESKTOP ENGINE")
    print("="*60)
    print(f"\n🖥️  DESKTOP CORE:   http://127.0.0.1:5001")
    print(f"📱 MOBILE CORE:    http://{local_ip}:5001")
    print("="*60)
    print("\n� ENGINE STARTING...")
    
    # Auto-Open IDE in browser after a short delay to ensure server is hot
    # DISABLED: Uncomment the lines below if you want auto-launch
    # def open_browser():
    #     time.sleep(2)
    #     print("🌍 [UI] Launching Bankoo AETHER IDE...")
    #     webbrowser.open('http://127.0.0.1:5001/ide')
    # 
    # threading.Thread(target=open_browser, daemon=True).start()

    # ✨ AUTO-LAUNCH: Open AETHER IDE automatically after startup
    # DISABLED: Uncomment the lines below if you want auto-launch
    # def launch_ide():
    #     time.sleep(1.5)
    #     url = "http://127.0.0.1:5001/ide"
    #     print(f"🌍 [LINK] Launching AETHER IDE at {url}")
    #     webbrowser.open(url)
    # 
    # threading.Thread(target=launch_ide, daemon=True).start()
    
    print("📌 [INFO] Auto-launch disabled. Manually visit: http://127.0.0.1:5001/ide")

    app.run(host='0.0.0.0', port=5001, debug=False, threaded=True, use_reloader=False)

def register_native_window(window):
    """Bridge for PyWebView to register its window instance for direct JS injection."""
    global native_window
    native_window = window
    print("💎 [CORE] Native Bridge Established. Zero-Latency mode ACTIVE.")


# --- MOLTBOT PROCESS MANAGER (Terminal Consolidation) ---
class MoltbotManager:
    def __init__(self):
        self.process = None
        self.stop_event = threading.Event()
        self.bridge_path = r"C:\Users\Meet Sutariya\.gemini\antigravity\scratch\molten_bridge"
        self.port = 18789

    def start(self):
        print("🦞 [MOLTBOT] Initializing Multi-Channel Gateway...")
        threading.Thread(target=self._run_gateway, daemon=True).start()

    def _run_gateway(self):
        try:
            # removing --verbose for a cleaner, faster experience23.
            cmd = ["pnpm", "moltbot", "gateway", "--port", str(self.port)]
            
            # Start process with piped output
            self.process = subprocess.Popen(
                cmd,
                cwd=self.bridge_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                shell=True
            )

            for line in iter(self.process.stdout.readline, ''):
                if line:
                    clean_line = line.strip()
                    # VERBOSE MODE: Show all Moltbot logs so user knows it is active
                    print(f"🦞 [MOLTBOT] {clean_line}")
                if self.stop_event.is_set():
                    break

            self.process.stdout.close()
            self.process.wait()
            print("🦞 [MOLTBOT] Gateway process terminated.")
        except Exception as e:
            print(f"❌ [MOLTBOT] Failed to launch gateway: {e}")

    def stop(self):
        self.stop_event.set()
        if self.process:
            self.process.terminate()

moltbot_manager = MoltbotManager()

if __name__ == "__main__":
    # Start Moltbot Gateway in background
    # ENABLED: Unified integration for multi-platform support!
    # moltbot_manager.start()
    
    # Run the main Bankoo server
    run_backend_server()
