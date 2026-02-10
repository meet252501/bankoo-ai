import os
import base64
import requests
import pyautogui
import logging
from io import BytesIO
from PIL import Image

logger = logging.getLogger(__name__)

class LocalVision:
    """
    Zenith v19: Local Screen Perception Engine.
    Uses Ollama (moondream / llava) for 100% free and private screen analysis.
    """
    def __init__(self, ollama_url="http://localhost:11434", model="moondream"):
        self.ollama_url = ollama_url
        self.model = model
        logger.info(f"👁️ [VISION] Local Vision Active (Model: {model})")

    def capture_screen(self, save_path="temp_vision.png"):
        """Captures a screenshot of the primary screen."""
        try:
            screenshot = pyautogui.screenshot()
            # Resize for faster processing (Ollama models like smaller images)
            screenshot.thumbnail((1280, 720))
            screenshot.save(save_path)
            return save_path
        except Exception as e:
            logger.error(f"👁️ [VISION] Screen capture failed: {e}")
            return None

    def analyze_screen(self, prompt="What is on my screen? describe concisely."):
        """Captures and analyzes the screen."""
        image_path = self.capture_screen()
        if not image_path:
            return "Vision capture failed."

        try:
            # Encode image to base64
            with open(image_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

            # Prepare Request for Ollama
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "images": [encoded_string]
            }

            response = requests.post(f"{self.ollama_url}/api/generate", json=payload, timeout=60)
            
            if response.status_code == 200:
                result = response.json().get("response", "No description generated.")
                logger.info("👁️ [VISION] Screen analysis successful.")
                return result
            else:
                return f"Vision Server Error: {response.status_code}"

        except Exception as e:
            logger.error(f"👁️ [VISION] Analysis failed: {e}")
            return f"Vision Error: {str(e)}"
        finally:
            if os.path.exists(image_path):
                os.remove(image_path)

# Global Instance
vision = LocalVision()
