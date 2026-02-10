
import sys
import os

print(f"Python Executable: {sys.executable}")
print(f"Working Directory: {os.getcwd()}")

try:
    import huggingface_hub
    print(f"✅ huggingface_hub found: {huggingface_hub.__version__}")
except ImportError as e:
    print(f"❌ huggingface_hub NOT found: {e}")

try:
    import config
    print(f"Config Loaded: {config.__file__}")
    print(f"GROQ_KEY: {'Found' if config.GROQ_API_KEY else 'Missing'}")
    print(f"HF_KEY: {'Found' if getattr(config, 'HUGGINGFACE_API_KEY', None) else 'Missing'}")
    
    # Check the key values (first few chars)
    if getattr(config, 'HUGGINGFACE_API_KEY', None):
         print(f"HF_KEY Value: {config.HUGGINGFACE_API_KEY[:4]}...")
except ImportError:
    print("❌ Config NOT found.")
