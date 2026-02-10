import cv2
import mediapipe as mp
import time
import math
import requests

# Try importing gesture dependencies
try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
except ImportError:
    PYAUTOGUI_AVAILABLE = False
    print("⚠️ pyautogui not found. Auto-installing...")

print("="*60)
print("  BANKOO VISION LAB - STABLE EDITION")
print("="*60)
print("  Gestures:")
print("  🤙 SHAKA   -> Mic ON")
print("  🖐️ OPEN    -> Mic OFF")
print("  ☝️ POINTER -> Mouse Navigation")
print("  [ESC] / Q  -> Exit")
print("="*60)

# Initialize MediaPipe
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

# Open Camera
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("❌ ERROR: Cannot access webcam!")
    exit()

# Globals
mic_active = False
last_mic_time = 0
last_action_time = 0
peace_start_time = 0 
volume_cooldown = 0 # Throttling for Analog Controls
ACTION_COOLDOWN = 0.5 

def calculate_angle(a, b, c):
    """Calculate angle between three points (joint)"""
    # Vectors BA and BC
    ba = [a.x - b.x, a.y - b.y, a.z - b.z]
    bc = [c.x - b.x, c.y - b.y, c.z - b.z]
    
    # Dot product and magnitudes
    dot_product = ba[0]*bc[0] + ba[1]*bc[1] + ba[2]*bc[2]
    mag_ba = math.sqrt(sum(x*x for x in ba))
    mag_bc = math.sqrt(sum(x*x for x in bc))
    
    if mag_ba * mag_bc == 0: return 0
    
    angle = math.acos(max(min(dot_product / (mag_ba * mag_bc), 1.0), -1.0))
    return math.degrees(angle)

