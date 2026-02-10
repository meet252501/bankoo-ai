"""
🚀 BANKOO AI - Setup Server
Flask backend for beautiful HTML installer

This server:
- Serves the HTML installer
- Handles API key saving
- Generates config files
- Opens browser automatically

Run: python setup_server.py
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import json
import webbrowser
import threading
from pathlib import Path

app = Flask(__name__)
CORS(app)

BASE_DIR = Path(__file__).parent.parent


@app.route('/')
def index():
    """Serve the main installer page"""
    return send_from_directory('', 'setup_ultimate.html')


@app.route('/api/save-config', methods=['POST'])
def save_config():
    """Save complete configuration"""
    try:
        config = request.json
        
        # Save .env file
        env_content = ""
        for key, value in config.get('api_keys', {}).items():
            if value:
                env_content += f"{key}={value}\n"
        
        env_path = BASE_DIR / ".env"
        with open(env_path, 'w') as f:
            f.write(env_content)
        
        # Save full config JSON
        config_path = BASE_DIR / "installer_config.json"
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        # Generate config.py updates
        config_updates = generate_config_updates(config)
        config_py_path = BASE_DIR / "config_updates.py"
        with open(config_py_path, 'w') as f:
            f.write(config_updates)
        
        return jsonify({
            'success': True,
            'message': 'Configuration saved successfully!',
            'files': [
                str(env_path),
                str(config_path),
                str(config_py_path)
            ]
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error saving configuration: {str(e)}'
        }), 500


def generate_config_updates(config):
    """Generate Python code to update config.py"""
    voice = config.get('voice', {})
    prefs = config.get('preferences', {})
    
    code = f"""# Auto-generated configuration updates
# Copy these to your config.py

# Voice Settings
DEFAULT_LANGUAGE = "{voice.get('default_language', 'gujarati').lower()}"
VOICE_GENDER = "{voice.get('gender', 'male').lower()}"
ENABLE_VOICE_AUTO_SWITCH = {voice.get('auto_switch', True)}

# AI Model Assignments
PRIMARY_MODEL = "{get_model_id(prefs.get('primary_model', 'Llama 3.3 70B (Cerebras)'))}"
CODING_MODEL = "{get_model_id(prefs.get('coding_model', 'DeepSeek Chat V3 (SOTA)'))}"

# Features
ENABLE_ANIMATIONS = {prefs.get('animations', True)}
ENABLE_TYPING_INDICATOR = {prefs.get('typing_indicator', True)}
ENABLE_AI_COUNCIL = {prefs.get('ai_council', True)}

# UI Theme
UI_THEME = "{prefs.get('ui_theme', 'dark').lower()}"
"""
    return code


def get_model_id(model_name):
    """Convert display name to model ID"""
    model_map = {
        "Llama 3.3 70B (Cerebras)": "cerebras/llama-3.3-70b",
        "Llama 3.3 70B (Groq)": "groq/llama-3.3-70b-versatile",
        "DeepSeek Chat V3": "deepseek/deepseek-chat",
        "DeepSeek Chat V3 (SOTA)": "deepseek/deepseek-chat",
        "Llama 3.3 70B": "cerebras/llama-3.3-70b"
    }
    return model_map.get(model_name, "cerebras/llama-3.3-70b")


def open_browser():
    """Open browser after short delay"""
    import time
    time.sleep(1.5)
    webbrowser.open('http://localhost:5555/')


if __name__ == '__main__':
    print("=" * 60)
    print("🚀 BANKOO AI SETUP SERVER")
    print("=" * 60)
    print()
    print("Opening browser to: http://localhost:5555/")
    print()
    print("Press Ctrl+C to stop the server when done.")
    print("=" * 60)
    
    # Open browser in background thread
    threading.Thread(target=open_browser, daemon=True).start()
    
    # Run Flask server
    app.run(host='localhost', port=5555, debug=False)
