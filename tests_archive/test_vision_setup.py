"""
Vision Lab Diagnostic Tool
Tests each component to identify the issue
"""

print("="*60)
print("  VISION LAB DIAGNOSTIC TEST")
print("="*60)
print()

# Test 1: Check OpenCV
print("Test 1: Checking OpenCV...")
try:
    import cv2
    print(f"   ✅ OpenCV installed (version {cv2.__version__})")
except ImportError as e:
    print(f"   ❌ OpenCV NOT installed: {e}")
    print("   Run: pip install opencv-python")
    input("\nPress Enter to exit...")
    exit()

# Test 2: Check MediaPipe
print("\nTest 2: Checking MediaPipe...")
try:
    import mediapipe as mp
    print(f"   ✅ MediaPipe imported")
except ImportError as e:
    print(f"   ❌ MediaPipe NOT installed: {e}")
    print("   Run: pip install mediapipe")
    input("\nPress Enter to exit...")
    exit()

# Test 3: Check MediaPipe.solutions
print("\nTest 3: Checking MediaPipe.solutions...")
try:
    if hasattr(mp, 'solutions'):
        print(f"   ✅ MediaPipe.solutions available")
        mp_hands = mp.solutions.hands
        mp_draw = mp.solutions.drawing_utils
        print(f"   ✅ MediaPipe hands module accessible")
    else:
        print(f"   ❌ MediaPipe.solutions NOT found")
        print(f"   MediaPipe attributes: {dir(mp)}")
        print("\n   Your MediaPipe installation is broken.")
        print("   Fix: pip uninstall mediapipe -y && pip install mediapipe")
        input("\nPress Enter to exit...")
        exit()
except Exception as e:
    print(f"   ❌ Error accessing MediaPipe.solutions: {e}")
    input("\nPress Enter to exit...")
    exit()

# Test 4: Check Camera Access
print("\nTest 4: Checking camera access...")
try:
    cap = cv2.VideoCapture(0)
    if cap.isOpened():
        print(f"   ✅ Camera opened successfully")
        ret, frame = cap.read()
        if ret:
            print(f"   ✅ Camera can read frames (Resolution: {frame.shape})")
        else:
            print(f"   ⚠️ Camera opened but can't read frames")
        cap.release()
    else:
        print(f"   ❌ Cannot open camera")
        print("   Possible issues:")
        print("   - No webcam connected")
        print("   - Camera in use by another app")
        print("   - Windows Privacy Settings blocking camera")
        input("\nPress Enter to exit...")
        exit()
except Exception as e:
    print(f"   ❌ Camera error: {e}")
    input("\nPress Enter to exit...")
    exit()

# All tests passed!
print("\n" + "="*60)
print("  ✅ ALL TESTS PASSED!")
print("="*60)
print("\nYour system is ready for Vision Lab!")
print("The issue might be with the script itself.")
print()
input("Press Enter to exit...")
