import os
import json
import logging
import google.generativeai as genai
from PIL import Image

class VisionAgent:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('models/gemini-2.0-flash')
        self.system_prompt = "Find UI elements. Return JSON {x, y, description}."

    def analyze_screen(self, image_path, goal):
        img = Image.open(image_path)
        prompt = f"{self.system_prompt}\n\nGoal: {goal}"
        response = self.model.generate_content(
            [prompt, img],
            generation_config=genai.GenerationConfig(response_mime_type="application/json")
        )
        return json.loads(response.text)
