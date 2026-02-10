import os
import sys
import logging
import types

# Bulletproof Mock for flash_attn
class MockModule(types.ModuleType):
    def __getattr__(self, name):
        return None
    def __bool__(self):
        return False

def mock_flash_attn():
    if "flash_attn" not in sys.modules:
        mock = MockModule("flash_attn")
        mock.__spec__ = types.SimpleNamespace(origin="mock", loader=None)
        sys.modules["flash_attn"] = mock
        sys.modules["flash_attn.flash_attn_interface"] = MockModule("flash_attn_interface")
        sys.modules["flash_attn.bert_padding"] = MockModule("bert_padding")

mock_flash_attn()

import torch
from transformers import AutoProcessor, AutoModelForCausalLM
from PIL import Image

logger = logging.getLogger(__name__)

class FlorenceVision:
    """Local Neural Vision using Microsoft Florence-2 (Ultra-Lightweight)"""
    
    def __init__(self):
        logger.info("🧠 Initializing Florence-2 Neural Eye (230MB)...")
        try:
            model_id = 'Microsoft/Florence-2-base'
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
            
            # Using standard attn implementation to avoid flash_attn
            self.model = AutoModelForCausalLM.from_pretrained(
                model_id, 
                trust_remote_code=True,
                attn_implementation="sdpa"
            ).to(self.device).eval()
            self.processor = AutoProcessor.from_pretrained(model_id, trust_remote_code=True)
            logger.info(f"✅ Florence-2 Ready on {self.device}.")
        except Exception as e:
            logger.error(f"❌ Florence-2 Init Failed: {e}")
            self.model = None

    def find_element(self, image_path, target):
        if not self.model: return {"error": "Model not ready"}
        try:
            image = Image.open(image_path).convert("RGB")
            # Florence-2 specific grounding task
            task_prompt = "<CAPTION_TO_PHRASE_GROUNDING>"
            prompt = f"{task_prompt} {target}"
            
            inputs = self.processor(text=prompt, images=image, return_tensors="pt").to(self.device)
            
            with torch.no_grad():
                generated_ids = self.model.generate(
                    input_ids=inputs["input_ids"],
                    pixel_values=inputs["pixel_values"],
                    max_new_tokens=1024,
                    num_beams=3
                )
            
            generated_text = self.processor.batch_decode(generated_ids, skip_special_tokens=False)[0]
            parsed_answer = self.processor.post_process_generation(generated_text, task=task_prompt, image_size=(image.width, image.height))
            
            logger.info(f"🧠 Florence Raw Parsed: {parsed_answer}")
            
            # The key in the results dict is the TASK prompt, not the full prompt
            results = parsed_answer.get(task_prompt, {})
            bboxes = results.get("bboxes", [])
            
            if bboxes:
                box = bboxes[0] # [x1, y1, x2, y2]
                cx, cy = (box[0] + box[2]) / 2, (box[1] + box[3]) / 2
                nx, ny = int((cx / image.width) * 1000), int((cy / image.height) * 1000)
                logger.info(f"🎯 Local Neural Grounding: {target} -> ({nx}, {ny})")
                return {"x": nx, "y": ny}
            
            return {"error": "Not found locally"}
        except Exception as e:
            logger.error(f"Florence Grounding Error: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return {"error": str(e)}
