import cv2
import mediapipe as mp
import pyautogui

# 1. Setup Camera and Screen
cap = cv2.VideoCapture(0)
screen_width, screen_height = pyautogui.size()

# 2. Setup Hand Detector
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils

while True:
    # 3. Read the Frame
    success, frame = cap.read()
    if not success:
        break
    
    frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = hands.process(rgb_frame)
    
    if output.multi_hand_landmarks:
        for hand_landmarks in output.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            landmarks = hand_landmarks.landmark
            
            # --- FIXED SECTION START ---
            
            # Get Index Finger Tip (ID 8) DIRECTLY
            index_tip = landmarks[8]
            index_x = int(index_tip.x * frame_width)
            index_y = int(index_tip.y * frame_height)
            
            # Get Thumb Tip (ID 4) DIRECTLY
            thumb_tip = landmarks[4]
            thumb_x = int(thumb_tip.x * frame_width)
            thumb_y = int(thumb_tip.y * frame_height)

            # Draw circles
            cv2.circle(frame, (index_x, index_y), 10, (0, 255, 255), cv2.FILLED)
            cv2.circle(frame, (thumb_x, thumb_y), 10, (0, 255, 255), cv2.FILLED)
            
            # Move Mouse
            mouse_x = screen_width / frame_width * index_x
            mouse_y = screen_height / frame_height * index_y
            pyautogui.moveTo(mouse_x, mouse_y)
            
            # Check for Click
            if abs(index_y - thumb_y) < 20: 
                pyautogui.click()
                pyautogui.sleep(1) 

            # --- FIXED SECTION END ---

    cv2.imshow('AI Virtual Mouse', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()