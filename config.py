
import os

# MODE SETTINGS
SIMPLE_MODE = True  # Set to True for direct LLM behavior, False for full assistant
ENABLE_LOCAL_VISION = False 

# ============================================
# API KEYS - CONFIGURE IN .env FILE
# ============================================
# DO NOT hardcode API keys here! Use .env file instead.
# Copy .env.example to .env and add your keys there.

# Load from environment variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
BYTEZ_API_KEY = os.getenv("BYTEZ_API_KEY", "")
CIVITAI_API_TOKEN = os.getenv("CIVITAI_API_TOKEN", "")

# EXTENDED PROVIDER KEYS
DEEPINFRA_API_KEY = os.getenv("DEEPINFRA_API_KEY", "")
FIREWORKS_API_KEY = os.getenv("FIREWORKS_API_KEY", "")
CEREBRAS_API_KEY = os.getenv("CEREBRAS_API_KEY", "")

# AI COUNCIL MEMBERS (Multi-Expert System)
COUNCIL_CONFIG = {
    # === EXECUTIVE LEADERSHIP (C-SUITE) ===
    "CEO": "cerebras/llama-3.3-70b",                        # Chief Executive Officer (Llama 70B - Decision Maker)
    "CTO": "cerebras/llama-3.3-70b",                        # Chief Technology Officer (Architecture)
    "CSO": "cerebras/llama-3.3-70b",                        # Chief Strategy Officer (Planning)
    "CISO": "groq/llama-3.3-70b-versatile",                 # Chief Info Security Officer (Security)
    "CDO": "black-forest-labs/FLUX.1-schnell",              # Chief Design Officer (Visuals)
    "CCO": "google/gemma-2-9b",                             # Chief Communications Officer (Copy)
    "CRO": "groq/llama-3.3-70b-versatile",                  # Chief Risk Officer (Critic)

    # === ENGINEERING LEADERSHIP ===
    "VP_ENGINEERING": "deepseek/deepseek-chat",             # Writes core complex logic (DeepSeek V3)
    "CHIEF_SCIENTIST": "deepseek/deepseek-chat",            # Deep Logic & Math (DeepSeek V3)
    "QA_LEAD": "google/gemma-2-9b",                         # Quality Assurance Lead (Reviewer)
    
    # === SPECIALIZED STAFF ===
    "PRINCIPAL_ENGINEER": "groq/llama-3.3-70b-versatile",   # Debugger (Llama 70B)
    "SENIOR_ENGINEER": "meta-llama/Llama-3.1-8B",           # Fast Feature Builder (Llama 8B)
    "DATA_ARCHITECT": "cerebras/llama-3.3-70b",             # Database Expert
    "PLATFORM_ARCHITECT": "deepseek/deepseek-chat",         # API & Systems Expert
    "PERFORMANCE_ENGINEER": "groq/llama-3.3-70b-versatile", # Optimization
    "TECHNICAL_WRITER": "cerebras/llama-3.3-70b",           # Documentation

    # === LEGACY COMPATIBILITY (Ref direct mapping) ===
    "ARCHITECT": "cerebras/llama-3.3-70b",        # -> CTO
    "STRATEGIST": "cerebras/llama-3.3-70b",       # -> CSO
    "SENIOR_CODER": "deepseek/deepseek-chat",     # -> VP_ENGINEERING
    "CRITIC": "groq/llama-3.3-70b-versatile",     # -> CRO
    "DESIGNER": "black-forest-labs/FLUX.1-schnell", # -> CDO
    "JUDGE": "cerebras/llama-3.3-70b",            # -> CEO
}

# MODEL ASSIGNMENTS (Role-Based Routing)
PRIMARY_MODEL = "cerebras/llama-3.3-70b"   # CHAT = Llama 3.3 (Reliable & Fast - via Cerebras)
FAST_MODEL = "groq/llama-3.1-8b-instant"            # SPEED = 8b-Instant (Required for Ghost-Pilot)
CODING_MODEL = "deepseek/deepseek-chat" # DeepSeek V3 (SOTA)
CODE_REVIEWER_MODEL = "cerebras/llama-3.3-70b"     # REVIEW = Llama Quality
REASONING_MODEL = "deepseek/deepseek-chat"  # LOGIC = Revert to DeepSeek (Stable)
CREATIVE_MODEL = "black-forest-labs/FLUX.1-schnell" # Creative = Flux Schnell (Active HF)
SECURITY_MODEL = "groq/llama-3.3-70b-versatile"  # SAFETY = Guard (70B)
SAFE_MODE_MODEL = "meta-llama/Llama-3.1-8B"       # Fallback = Llama 3.1 (Active HF)
WHISPER_MODEL = "openai/whisper-large-v3-turbo"   # Audio = Whisper V3 Turbo (Active HF)

# Note: CODE_REVIEWER acts like a senior developer/counselor
# - Reviews your code and suggests improvements
# - Explains what could be better and why
# - Guides you to the solution without writing everything

# VOICE SETTINGS (Multilingual Support)
# Default voices (Gujarati)
MALE_VOICE = "gu-IN-NiranjanNeural"
FEMALE_VOICE = "gu-IN-DhwaniNeural"
DEFAULT_VOICE = MALE_VOICE

