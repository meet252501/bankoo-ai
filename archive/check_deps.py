import importlib
packages = ['pyautogui', 'PIL', 'cv2', 'pytesseract', 'easyocr']
print("Dependency Check:")
for p in packages:
    try:
        importlib.import_module(p)
        print(f"✅ {p} is installed")
    except ImportError:
        print(f"❌ {p} is NOT installed")
