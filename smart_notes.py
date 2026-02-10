"""
Smart Notes Storage Manager
Handles note persistence and AI categorization
"""
import json
import os
from datetime import datetime
from typing import List, Dict, Optional

class SmartNotesManager:
    def __init__(self, storage_path="smart_notes.json"):
        self.storage_path = storage_path
        self.notes = self._load_notes()
    
    def _load_notes(self) -> List[Dict]:
        """Load notes from JSON file"""
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def _save_notes(self):
        """Persist notes to JSON file"""
        with open(self.storage_path, 'w', encoding='utf-8') as f:
            json.dump(self.notes, f, indent=2, ensure_ascii=False)
    
    def create_note(self, title: str, content: str, tags: List[str] = None, note_type: str = "text", language: str = None) -> Dict:
        """Create a new note"""
        note = {
            "id": len(self.notes) + 1,
            "title": title,
            "content": content,
            "tags": tags or [],
            "note_type": note_type,  # "text" or "code"
            "language": language,     # "python", "javascript", etc.
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        self.notes.append(note)
        self._save_notes()
        return note
    
    def get_all_notes(self) -> List[Dict]:
        """Get all notes"""
        return sorted(self.notes, key=lambda x: x['updated_at'], reverse=True)
    
    def get_note(self, note_id: int) -> Optional[Dict]:
        """Get a specific note by ID"""
        for note in self.notes:
            if note['id'] == note_id:
                return note
        return None
    
    def update_note(self, note_id: int, title: str = None, content: str = None, tags: List[str] = None, note_type: str = None, language: str = None) -> Optional[Dict]:
        """Update an existing note"""
        note = self.get_note(note_id)
        if note:
            if title is not None:
                note['title'] = title
            if content is not None:
                note['content'] = content
            if tags is not None:
                note['tags'] = tags
            if note_type is not None:
                note['note_type'] = note_type
            if language is not None:
                note['language'] = language
            note['updated_at'] = datetime.now().isoformat()
            self._save_notes()
            return note
        return None
    
    def delete_note(self, note_id: int) -> bool:
        """Delete a note"""
        for i, note in enumerate(self.notes):
            if note['id'] == note_id:
                self.notes.pop(i)
                self._save_notes()
                return True
        return False
    
    def search_notes(self, query: str) -> List[Dict]:
        """Search notes by title, content, or tags"""
        query = query.lower()
        results = []
        for note in self.notes:
            if (query in note['title'].lower() or 
                query in note['content'].lower() or 
                any(query in tag.lower() for tag in note['tags'])):
                results.append(note)
        return results
    
    def categorize_note_ai(self, content: str, ai_client) -> List[str]:
        """Use AI to suggest tags/categories for a note"""
        try:
            prompt = f"Suggest 3-5 relevant tags for this note (comma-separated, lowercase):\n\n{content[:500]}"
            response = ai_client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=50,
                temperature=0.3
            )
            tags_str = response.choices[0].message.content.strip()
            tags = [tag.strip() for tag in tags_str.split(',')]
            return tags[:5]  # Limit to 5 tags
        except:
            return []

# Global instance
notes_manager = SmartNotesManager()
