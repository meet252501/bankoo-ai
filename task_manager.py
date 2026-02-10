"""
Task Manager for Bankoo AI
Handles breaking down complex requests into step-by-step tasks and tracking progress.
"""

import uuid
import json
import logging
from typing import Dict, List, Optional
import re

logger = logging.getLogger(__name__)

class TaskManager:
    def __init__(self):
        # {task_id: {steps: [], current: 0, status: 'running', original_query: str}}
        self.tasks: Dict[str, Dict] = {}
        self.last_active_task_id: Optional[str] = None

    def get_last_active_task(self):
        """Return the ID of the most recently created incomplete task"""
        if self.last_active_task_id:
            task = self.tasks.get(self.last_active_task_id)
            if task and task['status'] != 'completed':
                return self.last_active_task_id
        return None
        
    def is_complex_task(self, text: str) -> bool:
        """
        Detect if a request requires breakdown into steps.
        Keywords: "plan", "step by step", "how to", "guide", "roadmap"
        """
        complex_keywords = [
            "plan a", "create a plan", "step by step", "roadmap", 
            "guide for", "how to start", "break down", "steps to"
        ]
        text_lower = text.lower()
        return any(kw in text_lower for kw in complex_keywords)

    def generate_steps(self, query: str) -> List[str]:
        """
        Generate logical steps for a given query using heuristic rules 
        (In a real scenario, this would call the LLM, but here we prep structure)
        """
        # This is a placeholder structure. The actual steps will be filled by the LLM
        # when processing the "PLAN_TASK" intent.
        
        # Simple heuristic fallback if LLM isn't used immediately
        if "trip" in query.lower():
            return [
                "Research destination and best time to visit",
                "Look for flights and accommodation options",
                "Create a daily itinerary of attractions",
                "Pack necessary items and check visa requirements",
                "Finalize budget and bookings"
            ]
        elif "workout" in query.lower():
            return [
                "Assess current fitness level and goals",
                "Design a warm-up routine",
                "Create a weekly exercise schedule (split by muscle groups)",
                "Plan nutrition and hydration",
                "Track progress and adjust intensity"
            ]
            
        return []

    def create_task(self, query: str, steps: List[str]) -> str:
        """Create a new task with given steps"""
        task_id = str(uuid.uuid4())[:8]
        self.tasks[task_id] = {
            'steps': steps,
            'current': 0,
            'status': 'pending',
            'original_query': query,
            'completed_steps': []
        }
        self.last_active_task_id = task_id
        logger.info(f"🆕 Created task {task_id}: {query} ({len(steps)} steps)")
        return task_id

    def get_next_step(self, task_id: str) -> Optional[str]:
        """Get the next pending step"""
        task = self.tasks.get(task_id)
        if not task:
            return None
            
        if task['current'] < len(task['steps']):
            step = task['steps'][task['current']]
            return step
        return None

    def complete_current_step(self, task_id: str) -> str:
        """Mark current step as done and advance"""
        task = self.tasks.get(task_id)
        if not task:
            return "Task not found."
            
        if task['current'] < len(task['steps']):
            completed = task['steps'][task['current']]
            task['completed_steps'].append(completed)
            task['current'] += 1
            
            if task['current'] >= len(task['steps']):
                task['status'] = 'completed'
                return f"✅ Task Completed! Final step done: {completed}"
            
            next_s = task['steps'][task['current']]
            return f"✅ Step completed: {completed}\n➡️ Next: {next_s}"
            
        return "Task already completed."

    def get_progress(self, task_id: str) -> str:
        """Get formatted progress string"""
        task = self.tasks.get(task_id)
        if not task:
            return "Task not found."
            
        total = len(task['steps'])
        current = task['current'] + 1
        percent = int((task['current'] / total) * 100)
        
        status = f"📋 Task: {task['original_query']}\n"
        status += f"Progress: {percent}% ({task['current']}/{total})\n\n"
        
        for i, step in enumerate(task['steps']):
            marker = "✅" if i < task['current'] else "⬜"
            if i == task['current']: marker = "➡️"
            status += f"{marker} Step {i+1}: {step}\n"
            
        return status

# Global instance
task_manager = TaskManager()