# Multilingual Voice Characters (Auto-switching based on language)
# When user says "speak in Spanish", Bankoo uses native Spanish voice
MULTILINGUAL_VOICES = {
    # Indian Languages
    'gujarati': ('gu-IN-NiranjanNeural', 'gu-IN-DhwaniNeural'),
    'hindi': ('hi-IN-MadhurNeural', 'hi-IN-SwaraNeural'),
    'tamil': ('ta-IN-ValluvarNeural', 'ta-IN-PallaviNeural'),
    'telugu': ('te-IN-MohanNeural', 'te-IN-ShrutiNeural'),
    'marathi': ('mr-IN-ManoharNeural', 'mr-IN-AarohiNeural'),
    'bengali': ('bn-IN-BashkarNeural', 'bn-IN-TanishaaNeural'),
    
    # European Languages
    'english': ('en-US-GuyNeural', 'en-US-JennyNeural'),
    'english-uk': ('en-GB-RyanNeural', 'en-GB-SoniaNeural'),
    'spanish': ('es-ES-AlvaroNeural', 'es-ES-ElviraNeural'),
    'french': ('fr-FR-HenriNeural', 'fr-FR-DeniseNeural'),
    'german': ('de-DE-ConradNeural', 'de-DE-KatjaNeural'),
    'italian': ('it-IT-DiegoNeural', 'it-IT-ElsaNeural'),
    'portuguese': ('pt-BR-AntonioNeural', 'pt-BR-FranciscaNeural'),
    'russian': ('ru-RU-DmitryNeural', 'ru-RU-SvetlanaNeural'),
    
    # Asian Languages  
    'chinese': ('zh-CN-YunxiNeural', 'zh-CN-XiaoxiaoNeural'),
    'japanese': ('ja-JP-KeitaNeural', 'ja-JP-NanamiNeural'),
    'korean': ('ko-KR-InJoonNeural', 'ko-KR-SunHiNeural'),
    'arabic': ('ar-SA-HamedNeural', 'ar-SA-ZariyahNeural'),
    'thai': ('th-TH-NiwatNeural', 'th-TH-PremwadeeNeural'),
    'vietnamese': ('vi-VN-NamMinhNeural', 'vi-VN-HoaiMyNeural'),
}

# Voice switching enabled (auto-detect language and use native voice)
ENABLE_VOICE_AUTO_SWITCH = True
VOICE_GENDER = 'male'  # Default: 'male' or 'female'

# LINGUISTIC SETTINGS
LANGUAGE_CODE = "gu-IN"
STRICT_GUJARATI = True
DEFAULT_SYSTEM_LANGUAGE = "gujarati"  # System-wide default
STT_MODE = "online" # Versions: "online" (Whisper) or "offline" (Vosk)
ZEN_MODE = "advanced" # "basic" (GitHub Zen only) or "advanced" (Hybrid)
ZEN_LOCALE = "gu" # Auto-translate Zen quotes to Gujarati

# SYSTEM FLAGS
ADMIN_MODE_ENABLED = True
LOG_PATH = "bankoo_interactions.jsonl"

# --- EXTERNAL API KEYS (Load from .env) ---
ALPHA_VANTAGE_KEY = os.getenv("ALPHA_VANTAGE_KEY", "")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "")
WOLFRAM_APP_ID = os.getenv("WOLFRAM_APP_ID", "")
ABSTRACT_IMAGES_KEY = os.getenv("ABSTRACT_IMAGES_KEY", "")
ABSTRACT_SCRAPE_KEY = os.getenv("ABSTRACT_SCRAPE_KEY", "")
ABSTRACT_AVATARS_KEY = os.getenv("ABSTRACT_AVATARS_KEY", "")
ABSTRACT_API_KEY = os.getenv("ABSTRACT_API_KEY", "")

IMAGGA_KEY = os.getenv("IMAGGA_KEY", "")
IMAGGA_SECRET = os.getenv("IMAGGA_SECRET", "")

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
SHUTTLEAI_API_KEY = os.getenv("SHUTTLEAI_API_KEY", "")
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY", "")

# OMDB API (For Movie Search)
OMDB_API_KEY = os.getenv("OMDB_API_KEY", "")

# UI SETTINGS
WINDOW_SIZE = (400, 500)
WINDOW_TITLE = "Bankoo Professional Assistant"

# --- TELEGRAM ZENITH BRIDGE (Clawd-Inspired) ---
# ⚠️ SECURITY: Keep your Token secret! 
# 🔒 WHITELIST: Only AUTHORIZED_USER_IDS can control Bankoo.
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
AUTHORIZED_USER_IDS = [int(id) for id in os.getenv("AUTHORIZED_USER_IDS", "").split(",") if id]

# LOCAL AI SETTINGS (Ollama v17)
OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_MODEL = "llama3.2:3b" # Options: llama3.2:1b (Faster), llama3.2:3b (Smarter)
ENABLE_LOCAL_FALLBACK = True  # Automatically switch to Ollama if internet fails
