import sys
import time
import requests
import logging
import asyncio
import threading
import config
import io
import base64
import os
import psutil
import ctypes
import pyautogui
import pyperclip
import schedule
import re
import edge_tts
import json
import socket
from datetime import time as dt_time
import asyncio
import subprocess
from groq import Groq
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from skill_manager import skill_manager
from vision_agent import VisionAgent
from vision_kernel import VisionKernel
# from agent_factory import AgentFactory # DEPRECATED

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class Sentinel(threading.Thread):
    """Background Watchdog for System Health"""
    def __init__(self, token, chat_id):
        super().__init__(daemon=True)
        self.token = token
        self.chat_id = chat_id
        self.last_alert = 0
        self.running = True

    def run(self):
        logger.info("🛡️ Sentinel Watchdog Started")
        while self.running:
            try:
                cpu = psutil.cpu_percent(interval=1)
                ram = psutil.virtual_memory().percent
                
                # Thresholds: CPU > 90% or RAM > 90%
                if cpu > 90 or ram > 90:
                    if time.time() - self.last_alert > 300: # 5 min cooldown
                        self.send_alert(f"⚠️ **High Load Alert!**\nCPU: {cpu}%\nRAM: {ram}%")
                        self.last_alert = time.time()
                
                time.sleep(60) 
            except Exception as e:
                logger.error(f"Sentinel Error: {e}")
                time.sleep(60)

    def send_alert(self, text):
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        try:
            requests.post(url, json={"chat_id": self.chat_id, "text": text, "parse_mode": "Markdown"}, timeout=5)
        except requests.exceptions.RequestException as e:
            logger.warning(f"Sentinel Alert Failed (Network Issue): {e}")
        except Exception as e:
            logger.error(f"Failed to send alert: {e}")

