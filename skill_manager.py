"""
Skill Manager - Plugin system for Bankoo AI
Allows community skills and custom extensions
"""

import os
import importlib.util
import inspect
from typing import Dict, Callable, Any

class Skill:
    """Base class for skills"""
    
    def __init__(self, name, description, func=None, content=None, path=None, skill_type="python", category="General"):
        self.name = name
        self.description = description
        self.func = func
        self.content = content # Markdown content for LLM
        self.path = path
        self.skill_type = skill_type # 'python' or 'markdown'
        self.category = category
    
    def execute(self, *args, **kwargs):
        if self.func:
            return self.func(*args, **kwargs)
        return f"Markdown Skill: Read {self.name} content."

class SkillManager:
    """Manages and executes skills/plugins"""
    
    def __init__(self, skills_dir='skills'):
        self.skills: Dict[str, Skill] = {}
        self.skills_dir = skills_dir
        self.markdown_skills: Dict[str, Skill] = {}
        self._register_built_in_skills()
    
    def _register_built_in_skills(self):
        """Register default built-in skills"""
        
        # Weather skill (placeholder)
        self.register_skill(
            'weather',
            'Get weather information',
            lambda city: f"🌤️ Weather in {city}: Sunny, 25°C (Mock data)"
        )
        
        # Calculator skill
        self.register_skill(
            'calculate',
            'Perform calculations',
            lambda expr: eval(expr, {"__builtins__": {}})  # Safe eval with no builtins
        )
        
        # Time skill
        self.register_skill(
            'time',
            'Get current time',
            lambda: __import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
    
    def register_skill(self, name: str, description: str, func: Callable):
        """Register a new skill"""
        self.skills[name] = Skill(name, description, func)
        print(f"✅ Registered skill: {name}")
    
    def unregister_skill(self, name: str):
        """Remove a skill"""
        if name in self.skills:
            del self.skills[name]
            print(f"🗑️ Unregistered skill: {name}")
    
    def execute_skill(self, name: str, *args, **kwargs) -> Any:
        """Execute a skill by name"""
        if name not in self.skills:
            return f"❌ Skill '{name}' not found. Available: {', '.join(self.skills.keys())}"
        
        try:
            result = self.skills[name].execute(*args, **kwargs)
            return result
        except Exception as e:
            return f"❌ Skill execution error: {e}"
    
    def list_skills(self):
        """List all available skills grouped by category"""
        grouped_skills = {}
        
        # Helper to add to group
        def add_to_group(skill):
            cat = skill.category
            if cat not in grouped_skills: grouped_skills[cat] = []
            grouped_skills[cat].append({
                'name': skill.name, 
                'description': skill.description, 
                'type': skill.skill_type
            })

        for skill in self.skills.values(): add_to_group(skill)
        for skill in self.markdown_skills.values(): add_to_group(skill)
        
        return grouped_skills
    
    def load_skill_from_file(self, filepath: str):
        """
        Load a skill from a Python file
        
        The file should have a function named 'skill_func' and optionally:
        - SKILL_NAME: str
        - SKILL_DESCRIPTION: str
        """
        try:
            spec = importlib.util.spec_from_file_location("custom_skill", filepath)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Get skill metadata
            name = getattr(module, 'SKILL_NAME', os.path.basename(filepath).replace('.py', ''))
            description = getattr(module, 'SKILL_DESCRIPTION', 'Custom skill')
            func = getattr(module, 'skill_func', None)
            
            if not func:
                return f"❌ No 'skill_func' found in {filepath}"
            
            self.register_skill(name, description, func)
            return f"✅ Loaded skill: {name} from {filepath}"
            
        except Exception as e:
            return f"❌ Failed to load skill: {e}"
    
    def load_skills_from_directory(self, directory: str):
        """Load all .py files from a directory as skills"""
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"📁 Created skills directory: {directory}")
            return
        
        loaded = 0
        for filename in os.listdir(directory):
            if filename.endswith('.py') and not filename.startswith('_'):
                filepath = os.path.join(directory, filename)
                result = self.load_skill_from_file(filepath)
                if '✅' in result:
                    loaded += 1
        
        print(f"📦 Loaded {loaded} skills from {directory}")

    def load_markdown_skills(self, root_dir: str):
        """Recursively scan for SKILL.md files"""
        if not os.path.exists(root_dir):
            print(f"⚠️ Skills directory not found: {root_dir}")
            return

        loaded_count = 0
        for root, dirs, files in os.walk(root_dir):
            if "SKILL.md" in files:
                path = os.path.join(root, "SKILL.md")
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Simple Frontmatter Parser (YAML-like)
                    metadata = {}
                    if content.startswith("---"):
                        end_meta = content.find("---", 3)
                        if end_meta != -1:
                            meta_text = content[3:end_meta]
                            for line in meta_text.split('\n'):
                                if ':' in line:
                                    key, val = line.split(':', 1)
                                    metadata[key.strip()] = val.strip()
                    
                    name = metadata.get('name', os.path.basename(os.path.dirname(path)))
                    desc = metadata.get('description', 'No description provided.')
                    
                    # Parse 'metadata' JSON field (contains requirements)
                    full_metadata = {}
                    if 'metadata' in metadata:
                        try:
                            import json
                            full_metadata = json.loads(metadata['metadata'])
                        except:
                            pass

                    # Extract Category (Parent Directory Name = Author)
                    parts = path.replace('\\', '/').split('/')
                    category = "General"
                    if len(parts) >= 3:
                        category = parts[-3] 
                        if category in ['skills', 'moltbot_skills']: category = "Core"

                    skill = Skill(name, desc, content=content, path=path, skill_type="markdown", category=category)
                    skill.metadata = full_metadata # Store parsed metadata
                    self.markdown_skills[name] = skill
                    loaded_count += 1
                except Exception as e:
                    print(f"❌ Failed to load skill at {path}: {e}")
        
        print(f"📚 Loaded {loaded_count} Markdown Skills from {root_dir}")

    def get_skill_content(self, name: str):
        """Get the full content of a markdown skill"""
        if name in self.markdown_skills:
            return self.markdown_skills[name].content
        return None

    def get_skill_obj(self, name: str) -> Skill:
        """Get the full Skill object"""
        if name in self.markdown_skills:
            return self.markdown_skills[name]
        return None

# Global skill manager
skill_manager = SkillManager()
