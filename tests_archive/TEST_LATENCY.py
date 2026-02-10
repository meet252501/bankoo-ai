3import time
from assistant import DesktopAssistant

print("⏱️ LATENCY TEST: Initializing Assistant...")
start = time.time()
bot = DesktopAssistant()
print(f"✅ Init took {time.time() - start:.2f}s")

print("⏱️ LATENCY TEST: Sending 'Hello' (First Run)...")
start = time.time()
# Mock the callback to avoid errors
def mock_callback(text, is_ide=False):
    print(f"CALLBACK RECEIVED: {text[:50]}...")

bot.output_callback = mock_callback

# Force init first to measure pure query time separately
bot._init_ai()
print(f"✅ _init_ai took {time.time() - start:.2f}s")

start = time.time()
bot.ask_ai("hello")
print(f"✅ ask_ai('hello') took {time.time() - start:.2f}s")

print("⏱️ LATENCY TEST: Sending 'Hello' (Second Run)...")
start = time.time()
bot.ask_ai("hello")
print(f"✅ ask_ai('hello') took {time.time() - start:.2f}s")
