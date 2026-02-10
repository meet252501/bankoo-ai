import sqlite3
import json
from datetime import datetime
import os

class BankooMemory:
    """Persistent memory system for cross-session user context"""
    
    def __init__(self, db_path='bankoo_memory.db'):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.create_tables()
    
    def create_tables(self):
        """Initialize database tables"""
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS user_memory (
                user_id TEXT,
                key TEXT,
                value TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (user_id, key)
            )
        ''')
        
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS conversation_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                message TEXT,
                response TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS user_preferences (
                user_id TEXT PRIMARY KEY,
                language TEXT DEFAULT 'gujarati',
                timezone TEXT,
                theme TEXT,
                metadata TEXT
            )
        ''')
        
        self.conn.commit()
    
    def remember(self, user_id, key, value):
        """Store a memory for a user"""
        self.conn.execute(
            'INSERT OR REPLACE INTO user_memory (user_id, key, value, timestamp) VALUES (?, ?, ?, ?)',
            (user_id, key, str(value), datetime.now())
        )
        self.conn.commit()
    
    def recall(self, user_id, key):
        """Retrieve a memory for a user"""
        cursor = self.conn.execute(
            'SELECT value FROM user_memory WHERE user_id = ? AND key = ?',
            (user_id, key)
        )
        result = cursor.fetchone()
        return result[0] if result else None
    
    def forget(self, user_id, key):
        """Delete a memory"""
        self.conn.execute(
            'DELETE FROM user_memory WHERE user_id = ? AND key = ?',
            (user_id, key)
        )
        self.conn.commit()
    
    def get_all_memories(self, user_id):
        """Get all memories for a user"""
        cursor = self.conn.execute(
            'SELECT key, value, timestamp FROM user_memory WHERE user_id = ?',
            (user_id,)
        )
        return cursor.fetchall()
    
    def save_conversation(self, user_id, message, response):
        """Save conversation for context"""
        self.conn.execute(
            'INSERT INTO conversation_history (user_id, message, response, timestamp) VALUES (?, ?, ?, ?)',
            (user_id, message, response, datetime.now())
        )
        self.conn.commit()
    
    def get_recent_conversations(self, user_id, limit=10):
        """Get recent conversations for context"""
        cursor = self.conn.execute(
            'SELECT message, response, timestamp FROM conversation_history WHERE user_id = ? ORDER BY timestamp DESC LIMIT ?',
            (user_id, limit)
        )
        return cursor.fetchall()
    
    def set_preference(self, user_id, language=None, timezone=None, theme=None, metadata=None):
        """Set user preferences"""
        if metadata and isinstance(metadata, dict):
            metadata = json.dumps(metadata)
        
        # Check if user exists
        cursor = self.conn.execute('SELECT user_id FROM user_preferences WHERE user_id = ?', (user_id,))
        exists = cursor.fetchone()
        
        if exists:
            # Update
            updates = []
            params = []
            if language:
                updates.append('language = ?')
                params.append(language)
            if timezone:
                updates.append('timezone = ?')
                params.append(timezone)
            if theme:
                updates.append('theme = ?')
                params.append(theme)
            if metadata:
                updates.append('metadata = ?')
                params.append(metadata)
            
            if updates:
                params.append(user_id)
                self.conn.execute(
                    f'UPDATE user_preferences SET {", ".join(updates)} WHERE user_id = ?',
                    params
                )
        else:
            # Insert
            self.conn.execute(
                'INSERT INTO user_preferences (user_id, language, timezone, theme, metadata) VALUES (?, ?, ?, ?, ?)',
                (user_id, language or 'gujarati', timezone, theme, metadata)
            )
        
        self.conn.commit()
    
    def get_preference(self, user_id):
        """Get user preferences"""
        cursor = self.conn.execute(
            'SELECT language, timezone, theme, metadata FROM user_preferences WHERE user_id = ?',
            (user_id,)
        )
        result = cursor.fetchone()
        if result:
            return {
                'language': result[0],
                'timezone': result[1],
                'theme': result[2],
                'metadata': json.loads(result[3]) if result[3] else {}
            }
        return None

# Global memory instance
memory = BankooMemory()
