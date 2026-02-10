import easyocr
import os

print("🚀 Initializing EasyOCR Reader (English)...")
try:
    # This downloads the models on first run
    reader = easyocr.Reader(['en'], gpu=False) 
    print("✅ EasyOCR is ready with English models.")
    
    # Simple test check
    print("🔬 Testing OCR on a dummy blank image...")
    import numpy as np
    from PIL import Image
    dummy_img = np.zeros((100, 100, 3), dtype=np.uint8)
    result = reader.readtext(dummy_img)
    print("✅ Basic OCR Loop test passed.")
except Exception as e:
    print(f"❌ Error during initialization: {e}")
