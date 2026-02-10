import sys

try:
    import pyfiglet
    print(pyfiglet.figlet_format("IT WORKS!"))
    print("SUCCESS: Pyfiglet is installed and running.")
except ImportError:
    print("❌ Pyfiglet NOT found (The Smart Runner should have installed this!).")
