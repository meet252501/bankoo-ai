
import os
import json
import time
import re
from datetime import datetime

NOTES_FILE = "smart_notes_db.json"

class SmartNotesEngine:
    def __init__(self):
        self.notes_data = {
            "version": "2.0",
            "folders": [
                {"id": "f_default", "name": "General", "color": "#00d4ff"},
                {"id": "f_code", "name": "Code Snippets", "color": "#b026ff"},
                {"id": "f_ideas", "name": "Brainstorming", "color": "#00ff88"}
            ],
            "notes": []
        }
        self._load_notes()

    def _load_notes(self):
        if os.path.exists(NOTES_FILE):
            try:
                with open(NOTES_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Simple migration check
                    if "version" not in data:
                        self.notes_data["notes"] = data # Assume list if legacy
                    else:
                        self.notes_data = data
            except Exception as e:
                print(f"Error loading notes: {e}")
        else:
            self._save_notes()

    def _save_notes(self):
        try:
            with open(NOTES_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.notes_data, f, indent=4)
        except Exception as e:
            print(f"Error saving notes: {e}")

    def get_all(self):
        return self.notes_data

    def create_note(self, title, content, folder_id="f_default", tags=None, note_type="text", language=None):
        new_note = {
            "id": int(time.time() * 1000), # Simple unique ID
            "title": title or "Untitled Note",
            "content": content or "",
            "folderId": folder_id,
            "tags": tags or [],
            "type": note_type, # 'text' or 'code'
            "language": language, # for code highlighting
            "createdAt": datetime.now().isoformat(),
            "updatedAt": datetime.now().isoformat(),
            "isPinned": False
        }
        self.notes_data["notes"].append(new_note)
        self._save_notes()
        return new_note

    def update_note(self, note_id, updates):
        for note in self.notes_data["notes"]:
            if str(note["id"]) == str(note_id):
                note.update(updates)
                note["updatedAt"] = datetime.now().isoformat()
                self._save_notes()
                return note
        return None

    def delete_note(self, note_id):
        initial_count = len(self.notes_data["notes"])
        self.notes_data["notes"] = [n for n in self.notes_data["notes"] if str(n["id"]) != str(note_id)]
        if len(self.notes_data["notes"]) < initial_count:
            self._save_notes()
            return True
        return False

    def create_folder(self, name, color=None):
        new_folder = {
            "id": f"f_{int(time.time())}",
            "name": name,
            "color": color or "#888888"
        }
        self.notes_data["folders"].append(new_folder)
        self._save_notes()
        return new_folder
    
    def delete_folder(self, folder_id):
        if folder_id == "f_default":
            return False # Cannot delete default
        
        self.notes_data["folders"] = [f for f in self.notes_data["folders"] if f["id"] != folder_id]
        
        # Move notes to default
        for note in self.notes_data["notes"]:
            if note["folderId"] == folder_id:
                note["folderId"] = "f_default"
        
        self._save_notes()
        return True

    # --- AI FEATURES API INTEGRATION ---
    def categorize_content(self, content, assistant_ref=None):
        if not assistant_ref or len(content) < 10:
            return ["general"]
        
        try:
            # Using the main assistant instance if passed
            prompt = f"Analyze this note content and suggest 3-5 short, relevant tags (comma separated). Output ONLY the tags:\n\n{content[:500]}"
            response = assistant_ref.chat(prompt) if hasattr(assistant_ref, 'chat') else "general"
            
            # Cleanup response
            tags = [t.strip().replace("#", "") for t in response.split(',') if t.strip()]
            return tags[:5]
        except:
            return ["general", "ai-tagged"]

    def summarize_content(self, content, assistant_ref=None):
        if not assistant_ref:
            return "AI Assistant not available."
        
        try:
            prompt = f"Summarize the following note in one concise paragraph:\n\n{content[:1500]}"
            return assistant_ref.chat(prompt)
        except Exception as e:
            return f"Error generating summary: {e}"
            
    def ask_about_notes(self, query, assistant_ref=None):
        if not assistant_ref:
            return {"answer": "AI Assistant not available.", "sources": []}
            
        # Simple RAG: Find relevant notes by keyword
        relevant_notes = []
        keywords = re.findall(r'\w+', query.lower())
        
        for note in self.notes_data["notes"]:
            score = 0
            text = (note["title"] + " " + note["content"]).lower()
            for kw in keywords:
                if kw in text:
                    score += 1
            if score > 0:
                relevant_notes.append({"note": note, "score": score})
        
        # Sort by relevance
        relevant_notes.sort(key=lambda x: x["score"], reverse=True)
        top_context = "\n---\n".join([f"Note: {n['note']['title']}\n{n['note']['content'][:300]}..." for n in relevant_notes[:5]])
        
        if not top_context:
            return {"answer": "I couldn't find any specific notes matching your query.", "sources": []}
            
        prompt = f"Answer the user's question based ONLY on these notes:\n\n{top_context}\n\nQuestion: {query}"
        answer = assistant_ref.chat(prompt)
        
        return {
            "answer": answer,
            "sources": [{"title": n['note']['title'], "id": n['note']['id']} for n in relevant_notes[:3]]
        }

# Global Instance
notes_engine = SmartNotesEngine()
