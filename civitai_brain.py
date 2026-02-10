
import config
import logging
import os

# --- CONFIGURE LOGGING ---
logger = logging.getLogger(__name__)

# --- AUTHENTICATION (Must be done BEFORE importing civitai) ---
if getattr(config, 'CIVITAI_API_TOKEN', None):
    # The SDK looks for CIVITAI_API_TOKEN in environment variables
    os.environ["CIVITAI_API_TOKEN"] = config.CIVITAI_API_TOKEN
else:
    logger.warning("Civitai Token not found in config.")

# Import Library AFTER setting env var
try:
    import civitai
except Exception as e:
    logger.error(f"Civitai Import Failed likely due to Key: {e}")
    civitai = None

class CivitaiArtist:
    """
    The Creative Engine powered by Civitai.
    Generates high-quality AI art using Stable Diffusion models.
    """
    def __init__(self):
        self.default_model = "urn:air:sd1:checkpoint:civitai:4201@130072" # Realistic Vision V1.3 (Reliable)
        # self.default_model = "urn:air:sdxl:checkpoint:civitai:101055@128078" # SDXL (Higher Quality but slower)
        logger.info("🎨 Civitai Artist initialized.")

    def generate_image(self, prompt, negative_prompt="", width=512, height=512):
        """
        Generates an image from a text prompt.
        """
        try:
            logger.info(f"🎨 Generating Image: '{prompt}'...")
            
            # Default Negative Prompt if none provided
            if not negative_prompt:
                negative_prompt = "nsfw, (deformed, distorted, disfigured:1.3), poorly drawn, bad anatomy, wrong anatomy, extra limb, missing limb, floating limbs, (mutated hands and fingers:1.4), disconnected limbs, mutation, mutated, ugly, disgusting, blurry, amputation"

            input_data = {
                "model": self.default_model,
                "params": {
                    "prompt": prompt,
                    "negativePrompt": negative_prompt,
                    "scheduler": "EulerA",
                    "steps": 25,
                    "cfgScale": 7,
                    "width": width,
                    "height": height,
                    "clipSkip": 2
                }
            }

            # Run Job
            response = civitai.image.create(input_data)
            
            if response and 'jobId' in response:
                logger.info(f"✅ Job Started: {response['jobId']}")
                # In a real async system we'd wait, but usually SDK handles it or returns a job ID to poll.
                # The 'create' method might return immediate token or job info.
                # Actually, SDK docs say: response = civitai.image.create(input)
                # We need to check if it returns the URL directly or a Job ID.
                return response
            
            return {"error": "No Job ID returned"}

        except Exception as e:
            logger.error(f"Civitai Generation Error: {e}")
            return {"error": str(e)}

# Singleton Instance
artist = CivitaiArtist()
