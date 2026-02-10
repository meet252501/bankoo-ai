import moondream as md
from PIL import Image
import logging
import os

logger = logging.getLogger(__name__)

class MoondreamVision:
    """Local Neural Vision using Moondream2 (Zero Training Required)"""
    
    def __init__(self, model_path=None):
        logger.info("🧠 Initializing Moondream Neural Eye...")
        try:
            # This will automatically download the 0.5B model if not present
            self.model = md.vl()
            logger.info("✅ Moondream Ready.")
        except Exception as e:
            logger.error(f"❌ Moondream Init Failed: {e}")
            self.model = None

    def find_element(self, image_path, target):
        """Find an element on screen using semantic logic"""
        if not self.model:
            return {"error": "Moondream model not initialized."}
            
        try:
            image = Image.open(image_path)
            
            # Use the detect action to find coordinates
            # Target should be a natural description like "the Chrome icon" or "the search bar"
            logger.info(f"🧠 Moondream is looking for: '{target}'...")
            
            # Moondream's detect returns a list of objects with bounding boxes
            objs = self.model.detect(image, target)["objects"]
            
            if objs:
                # Take the first/best match
                best_match = objs[0]
                bbox = best_match["bbox"] # [ymin, xmin, ymax, xmax] normalized 0-1
                
                # Calculate center
                cy = (bbox[0] + bbox[2]) / 2
                cx = (bbox[1] + bbox[3]) / 2
                
                # Scaled to 0-1000 for Bankoo Kernel
                nx = int(cx * 1000)
                ny = int(cy * 1000)
                
                logger.info(f"🎯 Moondream matched '{target}' at ({nx}, {ny})")
                return {"x": nx, "y": ny, "description": f"Neural match for '{target}'"}
            
            return {"error": "Neural match not found."}
        except Exception as e:
            logger.error(f"🧠 Moondream Error: {e}")
            return {"error": str(e)}
