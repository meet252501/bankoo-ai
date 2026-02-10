import os
import logging
from vision_landmark import LandmarkVision
from vision_accessibility import AccessibilityAgent
from vision_florence import FlorenceVision
import config

logger = logging.getLogger(__name__)

class LocalVisionCoordinator:
    """Coordinates local vision strategies to minimize cloud costs"""
    
    def __init__(self):
        self.landmarks = LandmarkVision()
        self.accessibility = AccessibilityAgent()
        self.neural_eye = FlorenceVision()
        
    def find_element(self, image_path, target):
        """Try local strategies in order of speed/cost"""
        
        # Strategy 1: Landmark / Template Matching (Fastest)
        logger.info(f"📍 Checking Landmarks for: {target}")
        result = self.landmarks.find_icon(target.lower().replace(" ", "_"))
        if "error" not in result:
            return {
                "thought": f"[LANDMARK] Found exact match for '{target}' via template.",
                "action": "click",
                "params": {"x": result["x"], "y": result["y"]},
                "status": "CONTINUE"
            }
            
            
        # Strategy 2: Accessibility Tree (Structure First)
        logger.info(f"🌳 Checking Accessibility Tree for: {target}")
        result = self.accessibility.find_element(target)
        if "error" not in result:
             return {
                "thought": f"[ACCESSIBILITY] Found '{target}' in the UI Tree structure.",
                "action": "click",
                "params": {"x": result["x"], "y": result["y"]},
                "status": "CONTINUE"
            }

        # Strategy 3: Neural Sight (Florence-2 - No Training Needed)
        logger.info(f"🧠 Checking Neural Sight (Florence-2) for: {target}")
        result = self.neural_eye.find_element(image_path, target)
        if "error" not in result:
             return {
                "thought": f"[NEURAL] Found '{target}' using local model.",
                "action": "click",
                "params": {"x": result["x"], "y": result["y"]},
                "status": "CONTINUE"
            }

        return {"error": "Local strategies failed"}
