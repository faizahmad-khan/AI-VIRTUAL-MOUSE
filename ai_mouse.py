import cv2
import mediapipe as mp
import pyautogui
import numpy as np

# --- CONFIGURATION (Tweak these numbers!) ---
smoothening = 7          # Higher = Smoother but slightly slower (Try 5 to 10)
frame_reduction = 100    # Higher = You move your hand LESS to cover screen
click_distance = 30      # Distance between fingers to trigger click

# Variables for smoothing logic
plocX, plocY = 0, 0      # Previous Location
clocX, clocY = 0, 0      # Current Location

# 1. Setup Camera
cap = cv2.VideoCapture(0)
# Set camera resolution explicitly for better performance
cap.set(3, 640) 
cap.set(4, 480)

screen_width, screen_height = pyautogui.size()

# 2. Setup Hand Detector
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7 
)
mp_draw = mp.solutions.drawing_utils

while True:
    success, frame = cap.read()
    if not success: break
    
    # Flip frame for mirror effect
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    
    # Draw the "Active Area" Box (Visual Guide)
    cv2.rectangle(frame, (frame_reduction, frame_reduction), 
                  (w - frame_reduction, h - frame_reduction), (255, 0, 255), 2)
    
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = hands.process(rgb_frame)
    
    if output.multi_hand_landmarks:
        for hand_landmarks in output.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            landmarks = hand_landmarks.landmark
            
            # --- 1. Get Coordinates ---
            # Index Finger Tip (ID 8)
            index_x = landmarks[8].x * w
            index_y = landmarks[8].y * h
            
            # --- 2. Convert Coordinates (Mapping) ---
            # Map the coordinates from the small box to the full screen
            # np.interp(variable, [min_input, max_input], [min_output, max_output])
            x3 = np.interp(index_x, (frame_reduction, w - frame_reduction), (0, screen_width))
            y3 = np.interp(index_y, (frame_reduction, h - frame_reduction), (0, screen_height))
            
            # --- 3. Apply Smoothing ---
            # Current = Previous + (Target - Previous) / Smoothing Amount
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening
            
            # --- 4. Move Mouse ---
            pyautogui.moveTo(clocX, clocY)
            
            # Update Previous Location for next loop
            plocX, plocY = clocX, clocY

            # --- 5. Clicking Logic ---
            thumb_x = landmarks[4].x * w
            thumb_y = landmarks[4].y * h
            
            # Calculate distance between Index and Thumb
            distance = ((index_x - thumb_x)**2 + (index_y - thumb_y)**2) ** 0.5
            
            if distance < click_distance:
                # Visual feedback for click (Green Circle)
                cv2.circle(frame, (int(index_x), int(index_y)), 15, (0, 255, 0), cv2.FILLED)
                pyautogui.click()
                pyautogui.sleep(0.2) # Avoid double clicks

    cv2.imshow('AI Smooth Mouse', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()