
import sys
sys.path.append(r"c:\Users\Meet Sutariya\Desktop\final banko.ai")
from youtube_brain import yt_brain

def verify():
    vid = "ocjB0F76EC8"
    print(f"🎬 Verifying Video ID: {vid}")
    res = yt_brain.get_transcript(vid)
    print(f"Status: {res['status']}")
    if res['status'] == 'success':
        print(f"✅ Success! Found transcript (length: {len(res['text'])})")
        print(f"Preview: {res['text'][:200]}...")
    else:
        print(f"❌ Failed: {res['message']}")

if __name__ == "__main__":
    verify()
