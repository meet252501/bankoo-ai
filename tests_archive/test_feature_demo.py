import sys
import os
import platform
import json

# Setup paths
sys.path.append(os.getcwd())
from skill_manager import SkillManager

def mock_simplifier(text):
    """Simulate what the AI would do"""
    return f"[AI SIMPLIFIED]: This skill controls {text[:20]}... (friendly summary)"

def test_logic():
    print("🔄 Initializing Skill Manager...")
    sm = SkillManager()
    # Mock loading a specific skill manually to ensure it's there for the test
    # (We assume the manager scans properly, but let's test the logic directly)
    
    # SYSTEM 1: TEST METADATA LOADING
    print("\n[TEST 1] Loading Skill Metadata...")
    # Using 'spotify' (mac) as example
    target_skill = "spotify" 
    
    # Force load if not found (since we might not have scanned everything in seconds)
    skill_path = os.path.join(os.getcwd(), "moltbot_skills", "openclaw-skills", "skills", "andrewjiang", "spotify-applescript", "SKILL.md")
    
    if os.path.exists(skill_path):
        with open(skill_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Manually run the parsing logic we added
        metadata = {}
        if content.startswith("---"):
            end_meta = content.find("---", 3)
            meta_text = content[3:end_meta]
            for line in meta_text.split('\n'):
                if ':' in line:
                    key, val = line.split(':', 1)
                    metadata[key.strip()] = val.strip()
        
        full_metadata = {}
        if 'metadata' in metadata:
            try:
                full_metadata = json.loads(metadata['metadata'])
                print(f"✅ Successfully parsed JSON metadata: {full_metadata.keys()}")
            except:
                print("❌ Failed to parse JSON metadata")
                
        # SYSTEM 2: OS CHECK LOGIC
        print("\n[TEST 2] Running OS Compatibility Check...")
        current_os = "Windows" # Simulator
        print(f"🖥️ Current OS: {current_os}")
        
        req_os = full_metadata.get('clawdbot', {}).get('requires', {}).get('os')
        print(f"📋 Skill Requires: {req_os}")
        
        warning_msg = ""
        if req_os:
             if req_os.lower() == 'darwin' and current_os.lower() != 'darwin':
                 warning_msg = "⚠️ **WARNING: This skill is for MacOS.** It may not work on Windows."
             elif req_os.lower() == 'windows' and current_os.lower() != 'windows':
                 warning_msg = "⚠️ **WARNING: This skill is for Windows.** It may not work on your OS."
        
        if warning_msg:
            print(f"🛡️ Security Result: {warning_msg}")
        else:
            print("✅ Security Result: Compatible")

        # SYSTEM 3: SIMPLIFIER LOGIC
        print("\n[TEST 3] Running Auto-Simplifier...")
        simplified = mock_simplifier(content)
        print(f"📝 Output:\n{simplified}\n{warning_msg}")

    else:
        print(f"❌ Test file not found at {skill_path}")

if __name__ == "__main__":
    test_logic()
