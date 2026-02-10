import shutil
import os

src = r"C:\Users\Meet Sutariya\Desktop\old backup banko\assistant.py"
dst = r"C:\Users\Meet Sutariya\Desktop\final banko.ai\assistant.py"
backup = r"C:\Users\Meet Sutariya\Desktop\final banko.ai\assistant.py.bak"

print("Starting restoration...")

# 1. Backup existing file
if os.path.exists(dst):
    try:
        print(f"Backing up current file to: {backup}")
        shutil.copy2(dst, backup)
        print("Backup created successfully.")
    except Exception as e:
        print(f"Warning: Backup failed: {e}")

# 2. Restore from backup
if os.path.exists(src):
    try:
        print(f"Restoring from: {src}")
        shutil.copy2(src, dst)
        print("Success! assistant.py has been restored.")
    except Exception as e:
        print(f"CRITICAL ERROR: Restore failed: {e}")
else:
    print(f"Error: Source file does not exist: {src}")
