import cv2
import numpy as np
import pyautogui
import os
import logging

logger = logging.getLogger(__name__)

class LandmarkVision:
    """Zero-Cost Vision using Template Matching (OpenCV)"""
    
    def __init__(self, templates_dir="vision_templates"):
        self.templates_dir = templates_dir
        if not os.path.exists(templates_dir):
            os.makedirs(templates_dir)
            
    def find_icon(self, icon_name, threshold=0.8):
        """Find an icon on screen based on a saved template image"""
        template_path = os.path.join(self.templates_dir, f"{icon_name}.png")
        if not os.path.exists(template_path):
            return {"error": f"Template for '{icon_name}' not found."}
            
        # Capture screen
        screen = np.array(pyautogui.screenshot())
        screen_gray = cv2.cvtColor(screen, cv2.COLOR_RGB2GRAY)
        
        # Load template
        template = cv2.imread(template_path, 0)
        w, h = template.shape[::-1]
        
        # Match
        res = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        
        if max_val >= threshold:
            # Calculate center
            cx = max_loc[0] + w // 2
            cy = max_loc[1] + h // 2
            
            # Normalize to 0-1000
            sw, sh = pyautogui.size()
            nx = int((cx / sw) * 1000)
            ny = int((cy / sh) * 1000)
            
            logger.info(f"🎯 Match found! Raw: ({cx}, {cy}) | Screen: {sw}x{sh} | Norm: ({nx}, {ny}) | MaxVal: {max_val:.4f}")
            return {"x": nx, "y": ny, "confidence": max_val}
            
        return {"error": f"'{icon_name}' not detected on screen."}

    def save_template(self, icon_name, x, y, w, h):
        """Save a region of the screen as a template for future use"""
        screen = np.array(pyautogui.screenshot())
        crop = screen[y:y+h, x:x+w]
        cv2.imwrite(os.path.join(self.templates_dir, f"{icon_name}.png"), cv2.cvtColor(crop, cv2.COLOR_RGB2BGR))
        return True