# Main Loop
with mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2, # Enabled 2 hands for Double Peace
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
) as hands:
    
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("⚠️ Failed to read frame")
            continue

        # Flip & Convert
        image = cv2.flip(image, 1)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        h, w, _ = image.shape
        
        # Process
        results = hands.process(image_rgb)
        
        current_time = time.time()
        peace_hand_count = 0 

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                
                try:
                    # =================================================
                    # 🧠 VECTOR GESTURE ENGINE
                    # =================================================
                    
                    # Landmarks
                    wrist = hand_landmarks.landmark[0]
                    thumb_tip = hand_landmarks.landmark[4]
                    index_tip = hand_landmarks.landmark[8]
                    middle_tip = hand_landmarks.landmark[12]
                    ring_tip = hand_landmarks.landmark[16]
                    pinky_tip = hand_landmarks.landmark[20]
                    
                    pinky_pip = hand_landmarks.landmark[18]

                    # 1. Calculate Angles (Straight > 150, Bent < 100)
                    angle_index = calculate_angle(hand_landmarks.landmark[5], hand_landmarks.landmark[6], hand_landmarks.landmark[8])
                    angle_middle = calculate_angle(hand_landmarks.landmark[9], hand_landmarks.landmark[10], hand_landmarks.landmark[12])
                    angle_ring = calculate_angle(hand_landmarks.landmark[13], hand_landmarks.landmark[14], hand_landmarks.landmark[16])
                    angle_pinky = calculate_angle(hand_landmarks.landmark[17], hand_landmarks.landmark[18], hand_landmarks.landmark[20])
                    
                    # 2. Define States
                    thumb_extended = math.hypot(thumb_tip.x - pinky_pip.x, thumb_tip.y - pinky_pip.y) > 0.15
                    pinch_dist = math.hypot(thumb_tip.x - index_tip.x, thumb_tip.y - index_tip.y)
                    is_pinch = pinch_dist < 0.05 

                    index_straight = angle_index > 150
                    middle_straight = angle_middle > 150
                    ring_straight = angle_ring > 150
                    pinky_straight = angle_pinky > 150
                    
                    index_bent = angle_index < 100
                    middle_bent = angle_middle < 100
                    ring_bent = angle_ring < 100
                    pinky_bent = angle_pinky < 100

                    # -------------------------------------------------
                    # A. ANALOG CONTROLS (PINCH) - OVERRIDES OTHERS
                    # -------------------------------------------------
                    if is_pinch:
                        # Draw pinch point
                        cx, cy = int((thumb_tip.x + index_tip.x)/2 * w), int((thumb_tip.y + index_tip.y)/2 * h)
                        cv2.circle(image, (cx, cy), 10, (255, 255, 0), -1)

                        if index_tip.x < 0.5: # LEFT SIDE -> BRIGHTNESS
                            cv2.putText(image, "BRIGHTNESS", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
                            level = "UNK"
                            try: 
                                import screen_brightness_control as sbc
                                if index_tip.y < 0.2: sbc.set_brightness('+2')
                                elif index_tip.y > 0.8: sbc.set_brightness('-2')
                            except: pass
                        else: # RIGHT SIDE -> VOLUME
                            cv2.putText(image, "VOLUME", (w-150, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                            if index_tip.y < 0.2: 
                                if current_time - volume_cooldown > 0.1:
                                    pyautogui.press('volumeup')
                                    volume_cooldown = current_time
                            elif index_tip.y > 0.8:
                                if current_time - volume_cooldown > 0.1:
                                    pyautogui.press('volumedown')
                                    volume_cooldown = current_time
                        
                        # SKIP other gestures if pinching
                        raise Exception("Pinch Active") 

                    # -------------------------------------------------
                    # B. VOICE TRIGGER: SHAKA (🤙) - ULTRA RESPONSIVE
                    # -------------------------------------------------
                    # Logic: Thumb & Pinky OUT | Index, Middle, Ring IN
                    # We use relative distance to hand size for robustness
                    hand_size = math.hypot(wrist.x - hand_landmarks.landmark[9].x, wrist.y - hand_landmarks.landmark[9].y)
                    
                    # Thumb is out if far from Index Base
                    thumb_dist = math.hypot(thumb_tip.x - hand_landmarks.landmark[5].x, thumb_tip.y - hand_landmarks.landmark[5].y)
                    thumb_ready = thumb_dist > (hand_size * 0.8)
                    
                    # Pinky is out if straight and far from Ring Base
                    pinky_dist = math.hypot(pinky_tip.x - hand_landmarks.landmark[13].x, pinky_tip.y - hand_landmarks.landmark[13].y)
                    pinky_ready = pinky_straight and (pinky_dist > hand_size * 0.7)

                    is_shaka = (
                        thumb_ready and 
                        pinky_ready and 
                        index_bent and 
                        middle_bent and 
                        ring_bent
                    )

                    if is_shaka and (current_time - last_mic_time > 2.0):
                        mic_active = True
                        last_mic_time = current_time
                        print("🤙 SHAKA Detected -> ORB LISTENING")
                        cv2.putText(image, "ORB: LISTENING", (w//2-100, h//2-50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
                        try:
                            r = requests.post('http://127.0.0.1:5001/api/voice/toggle', json={'active': True}, timeout=2)
                            print(f"   -> SIGNAL SENT: {r.status_code}")
                        except Exception as e:
                            print(f"   -> SIGNAL ERROR: {e}")

                    # -------------------------------------------------
                    # C. OPEN HAND (🖐️) -> MIC OFF
                    # -------------------------------------------------
                    is_open = (
                        index_straight and middle_straight and ring_straight and pinky_straight and not is_pinch
                    )

                    if is_open and (current_time - last_mic_time > 2.0):
                        mic_active = False
                        last_mic_time = current_time
                        print("🖐️ Open Hand -> Sending OFF Signal")
                        try:
                            requests.post('http://127.0.0.1:5001/api/voice/toggle', json={'active': False})
                        except: pass

                    # -------------------------------------------------
                    # D. POINTER (☝️) -> NAVIGATION
                    # -------------------------------------------------
                    is_pointer = (
                        index_straight and 
                        middle_bent and 
                        ring_bent and 
                        pinky_bent and
                        not is_pinch
                    )

                    if is_pointer:
                        cv2.putText(image, "POINTER", (int(index_tip.x * w), int(index_tip.y * h) - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 1)
                        
                        curr_x = index_tip.x
                        if 'prev_pointer_x' not in locals(): prev_pointer_x = curr_x
                        
                        velocity = curr_x - prev_pointer_x
                        
                        if abs(velocity) > 0.08 and (current_time - last_action_time > ACTION_COOLDOWN):
                            if velocity < 0: # Screen Left
                                pyautogui.hotkey('alt', 'tab')
                                cv2.putText(image, "NEXT >>", (w//2, h//2), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,255), 3)
                            else: # Screen Right
                                pyautogui.hotkey('alt', 'shift', 'tab')
                                cv2.putText(image, "<< PREV", (w//2, h//2), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,255), 3)
                            last_action_time = current_time
                        prev_pointer_x = curr_x
                    else:
                        if 'prev_pointer_x' in locals(): del prev_pointer_x

                    # -------------------------------------------------
                    # D. PEACE SIGN CHECK (For Exit)
                    # -------------------------------------------------
                    is_peace = (index_straight and middle_straight and ring_bent and pinky_bent)
                    if is_peace: peace_hand_count += 1

                except Exception as e:
                    pass # Ignore math errors to prevent crash

        # EXIT LOGIC (Double Peace for 2 Seconds)
        if peace_hand_count >= 2:
            if peace_start_time == 0:
                peace_start_time = current_time # Start timer
            
            elapsed = current_time - peace_start_time
            duration = 2.0 # 2 Seconds to Close
            progress = min(elapsed / duration, 1.0)
            
            # Draw Progress Bar
            bar_w = 300
            bar_h = 20
            x = (w - bar_w) // 2
            y = h // 2 + 50
            
            # Background
            cv2.rectangle(image, (x, y), (x + bar_w, y + bar_h), (50, 50, 50), -1)
            # Fill (Red)
            cv2.rectangle(image, (x, y), (x + int(bar_w * progress), y + bar_h), (0, 0, 255), -1)
            # Border
            cv2.rectangle(image, (x, y), (x + bar_w, y + bar_h), (255, 255, 255), 2)
            
            cv2.putText(image, f"HOLD TO CLOSE: {duration-elapsed:.1f}s", (x + 20, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

            if elapsed > duration:
                print("✌️✌️ Double Peace - Closing App...")
                break # EXIT LOOP
        else:
            peace_start_time = 0 # Reset timer if gesture broken

        # UI Overlay

        # UI Overlay
        if mic_active:
            cv2.putText(image, "[MIC ON]", (w//2-50, h-30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            cv2.putText(image, "SHAKA: ON | OPEN: OFF", (10, h-20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)

        # 🛡️ WINDOW STABILITY LOCK
        win_name = 'Bankoo Vision Hub'
        cv2.imshow(win_name, image)
        
        # Ensure window stays at top-left and TopMost to prevent accidental moves
        if 'window_locked' not in locals():
            cv2.moveWindow(win_name, 50, 50) # Pin to top-left
            try:
                cv2.setWindowProperty(win_name, cv2.WND_PROP_TOPMOST, 1)
            except: pass
            window_locked = True
        
        # Exit Check
        key = cv2.waitKey(5) & 0xFF
        if key == 27 or key == ord('q'):
            break

cv2.destroyAllWindows()
cap.release()
