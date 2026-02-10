
import os
import json
import time
import random
from datetime import datetime

NOTES_V3_FILE = "smart_notes_v3.json"

class SmartNotesEngineV3:
    def __init__(self):
        self.data = {
            "notes": [],
            "folders": [
                {"id": "f_default", "name": "General", "color": "#00d4ff"},
                {"id": "f_code", "name": "Coding", "color": "#b026ff"}
            ]
        }
        self.load()

    def load(self):
        if os.path.exists(NOTES_V3_FILE):
            try:
                with open(NOTES_V3_FILE, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
            except: pass
        else:
            self.save()

    def save(self):
        try:
            with open(NOTES_V3_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=4)
        except Exception as e:
            print(f"Error saving notes v3: {e}")

    def create_note(self, title="New Note", content="", folder_id="f_default", language="english"):
        note = {
            "id": int(time.time() * 1000),
            "title": title,
            "content": content,
            "folderId": folder_id,
            "language": language,
            "updatedAt": datetime.now().isoformat(),
            "type": "text"
        }
        self.data["notes"].insert(0, note)
        self.save()
        
        # Trigger Background Brain
        if hasattr(self, 'brain'):
            self.brain.analyze_note(note['id'])
            
        return note

    def update_note(self, note_id, updates):
        for n in self.data["notes"]:
            if str(n["id"]) == str(note_id):
                n.update(updates)
                n["updatedAt"] = datetime.now().isoformat()
                self.save()
                
                # Trigger Background Brain (Debounced by brain logic)
                if hasattr(self, 'brain'):
                    self.brain.analyze_note(n['id'])
                    
                return n
        return None

    def create_folder(self, name, custom_id=None):
        fid = custom_id if custom_id else f"f_{int(time.time())}"
        # Check if exists
        if any(f['id'] == fid for f in self.data['folders']): return
        
        folder = {
            "id": fid,
            "name": name,
            "color": "#" + "".join([random.choice('0123456789ABCDEF') for j in range(6)])
        }
        self.data["folders"].append(folder)
        self.save()
        return folder

    def delete_note(self, note_id):
        self.data["notes"] = [n for n in self.data["notes"] if str(n["id"]) != str(note_id)]
        self.save()
        return True

    def get_all(self):
        return self.data

# Link Brain
from smart_notes_brain import BackgroundBrain
notes_engine_v3 = SmartNotesEngineV3()
notes_engine_v3.brain = BackgroundBrain(notes_engine_v3)
