
import re
import random
import time
from threading import Thread

class AutoSorter:
    """Intelligently moves notes into folders based on keywords."""
    def __init__(self, notes_engine):
        self.engine = notes_engine
        self.mapping = {
            "code": ["python", "javascript", "html", "css", "function", "api", "bug", "error", "arjun", "startup", "github", "coding", "logic", "dev"],
            "personal": ["recipe", "movie", "idea", "dream", "todo", "shopping", "health", "gym", "food", "travel", "story", "journal"],
            "work": ["meeting", "deadline", "project", "client", "report", "quarter", "investment", "stock", "finance", "bankoo", "trading", "equity"]
        }

    def process(self, note):
        text = (note.get("title", "") + " " + note.get("content", "")).lower()
        
        # 1. Folder Management (Keep basic sorting for speed)
        if note.get("folderId") == "f_default":
            for category, keywords in self.mapping.items():
                if any(k in text for k in keywords):
                    target_id = f"f_{category}"
                    if not any(f['id'] == target_id for f in self.engine.data['folders']):
                        self.engine.create_folder(category.capitalize(), target_id)
                    note['folderId'] = target_id
                    break

        # 2. Neural Tagging Pass (AI-Powered)
        # Legacy keyword tagging removed to prevent "Stuck" tags.
        pass

class AITagger:
    """Uses LLM to generate context-aware tags for a note."""
    def __init__(self, notes_engine):
        self.engine = notes_engine

    def process(self, note):
        try:
            from assistant import assistant
            import config
            
            content = f"Title: {note.get('title')}\nContent: {note.get('content')}"
            language = note.get('language', 'english')
            
            # Language-specific instructions
            lang_instructions = {
                'hindi': 'Generate tags in Hindi (हिंदी). Use Devanagari script.',
                'gujarati': 'Generate tags in Gujarati (ગુજરાતી). Use Gujarati script.',
                'english': 'Generate tags in English.'
            }
            
            lang_instruction = lang_instructions.get(language, lang_instructions['english'])
            
            prompt = f"""PERFORM DEEP SEMANTIC ANALYSIS.
            Provide 3-5 unique, conceptual tags for this note. 
            
            LANGUAGE: {lang_instruction}
            
            STRICT RULES:
            - AVOID generic tags like 'Code', 'Programming', 'Python' unless the note is 100% just a code snippet.
            - FOCUS on the SUBJECT MATTER (e.g. DatabaseArchitecture, NeuralNetwork, Logic, Strategy, History).
            - THINK: What is the high-level intent?
            
            Format: comma-separated list. No hashtags.
            Note:
            {content}
            """
            
            res = assistant.client.chat.completions.create(
                model=config.PRIMARY_MODEL,
                messages=[
                    {"role": "system", "content": "You are Bankoo's Neural Intelligence Engine. You analyze subject significance, not just keywords."},
                    {"role": "user", "content": prompt}
                ]
            )
            
            raw_tags = res.choices[0].message.content.strip().replace("#", "").split(",")
            clean_tags = [t.strip().capitalize() for t in raw_tags if t.strip() and len(t) > 2][:5]
            
            if clean_tags:
                note["tags"] = clean_tags
                self.engine.save()
                print(f"🧠 [DEEP THINKING] Neural Tags Applied: {clean_tags}")
        except Exception as e:
            print(f"⚠️ [AITAGGER] Deep analysis failed: {e}")

class ActionExtractor:
    """Scans for TODOs and actionable items."""
    def __init__(self, notes_engine):
        self.engine = notes_engine

    def process(self, note):
        content = note.get("content", "")
        # Regex for lines starting with "- [ ]", "TODO:", "Action:", or "To-do:"
        todos = re.findall(r'(?:-\s\[\s\]|TODO:|Action:|To-do:)\s*(.*)', content, re.IGNORECASE)
        
        if "tags" not in note: note["tags"] = []
        changed = False

        if todos:
            if "Actionable" not in note["tags"]:
                note["tags"].append("Actionable")
                changed = True
        
        # Also tag based on folder (Mapping to capitalized names)
        folder_id = note.get("folderId", "")
        if folder_id.startswith("f_"):
            cat = folder_id.replace("f_", "").capitalize()
            if cat != "Default" and cat not in note["tags"]:
                note["tags"].append(cat)
                changed = True

        if changed:
            print(f"⚡ [BRAIN] Tagged '{note['title']}' with: {note['tags']}")
            self.engine.save()

class NeuralLinker:
    """Connects related notes."""
    def process(self, note):
        # Placeholder for vector search
        pass

class BackgroundBrain:
    def __init__(self, notes_engine):
        self.sorter = AutoSorter(notes_engine)
        self.extractor = ActionExtractor(notes_engine)
        self.tagger = AITagger(notes_engine)
        self.linker = NeuralLinker()
        self.running = False
        
    def analyze_note(self, note_id):
        """Spawns a thread to analyze the note without blocking UI."""
        def _run():
            time.sleep(1) # Wait for typing to settle
            try:
                # Re-fetch note to get latest content
                note = next((n for n in self.sorter.engine.data["notes"] if str(n["id"]) == str(note_id)), None)
                if note:
                    self.sorter.process(note)
                    self.extractor.process(note)
                    self.tagger.process(note)
            except Exception as e:
                print(f"❌ [BRAIN ERROR] Analysis failed: {e}")

        Thread(target=_run, daemon=True).start()

# We will instantiate this in smart_notes_3.py
