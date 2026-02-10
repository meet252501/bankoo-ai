import shutil
import os

src_base = r"C:\Users\Meet Sutariya\.gemini\antigravity\scratch"
dst_base = r"c:\Users\Meet Sutariya\Desktop\final banko.ai\resources\external_research"

try:
    os.makedirs(dst_base, exist_ok=True)
except Exception as e:
    print(f"Error creating dir: {e}")

repos = ["awesome-llm-apps", "owl"]

for repo in repos:
    s = os.path.join(src_base, repo)
    d = os.path.join(dst_base, repo)
    print(f"Moving {s} -> {d}...")
    try:
        if os.path.exists(d):
            print(f"⚠️ Destination {d} already exists!")
        else:
            shutil.move(s, d)
            print("✅ Success.")
    except Exception as e:
        print(f"❌ Error moving {repo}: {e}")