class MoltbotAgent:
    """
    Moltbot Agent (Ascended v10)
    - Direct Groq Brain (Independence)
    - System Control (Guardian)
    - Flask Bridge (Bankoo Synergy)
    - Omni Tools (File/Web/Sync)
    """
    def __init__(self):
        # 1. Identity & Auth
        self.token = getattr(config, 'TELEGRAM_BOT_TOKEN', '')
        if not self.token:
            logger.error("Telegram Token missing!")
            raise ValueError("TELEGRAM_BOT_TOKEN not found")
        
        # 2. Brain (Groq Direct)
        self.groq_api_key = getattr(config, 'GROQ_API_KEY', '')
        self.groq_client = None
        if self.groq_api_key:
            try:
                self.groq_client = Groq(api_key=self.groq_api_key)
                logger.info("🧠 Moltbot Brain: Groq Connected")
                # Initialize Specialized Vision Brain (OpenRouter)
                self.or_api_key = getattr(config, 'OPENROUTER_API_KEY', '')
                self.vision_brain = VisionAgent(self.or_api_key)
                logger.info("👁️ Vision Brain: Initialized via OpenRouter")
                # Initialize Specialized Autonomous Kernel
                self.vision_kernel = VisionKernel(self.vision_brain)
                logger.info("🦾 Vision Kernel: Initialized")
            except Exception as e:
                logger.error(f"Groq Error: {e}")

        # 3. Connection to Bankoo Main
        self.backend_url = "http://127.0.0.1:5001/api/bridge/telegram"
        
        # 4. Guardian System Prompt
        self.system_prompt = (
            "You are Moltbot, the Guardian Agent of this PC. "
            "You have direct control over system status. "
            "If Bankoo Main is offline, YOU take charge. "
            "Be concise, helpful, and protective."
        )
        
        # 5. Sentinel Start
        authorized_ids = getattr(config, 'AUTHORIZED_USER_IDS', [])
        primary_user = authorized_ids[0] if authorized_ids else 0
        if primary_user:
            self.sentinel = Sentinel(self.token, primary_user)
            self.sentinel.start()

        # 6. Zenith Pro State (v14)
        self.busy_mode = False
        self.busy_message = "I am currently busy. Bankoo is monitoring the system."

        # 7. Unified Skill System (v17) - Replaces Agent Spawner
        # Automatically load skills on startup
        skill_manager.load_markdown_skills(os.path.join(os.path.dirname(__file__), "moltbot_skills"))
        
        # self.factory = AgentFactory() # DEPRECATED
        # self.active_agent = None # DEPRECATED

        # 8. Dynamic API Key Vault (v19.3)
        self.key_vault_path = os.path.join(os.path.dirname(__file__), "api_keys.json")
        self.api_keys = self._load_keys()

    def _load_keys(self):
        if os.path.exists(self.key_vault_path):
            try:
                with open(self.key_vault_path, 'r') as f: return json.load(f)
            except: return {}
        return {}

    def _save_keys(self):
        try:
            with open(self.key_vault_path, 'w') as f: json.dump(self.api_keys, f, indent=4)
        except Exception as e:
            logger.error(f"Failed to save keys: {e}")

    def is_authorized(self, update):
        chat_id = update.effective_chat.id
        user_id = update.effective_user.id
        authorized_ids = getattr(config, 'AUTHORIZED_USER_IDS', [])
        return chat_id in authorized_ids or user_id in authorized_ids

    def _ensure_app_running(self, app_name):
        """
        Check if an app is running. If not, launch it.
        Returns True if app is ready, False if launch failed.
        """
        import time
        
        # Normalize app name
        app_lower = app_name.lower()
        
        # Check if already running
        is_running = False
        for proc in psutil.process_iter(['name']):
            try:
                if app_lower in proc.info['name'].lower():
                    is_running = True
                    break
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        if is_running:
             logger.info(f"✅ {app_name} is running (background/tray).")
             # We CONTINUING to launch code below to ensure it comes to FOREGROUND
        
        # App map for common applications
        app_paths = {
            'spotify': 'spotify',
            'chrome': 'chrome',
            'notepad': 'notepad',
            'discord': 'discord',
            'vscode': 'code',
            'code': 'code',
            'firefox': 'firefox',
            'edge': 'msedge'
        }
        
        launch_target = app_paths.get(app_lower, app_name)
        
        try:
            logger.info(f"🚀 Launching {app_name}...")
            os.startfile(launch_target)
            time.sleep(3)  # Give app time to initialize
            return True
        except Exception as e:
            logger.error(f"❌ Failed to launch {app_name}: {e}")
            return False

    # --- CORE COMMANDS ---
    async def handle_busy(self, update, context):
        """/busy [message] - Toggle Busy Mode"""
        if not self.is_authorized(update): return
        self.busy_mode = not self.busy_mode
        if context.args:
            self.busy_message = " ".join(context.args)
        
        status = "ON 🔴" if self.busy_mode else "OFF 🟢"
        msg = f"🛰️ **Busy Mode:** {status}\n💬 **Reply:** {self.busy_message}"
        await update.message.reply_markdown(msg)

    async def handle_task(self, update, context):
        """/task <actions> - Automated Sequence (comma separated)"""
        if not self.is_authorized(update): return
        raw_actions = " ".join(context.args)
        if not raw_actions:
            return await update.message.reply_text("Usage: /task open chrome, notify done")
        
        actions = [a.strip() for a in raw_actions.split(',')]
        await update.message.reply_text(f"🚀 **Zenith Task Initialized:** {len(actions)} steps...")
        
        # Run automation in background
        asyncio.create_task(self.execute_task_sequence(actions, update))

    async def execute_task_sequence(self, actions, update):
        """Background executor for /task sequences"""
        for i, action in enumerate(actions):
            try:
                logger.info(f"⚙️ [TASK] Executing step {i+1}: {action}")
                
                # Basic parsing for "open", "notify", "kill", "wait"
                if action.startswith("open "):
                    target = action.replace("open ", "")
                    os.startfile(target)
                elif action.startswith("notify "):
                    msg = action.replace("notify ", "")
                    await update.message.reply_text(f"🔔 **Notification:** {msg}")
                elif action.startswith("kill "):
                    name = action.replace("kill ", "")
                    for proc in psutil.process_iter(['name']):
                        if name in proc.info['name'].lower(): proc.kill()
                elif action.startswith("wait "):
                    secs = int(re.search(r'\d+', action).group())
                    await asyncio.sleep(secs)
                else:
                    # Fallback to general command execution or brain
                    await update.message.reply_text(f"⚠️ Unknown task step: {action}")
                
                await asyncio.sleep(1) # Gap between steps
            except Exception as e:
                await update.message.reply_text(f"❌ Task Step Failed ({action}): {e}")
        
        await update.message.reply_text("✅ **Zenith Task Sequence Completed.**")


    # --- KEY MANAGEMENT COMMANDS (v19.3) ---
    async def handle_setkey(self, update, context):
        """/setkey <KEY_NAME> <VALUE> - Securely save an API key"""
        if not self.is_authorized(update): return
        
        args = context.args
        if len(args) < 2:
            return await update.message.reply_text("Usage: /setkey KEY_NAME key_value_here")
            
        key_name = args[0].upper()
        key_value = args[1] # Simple token, for multi-word keys use quotes or careful parsing
        
        self.api_keys[key_name] = key_value
        self._save_keys()
        
        await update.message.reply_text(f"✅ **Securely Saved:** `{key_name}`")
        # Delete user message for security if possible (requires extended permissions)
        try:
            await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.message.message_id)
        except:
            pass

    async def handle_mykeys(self, update, context):
        """/mykeys - List stored API keys (masked)"""
        if not self.is_authorized(update): return
        
        if not self.api_keys:
            return await update.message.reply_text("📭 No API keys stored in Vault.")
            
        msg = "🔐 **Vault Contents:**\n"
        for k, v in self.api_keys.items():
            masked = f"{v[:4]}...{v[-4:]}" if len(v) > 8 else "****"
            msg += f"- `{k}`: {masked}\n"
            
        await update.message.reply_text(msg)

    # --- SKILL SYSTEM COMMANDS (v17) ---
    async def handle_skills(self, update, context):
        """/skills [category] - List skills or categories"""
        if not self.is_authorized(update): return
        
        grouped_skills = skill_manager.list_skills()
        if not grouped_skills:
            return await update.message.reply_text("📭 No skills loaded. Check moltbot_skills folder.")
            
        args = context.args
        print(f"DEBUG: /skills called with args: {args}")
        is_all = args and args[0].lower() == 'all'
        
        if args and not is_all:
            # User requested specific category
            target_cat = " ".join(args)
            # Fuzzy match or exact match
            matched_cat = None
            for cat in grouped_skills.keys():
                if target_cat.lower() in cat.lower():
                    matched_cat = cat
                    break
            
            if matched_cat:
                skills = grouped_skills[matched_cat]
                msg = f"📂 **Category: {matched_cat}**\n━━━━━━━━━━━━━━━━━━━━\n"
                # Chunking to avoid limit issues even within category
                chunks = []
                current_chunk = ""
                
                for s in sorted(skills, key=lambda x: x['name']):
                    icon = "📘" if s['type'] == 'knowledge' else "🐍"
                    desc = s['description'][:50] + "..." if len(s['description']) > 50 else s['description']
                    line = f"• `{s['name']}` - {desc}\n"
                    
                    if len(current_chunk) + len(line) > 3800:
                        chunks.append(current_chunk)
                        current_chunk = line
                    else:
                        current_chunk += line
                chunks.append(current_chunk)
                
                for chunk in chunks:
                    await update.message.reply_markdown(msg + chunk if chunk == chunks[0] else chunk)
            else:
                await update.message.reply_text(f"❌ Category '{target_cat}' not found. Try `/skills` or `/skills all`.")
        
        elif is_all:
            # Full Category List (Paginated)
            header = "📚 **FULL SKILL LIBRARY**\n━━━━━━━━━━━━━━━━━━━━\n"
            msg = header
            
            categories = sorted(grouped_skills.keys())
            
            # Chunking loop
            for cat in categories:
                count = len(grouped_skills[cat])
                line = f"📂 `{cat}` ({count})\n"
                
                if len(msg) + len(line) > 3800:
                    await update.message.reply_markdown(msg)
                    msg = line # Start new chunk
                else:
                    msg += line
            
            # Send final chunk + instructions
            footer = "\n💡 Usage:\n• `/skills <category>` to list skills\n• `/skill <name>` to view manual"
            if len(msg) + len(footer) > 4000:
                await update.message.reply_markdown(msg)
                await update.message.reply_markdown(footer)
            else:
                msg += footer
                await update.message.reply_markdown(msg)

        else:
            # Default: Essentials Dashboard (User Requested Structure)
            
            # flatten names for searching
            all_names = set()
            for s_list in grouped_skills.values():
                for s in s_list: all_names.add(s['name'])
            
            # Categories defined by user
            sections = [
                ("⚡ **System & Core**", ["bankoo", "github-pr", "shell", "file-search", "apple-notes", "weather", "time", "calculate"]),
                ("✅ **Productivity**", ["todoist", "google-calendar", "linear", "clickup", "things3"]),
                ("🛠️ **DevOps & Cloud**", ["kubectl", "docker", "vercel", "tailscale", "proxmox"]),
                ("🌐 **Web & Search**", ["tavily", "exa", "brave-search", "playwright"]),
                ("🎨 **Media & Creative**", ["spotify", "veo", "elevenlabs", "youtube-summarizer"]),
                ("💰 **Finance & Health**", ["ynab", "whoop", "crypto-prices"])
            ]
            
            msg = "⭐️ **ESSENTIAL SKILLS DASHBOARD**\n━━━━━━━━━━━━━━━━━━━━\n"
            
            for title, tags in sections:
                found_lines = []
                for tag in tags:
                    # 1. Exact Match
                    if tag in all_names:
                        found_lines.append(f"• `{tag}`")
                        continue
                        
                    # 2. Fuzzy/Substring Match (e.g. 'todoist' -> 'todoist-task-manager')
                    # We pick the shortest match to avoid junk
                    matches = [n for n in all_names if tag in n]
                    if matches:
                        best = min(matches, key=len)
                        found_lines.append(f"• `{best}`")
                
                if found_lines:
                    msg += f"\n{title}\n" + "\n".join(found_lines) + "\n"

            msg += (
                "\n━━━━━━━━━━━━━━━━━━━━\n"
                f"📚 **Total Library:** {sum(len(v) for v in grouped_skills.values())} skills\n"
                "• `/skills all` - Browse full list\n"
                "• `/skills <cat>` - Browse category"
            )
            await update.message.reply_markdown(msg)

    async def handle_skill_view(self, update, context):
        """/skill <name> - View skill instructions + Interactive Help"""
        if not self.is_authorized(update): return
        if not context.args: return await update.message.reply_text("Usage: `/skill <name>`\n💡 Tip: Use `/skills` to see the list.", parse_mode='Markdown')
        
        target = context.args[0].strip("<> ")
        
        # 0. Cross-Platform Aliases (Smart OS Detection)
        import platform
        current_os = platform.system()
        
        aliases = {
            'todo': 'todoist',
            'search': 'tavily',
            'browsing': 'brave-search',
            'calendar': 'google-calendar',
            'video': 'veo',
            'voice': 'elevenlabs',
            'trading': 'simmer-weather'
        }
        
        # Music Logic: Auto-detect best skill for OS
        if current_os == 'Darwin': # Mac
             aliases['music'] = 'spotify' # Uses AppleScript (Mac preferred)
             aliases['spotify'] = 'spotify'
        else: # Windows / Linux
             aliases['music'] = 'windows-media' # Simple (Media Keys)
             aliases['spotify'] = 'windows-media' # Default to No-API skill since user has no keys
             
        if target.lower() in aliases:
            target = aliases[target.lower()]
            
        content = skill_manager.get_skill_content(target)
        
        # Fuzzy Match Logic
        if not content:
            all_skills = skill_manager.list_skills() 
            # flatten
            flat_names = []
            if isinstance(all_skills, dict):
                 for s_list in all_skills.values():
                     for s in s_list: flat_names.append(s['name'])
            else:
                 flat_names = [s['name'] for s in all_skills]
            
            # Find matches where target is substring
            matches = [n for n in flat_names if target.lower() in n.lower()]
            
            if matches:
                # Pick shortest match (usually the most relevant root name)
                best_match = min(matches, key=len)
                await update.message.reply_text(f"🔍 Exact match not found. Assuming you meant: `{best_match}`")
                target = best_match
                content = skill_manager.get_skill_content(target)
        
        if content:
             # SYSTEMIC COMPATIBILITY CHECK
             skill_obj = skill_manager.get_skill_obj(target)
             warning_msg = ""
             
             if skill_obj and hasattr(skill_obj, 'metadata') and skill_obj.metadata:
                 try:
                     req_os = skill_obj.metadata.get('clawdbot', {}).get('requires', {}).get('os')
                     # Check if OS mismatch (e.g. Darwin vs Windows)
                     if req_os:
                         sys_os = current_os.lower()
                         if req_os.lower() == 'darwin' and sys_os != 'darwin':
                             warning_msg = "\n\n⚠️ **WARNING: This skill is for MacOS.** It may not work on Windows."
                         elif req_os.lower() == 'windows' and sys_os != 'windows':
                             warning_msg = "\n\n⚠️ **WARNING: This skill is for Windows.** It may not work on your OS."
                 except: pass

             # AUTO-SIMPLIFIER (AI Translator)
             summary = content[:2000]
             try:
                 if self.groq_client:
                     sys_prompt = (
                         "You are a Tech Simplifier. Rewrite this technical documentation into a short, friendly summary for a normal user.\n"
                         "Format:\n"
                         "🚀 **What it does:** (1 sentence)\n"
                         "🎮 **How to use:** (List 2-3 common natural language examples, e.g. 'Just say...')\n"
                         "⚠️ **Note:** (Any strict requirement, e.g. API key, OS)\n"
                         "Keep it under 100 words. NO code blocks."
                     )
                     c = self.groq_client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "system", "content": sys_prompt}, {"role": "user", "content": content[:3000]}]
                     )
                     summary = c.choices[0].message.content
             except:
                 pass # Fallback to raw text if AI fails

             await update.message.reply_markdown(f"📘 **Skill: {target}**\n\n{summary}{warning_msg}")
             
             # 2. Interactive Prompt
             prompt_msg = (
                 f"❓ **How can I help you with `{target}`?**\n"
                 f"Reply directly to this message with your request."
             )
             await update.message.reply_markdown(prompt_msg)
        else:
             await update.message.reply_text(f"❌ Skill '{target}' not found (and no close matches).")

    # --- REMOVED AGENT SPAWNER COMMANDS ---
    # handle_spawn, handle_agents, handle_agent_chat, handle_stop removed. 

    async def handle_status(self, update, context):
        cpu = psutil.cpu_percent(interval=None)
        ram = psutil.virtual_memory()
        uptime = int(time.time() - psutil.boot_time()) // 3600
        msg = (
            f"🛡️ **Zenith Health Diagnostic**\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"🧠 **CPU:** {cpu}%\n"
            f"💾 **RAM:** {ram.percent}% ({round(ram.used/1024**3,1)}/{round(ram.total/1024**3,1)} GB)\n"
            f"⏱️ **Uptime:** {uptime} hours\n"
            f"📡 **Sentinel:** Active"
        )
        await update.message.reply_markdown(msg)

    async def handle_ip(self, update, context):
        """/ip - Public & Local IP info"""
        try:
            local_ip = socket.gethostbyname(socket.gethostname())
            public_ip = requests.get("https://api.ipify.org?format=json").json()["ip"]
            msg = f"📡 **Network Identity:**\n🌍 Public: `{public_ip}`\n🏠 Local: `{local_ip}`"
            await update.message.reply_markdown(msg)
        except Exception as e:
            await update.message.reply_text(f"❌ Network Error: {e}")

    async def handle_wifi(self, update, context):
        """/wifi - Detailed WiFi Signal info"""
        try:
            results = subprocess.check_output(["netsh", "wlan", "show", "interfaces"], text=True)
            ssid = re.search(r"SSID\s+:\s+(.*)", results)
            signal = re.search(r"Signal\s+:\s+(.*)", results)
            msg = f"📶 **WiFi Diagnostic:**\n"
            msg += f"🔗 SSID: `{ssid.group(1).strip() if ssid else 'Disconnected'}`\n"
            msg += f"⚡ Strength: `{signal.group(1).strip() if signal else '0%'}`"
            await update.message.reply_markdown(msg)
        except:
            await update.message.reply_text("❌ WiFi info unavailable (Ethernet or Disabled).")

    async def handle_lock(self, update, context):
        """/lock"""
        await update.message.reply_text("🔒 Locking...")
        ctypes.windll.user32.LockWorkStation()

    async def handle_screenshot(self, update, context):
        """/screenshot"""
        try:
            path = "monitor_snap.png"
            pyautogui.screenshot(path)
            await update.message.reply_photo(photo=open(path, 'rb'), caption="🖥️ Screenshot")
        except Exception as e:
            await update.message.reply_text(f"❌ Screen Error: {e}")
        finally:
            if os.path.exists("monitor_snap.png"):
                os.remove("monitor_snap.png")

    # --- CONNECTIVITY ---
    async def handle_copy(self, update, context):
        """/copy <text>"""
        text = " ".join(context.args)
        if text:
            pyperclip.copy(text)
            await update.message.reply_text(f"📋 Copied: '{text}'")
        else:
            await update.message.reply_text("Usage: /copy <text>")

    async def handle_paste(self, update, context):
        """/paste"""
        text = pyperclip.paste()
        await update.message.reply_text(f"📋 **Clipboard:**\n{text}" if text else "📋 Empty")

    # --- WEB ---
    async def handle_google(self, update, context):
        """/google <query>"""
        query = " ".join(context.args)
        if not query: return await update.message.reply_text("Usage: /google <query>")
        
        await update.message.reply_text(f"🌍 Searching: {query}...")
        try:
            url = "https://html.duckduckgo.com/html/"
            headers = {'User-Agent': 'Mozilla/5.0'}
            
            def run_req():
                return requests.get(url, params={'q': query}, headers=headers, timeout=10)
            
            loop = asyncio.get_event_loop()
            res = await loop.run_in_executor(None, run_req)
            
            links = re.findall(r'<a class="result__a" href="([^"]+)">([^<]+)</a>', res.text)
            if links:
                msg = f"🌍 **Results:**\n"
                for i, (href, title) in enumerate(links[:5]):
                    msg += f"{i+1}. [{title}]({href})\n"
                await update.message.reply_markdown(msg)
            else:
                await update.message.reply_text("❌ No results.")
        except Exception as e:
            await update.message.reply_text(f"❌ Search Error: {e}")

    # --- OMNI TOOLS (File Ops) ---
    async def handle_ls(self, update, context):
        """/ls [path]"""
        path = " ".join(context.args).strip("<> ") or "."
        try:
            if os.path.isdir(path):
                items = os.listdir(path)
                msg = f"📂 **{path}:**\n" + "\n".join(items[:20])
                if len(items) > 20: msg += "\n...(more)"
                await update.message.reply_markdown(msg)
            else:
                await update.message.reply_text("❌ Not a directory.")
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {e}")

    async def handle_get(self, update, context):
        """/get <path>"""
        path = " ".join(context.args).strip("<> ")
        if not path: return
        if os.path.exists(path) and os.path.isfile(path):
            await update.message.reply_document(document=open(path, 'rb'))
        else:
            await update.message.reply_text("❌ File not found.")

    async def handle_upload(self, update, context):
        """Handle Document/Photo Uploads"""
        if not self.is_authorized(update): return
        
        # 1. Handle Photo (Direct Scan)
        if update.message.photo:
            photo = update.message.photo[-1]
            f = await photo.get_file()
            path = "incoming_vision.png"
            await f.download_to_drive(path)
            
            await update.message.reply_text("👁️ **Analyzing Image...**")
            
            with open(path, "rb") as img_f:
                b64 = base64.b64encode(img_f.read()).decode("utf-8")
            
            # Request Analysis from Backend
            v_url = "http://127.0.0.1:5001/api/vision/analyze"
            payload = {"image": b64, "prompt": "Describe this image in detail and identify any text or objects."}
            
            try:
                loop = asyncio.get_event_loop()
                resp = await loop.run_in_executor(None, lambda: requests.post(v_url, json=payload, timeout=30))
                if resp.status_code == 200:
                    data = resp.json()
                    await update.message.reply_text(f"🧠 **Vision Analysis:**\n{data.get('description')}")
                else:
                    await update.message.reply_text("❌ Neural Vision Error.")
            except Exception as e:
                await update.message.reply_text(f"❌ Analysis Failed: {e}")
            finally:
                if os.path.exists(path): os.remove(path)
            return

        # 2. Handle Document (Standard Save)
        doc = update.message.document
        if doc:
            f = await doc.get_file()
            path = os.path.join(os.path.dirname(__file__), doc.file_name)
            await f.download_to_drive(path)
            await update.message.reply_text(f"📂 Saved to Root: {doc.file_name}")

    # --- MEDIA & VOICE ---
    async def handle_media(self, update, context):
        """/play, /pause, /next, /mute, /vol [up/down/0-100]"""
        cmd = update.message.text.lower().replace('/', '').split()[0] # play, pause, etc.
        args = context.args
        
        try:
            if cmd in ['play', 'pause']: pyautogui.press('playpause')
            elif cmd == 'next': pyautogui.press('nexttrack')
            elif cmd == 'prev': pyautogui.press('prevtrack')
            elif cmd == 'mute': pyautogui.press('volumemute')
            elif cmd == 'vol':
                if not args: 
                    await update.message.reply_text("Usage: /vol [up/down]")
                    return
                val = args[0]
                if val == 'up': pyautogui.press('volumeup', presses=5)
                elif val == 'down': pyautogui.press('volumedown', presses=5)
                else: await update.message.reply_text("Usage: /vol [up/down]")
                
            await update.message.reply_text(f"🎵 Media: {cmd} executed")
        except Exception as e:
            await update.message.reply_text(f"❌ Media Error: {e}")

    async def _speak_response(self, text, update):
        """Helper to generate and send voice note + play on PC"""
        if not text: return
        try:
            # 1. Detect Language
            voice = "en-US-AriaNeural"
            if re.search(r'[\u0900-\u097F]', text): voice = "hi-IN-SwaraNeural"
            elif re.search(r'[\u0A80-\u0AFF]', text): voice = "gu-IN-DhwaniNeural"
            
            communicate = edge_tts.Communicate(text, voice)
            path = f"voice_{int(time.time())}.mp3"
            await communicate.save(path)
            
            # 2. Telegram Voice Note
            try:
                with open(path, 'rb') as vf:
                    await update.message.reply_voice(voice=vf)
            except Exception as e:
                logger.error(f"Telegram voice error: {e}")

            # 3. PC Playback
            try:
                os.startfile(os.path.abspath(path))
            except: pass

            # Cleanup after delay
            await asyncio.sleep(3)
            if os.path.exists(path): os.remove(path)
        except Exception as e:
            logger.error(f"TTS Error in _speak_response: {e}")

    async def handle_speak(self, update, context):
        """/say <text> -> TTS Audio Reply (Telegram + PC)"""
        text = " ".join(context.args)
        if not text: return
        await self._speak_response(text, update)

    # --- PROACTIVE & LIFE ---
    async def send_briefing(self, context):
        """Morning Briefing Task"""
        user_id = config.AUTHORIZED_USER_IDS[0]
        greeting = "🌅 *Good Morning, Sir!* \n\n"
        status = f"🛡️ **Sentinel:** Online\n🧠 **Brain:** Connected\n📅 **Calendar:** No meetings found (Mock)"
        await context.bot.send_message(chat_id=user_id, text=greeting + status, parse_mode='Markdown')

    async def handle_calendar(self, update, context):
        """/calendar [day]"""
        await update.message.reply_text("📅 **Calendar (Mock):**\n- 10:00 AM: Team Sync\n- 02:00 PM: Deep Work\n- 05:00 PM: Gym")

    # --- BRAIN ---
    async def chat_with_brain(self, text, user, injected_context=None):
        # 1. Bankoo Main
        try:
            resp = requests.post(self.backend_url, json={"message": text, "user": user}, timeout=5)
            if resp.status_code == 200:
                d = resp.json()
                return d.get("response", "✅"), d.get("media_path"), d.get("media_type")
        except:
            pass # Fail silently to backup
            
        if self.groq_client:
            # 2.0 Dynamic Skill Injection - Flatten the categorized list for the LLM
            all_skills = []
            skill_dict = skill_manager.list_skills()
            for cat, skills in skill_dict.items():
                for s in skills: all_skills.append(s['name'])
                
            skill_prompt = f"\n\n[AVAILABLE SKILLS]: {', '.join(all_skills)}\n" \
                           "If you need to use a skill, reply: [SKILL_REQUEST: <skill_name>]"
            
            # Detect recursive tool use
            final_system = self.system_prompt + skill_prompt
            
            if injected_context:
                final_system += f"\n\n[SYSTEM INJECTED KNOWLEDGE]:\n{injected_context}\n\n[INSTRUCTION]: Execute the request using this manual."

            try:
                c = self.groq_client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": final_system},
                        {"role": "user", "content": f"[{user}]: {text}"}
                    ]
                )
                reply = c.choices[0].message.content
                
                # Check for Skill Request
                if "[SKILL_REQUEST:" in reply:
                    match = re.search(r'\[SKILL_REQUEST:\s*(.*?)\]', reply)
                    if match:
                        skill_name = match.group(1).strip()
                        content = skill_manager.get_skill_content(skill_name)
                        if content:
                            # RECURSIVE CALL with skill context in SYSTEM PROMPT
                            return await self.chat_with_brain(text, user, injected_context=content)
                        else:
                            return f"❌ Skill '{skill_name}' requested but not found.", None, None
                
                return reply, None, None
            except Exception as e:
                return f"❌ Brain Dead ({e})", None, None
        return "❌ Offline.", None, None

    async def handle_message(self, update, context):
        if not self.is_authorized(update): return
        text = update.message.text
        user = update.message.from_user.username or "User"
        
        # 0. Busy Mode Auto-Responder
        if self.busy_mode:
            await update.message.reply_text(f"🤖 **Busy Mode Active:**\n{self.busy_message}")
            return

        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')
        
        # 1. Standard Brain (with Skills)
        reply, media, mtype = await self.chat_with_brain(text, user)
        # 2. Check for recursive skill output
        # (This is handled inside chat_with_brain recursion, so 'reply' is the final answer)
        
        # 1. Send Text Reply
        if media and os.path.exists(media):
            try:
                if mtype == "image": await update.message.reply_photo(open(media, 'rb'), caption=reply)
                elif mtype == "document": await update.message.reply_document(open(media, 'rb'), caption=reply)
            except: await update.message.reply_text(reply)
        else:
            await update.message.reply_text(reply)
            
        # 2. Automated Voice Response (Conditional v12.3)
        # Only trigger voice if user asks for it (Keywords: vn, voice, bol, speak, say)
        trigger_keywords = ['vn', 'voice', 'bol', 'speak', 'say', 'આવાજ']
        if any(k in text.lower() for k in trigger_keywords):
            # We strip markdown for better TTS quality
            clean_reply = re.sub(r'[*_`#]', '', reply)
            await self._speak_response(clean_reply, update)

    # --- CODING SKILLS ---
    async def handle_write(self, update, context):
        """/write <filename> <code>"""
        if not self.is_authorized(update): return
        text = update.message.text
        # Parse: /write filename code...
        parts = text.split(maxsplit=2)
        if len(parts) < 3:
            await update.message.reply_text("Usage: /write <filename> <code>")
            return
        
        filename = parts[1]
        code = parts[2]
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(code)
            await update.message.reply_text(f"💾 Saved: `{filename}`", parse_mode='Markdown')
        except Exception as e:
            await update.message.reply_text(f"❌ Write Error: {e}")

    async def handle_cmd(self, update, context):
        """/cmd <command>"""
        if not self.is_authorized(update): return
        cmd = " ".join(context.args)
        if not cmd: return
        
        await update.message.reply_text(f"⚙️ Executing: `{cmd}`...", parse_mode='Markdown')
        try:
            # Run command
            proc = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
            output = proc.stdout[:3000] + (proc.stderr[:1000] if proc.stderr else "")
            if not output: output = "✅ Done (No Output)"
            
            await update.message.reply_text(f"```\n{output}\n```", parse_mode='Markdown')
        except Exception as e:
            await update.message.reply_text(f"❌ Execution Error: {e}")

    async def handle_open(self, update, context):
        """/open <file/app/url>"""
        target = " ".join(context.args).strip("<> ")
        if not target: return
        try:
            os.startfile(target)
            await update.message.reply_text(f"🚀 Opening: `{target}`", parse_mode='Markdown')
        except Exception as e:
            await update.message.reply_text(f"❌ Open Error: {e}")

    async def handle_kill(self, update, context):
        """/kill <process_name>"""
        name = " ".join(context.args).strip("<> ").lower()
        if not name: return
        try:
            killed = 0
            for proc in psutil.process_iter(['name']):
                if name in proc.info['name'].lower():
                    proc.kill()
                    killed += 1
            await update.message.reply_text(f"💀 Terminated {killed} processes containing '{name}'.")
        except Exception as e:
            await update.message.reply_text(f"❌ Kill Error: {e}")

    async def handle_click(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """🎯 Neural VLM Click"""
        if not self.is_authorized(update): return
        if not context.args:
            return await update.message.reply_text("Usage: `/click <text>`\nExample: `/click login`", parse_mode='Markdown')
        
        target = " ".join(context.args).strip("<> ")
        await update.message.reply_text(f"👁️ Scanning screen for `{target}`...")
        
        try:
            # 1. Capture Screenshot
            path = "click_screenshot.jpg"
            screenshot = pyautogui.screenshot()
            screenshot.save(path)
            
            # 2. Analyze with Specialized Brain
            result = self.vision_brain.analyze_screen(path, f"Find and click the center of: {target}")
            
            if "error" in result:
                await update.message.reply_text(f"❌ **Brain Error:** {result['error']}")
            else:
                x, y = result['x'], result['y']
                desc = result.get('description', 'Target')
                
                pyautogui.moveTo(x, y, duration=1.0)
                pyautogui.click()
                await update.message.reply_text(f"✅ Mission Accomplished: Clicked `{desc}`.")
                
        except Exception as e:
            await update.message.reply_text(f"❌ **Click Error:** {e}")
        finally:
            if os.path.exists("click_screenshot.jpg"): os.remove("click_screenshot.jpg")

    async def handle_nav(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """🎨 Neural Vision Navigation (Brain-Only)"""
        if not self.is_authorized(update): return
        if not context.args:
            return await update.message.reply_text("Usage: `/nav <goal>`\nExample: `/nav find the login button`", parse_mode='Markdown')
        
        goal = " ".join(context.args)
        status_msg = await update.message.reply_text("🧠 **Consulting Vision Brain...**")
        
        try:
            # 1. Capture Screenshot
            path = "nav_screenshot.jpg"
            screenshot = pyautogui.screenshot()
            screenshot.save(path)
            
            # 2. Analyze with Specialized Brain
            result = self.vision_brain.analyze_screen(path, goal)
            
            if "error" in result:
                await status_msg.edit_text(f"❌ **Brain Error:** {result['error']}")
            else:
                x, y = result['x'], result['y']
                desc = result.get('description', 'Target')
                
                await status_msg.edit_text(f"🎯 **Brain Decision:** Found `{desc}` at ({x}, {y})\n⚙️ Moving & Clicking...")
                
                pyautogui.moveTo(x, y, duration=1.0)
                pyautogui.click()
                await update.message.reply_text(f"✅ Mission Accomplished: Clicked `{desc}`.")
                
        except Exception as e:
            await status_msg.edit_text(f"❌ **Navigation Error:** {e}")
        finally:
            if os.path.exists(path): os.remove(path)

    async def handle_auto(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """🦾 Full Autonomous Mission (The Marvelous Ghost)"""
        if not self.is_authorized(update): return
        if not context.args:
            return await update.message.reply_text("Usage: `/auto <goal>`\nExample: `/auto login to my portal and check status`", parse_mode='Markdown')
        
        goal = " ".join(context.args)
        status_msg = await update.message.reply_text("🚀 **MARVELOUS GHOST: MISSION STARTED**\n" + f"Goal: `{goal}`")

        async def update_status(text):
            try:
                # We append to the status message to keep history
                await context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode='Markdown')
            except: pass

        try:
            result = await self.vision_kernel.run_mission(goal, update_callback=update_status)
            await update.message.reply_text(f"🏁 **Mission Finale:**\n{result}", parse_mode='Markdown')
        except Exception as e:
            await update.message.reply_text(f"❌ **Operational Failure:**\n`{str(e)}`", parse_mode='Markdown')
    async def handle_stop(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """🚨 Emergency Stop"""
        if not self.is_authorized(update): return
        
        if hasattr(self, 'vision_kernel'):
            self.vision_kernel.stop_mission()
            await update.message.reply_text("🚨 **EMERGENCY STOP TRIGGERED!**\nAborting mission immediately...", parse_mode='Markdown')
        else:
             await update.message.reply_text("❌ Vision Kernel not active.", parse_mode='Markdown')

    async def handle_weather(self, update, context):
        """/weather <city>"""
        city = " ".join(context.args) or "Surat"
        try:
            url = f"https://wttr.in/{city}?format=%C+%t+%w"
            res = requests.get(url, timeout=10).text
            await update.message.reply_text(f"🌤️ **Weather ({city}):**\n{res}")
        except:
            await update.message.reply_text("❌ Weather service unavailable.")

    async def handle_voice(self, update, context):
        """Handle incoming Voice Notes (STT)"""
        if not self.is_authorized(update): return
        try:
            # 1. Download
            voice = update.message.voice
            path = "incoming_voice.ogg"
            f = await context.bot.get_file(voice.file_id)
            await f.download_to_drive(path)
            
            await update.message.reply_text("🎧 **Transcribing Voice...**")
            
            # 2. STT via Groq Whisper (Dedicated Satellite)
            if self.groq_client:
                with open(path, "rb") as audio_file:
                    transcription = self.groq_client.audio.transcriptions.create(
                        file=(path, audio_file.read()),
                        model="whisper-large-v3",
                        response_format="text"
                    )
                text = transcription
                await update.message.reply_text(f"📝 **Transcribed:**\n\"{text}\"")
                
                # 3. Process as normal message
                update.message.text = text
                await self.handle_message(update, context)
            else:
                await update.message.reply_text("❌ Groq Engine offline (No STT available).")
                
        except Exception as e:
            logger.error(f"Voice Error: {e}")
            await update.message.reply_text(f"❌ Voice Sat-Link Error: {e}")
        finally:
            if os.path.exists(path): os.remove(path)

    # --- HELP ---
    async def handle_help(self, update, context):
        msg = (
            "🦞 **BANKOO ZENITH v16: OMNI-REBORN**\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "🧬 **DYNAMIC SKILLS (v17)**\n"
            "• `/skills` — List available skills\n"
            "• `/skill <name>` — View manual\n"
            "• `[Auto]` — Just ask, I will use skills!\n"
            "\n"
            "🤖 **AUTOMATION & PRESENCE**\n"
            "• `/auto <goal>` — 🦾 Autonomous Mission\n"
            "• `/task <steps>` — Action sequences\n"
            "• `/busy <msg>` — Set auto-responder\n"
            "• `/copy` & `/paste` — Clipboard control\n"
            "\n"
            "🛡️ **SYSTEM GUARDIAN**\n"
            "• `/status` — Deep diagnostics\n"
            "• `/ip` & `/wifi` — Connectivity scan\n"
            "• `/lock` — Instant PC lockout\n"
            "\n"
            "👁️ **NEURAL WORKSPACE**\n"
            "• `/screenshot` — Capture monitor\n"
            "• `/click <text>` — 🎯 Neural VLM Click\n"
            "• `/nav <goal>` — 🧠 Vision Navigation\n"
            "• `[Photo]` — Scene analysis\n"
            "• `[Voice]` — Neural voice STT\n"
            "\n"
            "📂 **REMOTE EXPLORER**\n"
            "• `/ls <path>` — Scan directories\n"
            "• `/get <file>` — Download file\n"
            "• `/open <app>` — Launch app\n"
            "• `/kill <proc>` — Terminate process\n"
            "• `/write <f> <code>` — Code injection\n"
            "• `/cmd <shell>` — Terminal access\n"
            "\n"
            "🎵 **MULTIMEDIA & LIFE**\n"
            "• `/vol up/down` — Audio control\n"
            "• `/say <text>` — Neural speech\n"
            "• `/weather <city>` — Global climate\n"
            "• `/calendar` — Schedule peek\n"
            "\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "✨ *Master your machine. Anywhere.*"
        )
        await update.message.reply_markdown(msg)

    def run(self):
        # Custom Request with higher timeouts (Stability for slow networks)
        from telegram.request import HTTPXRequest
        # Increased to 120s to fix startup timeout issues
        request = HTTPXRequest(connect_timeout=120, read_timeout=120)
        
        app = ApplicationBuilder().token(self.token).request(request).build()
        
        app.add_handler(CommandHandler("start", self.handle_help))
        app.add_handler(CommandHandler("help", self.handle_help))
        app.add_handler(CommandHandler("status", self.handle_status))
        
        # Skills System (v17)
        app.add_handler(CommandHandler("skills", self.handle_skills))
        app.add_handler(CommandHandler("skill", self.handle_skill_view))
        
        app.add_handler(CommandHandler("busy", self.handle_busy))
        app.add_handler(CommandHandler("task", self.handle_task))
        app.add_handler(CommandHandler("ip", self.handle_ip))
        app.add_handler(CommandHandler("wifi", self.handle_wifi))
        app.add_handler(CommandHandler("lock", self.handle_lock))
        app.add_handler(CommandHandler("screenshot", self.handle_screenshot))
        app.add_handler(CommandHandler("click", self.handle_click))
        app.add_handler(CommandHandler("nav", self.handle_nav)) # New Vision Brain Command
        app.add_handler(CommandHandler("auto", self.handle_auto)) # New Autonomous Kernel Command
        app.add_handler(CommandHandler("stop", self.handle_stop)) # Emergency Stop
        app.add_handler(CommandHandler("copy", self.handle_copy))
        app.add_handler(CommandHandler("open", self.handle_open))
        app.add_handler(CommandHandler("kill", self.handle_kill))
        app.add_handler(CommandHandler("weather", self.handle_weather))

        app.add_handler(CommandHandler("paste", self.handle_paste))
        app.add_handler(CommandHandler("google", self.handle_google))
        app.add_handler(CommandHandler("ls", self.handle_ls))
        app.add_handler(CommandHandler("get", self.handle_get))
        app.add_handler(CommandHandler(["play", "pause", "next", "prev", "mute", "vol"], self.handle_media))
        app.add_handler(CommandHandler("say", self.handle_speak))
        app.add_handler(CommandHandler("calendar", self.handle_calendar))
        
        # Coding
        app.add_handler(CommandHandler("write", self.handle_write))
        app.add_handler(CommandHandler("cmd", self.handle_cmd))
        
        # Scheduler (JobQueue)
        app.job_queue.run_daily(self.send_briefing, time=dt_time(hour=8, minute=0))

        app.add_handler(MessageHandler(filters.VOICE, self.handle_voice))
        app.add_handler(MessageHandler(filters.Document.ALL | filters.PHOTO, self.handle_upload))
        app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), self.handle_message))
        
        print(f"🦞 [MOLTBOT] Omni-Guardian ONLINE")
        
        # Polling with retry logic for network instability
        # Polling with INFINITE retry logic for network instability (Daemon Mode)
        retry_delay = 5
        while True:
            try:
                app.run_polling(timeout=30)
                # If run_polling returns, it usually means clean shutdown, so we break
                break 
            except Exception as e:
                # Handle Conflict (Duplicate Instance) explicitly
                if "Conflict" in str(e):
                    logger.critical("⚠️ [MOLTBOT] Conflict Error: Another instance is running!")
                    logger.info("Waiting 15s for other instance to die...")
                    time.sleep(15)
                    continue

                logger.warning(f"⚠️ [MOLTBOT] Connection Lost: {e}. Retrying in {retry_delay}s...")
                time.sleep(retry_delay)
                # Exponential backoff up to 60s
                retry_delay = min(retry_delay * 2, 60)

if __name__ == "__main__":
    MoltbotAgent().run()
