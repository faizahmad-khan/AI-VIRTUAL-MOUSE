import cv2
import mediapipe as mp
import pyautogui

# 1. Setup Camera and Screen
cap = cv2.VideoCapture(0) # 0 is usually the default webcam
screen_width, screen_height = pyautogui.size() # Get your monitor size

# 2. Setup Hand Detector (MediaPipe)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,           # We only want to track one hand
    min_detection_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils

while True:
    # 3. Read the Frame
    success, frame = cap.read()
    if not success:
        break
    
    # Flip the frame horizontally so it acts like a mirror (intuitive movement)
    frame = cv2.flip(frame, 1)
    
    # Get frame dimensions
    frame_height, frame_width, _ = frame.shape
    
    # Convert BGR image to RGB for MediaPipe processing
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Process the frame to find hands
    output = hands.process(rgb_frame)
    
    hands_detected = output.multi_hand_landmarks
    
    if hands_detected:
        for hand_landmarks in hands_detected:
            # Draw the hand skeleton on the video
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            # 4. Get Landmark Coordinates
            landmarks = hand_landmarks.landmark
            
            for id, landmark in enumerate(landmarks):
                # ID 8 is the Index Finger Tip
                if id == 8:
                    x = int(landmark.x * frame_width)
                    y = int(landmark.y * frame_height)
                    
                    # Draw a circle on the index finger
                    cv2.circle(frame, (x, y), 10, (0, 255, 255), cv2.FILLED)
                    
                    # 5. Move Mouse
                    # Map the camera coordinates to screen coordinates
                    # using simple proportion
                    mouse_x = screen_width / frame_width * x
                    mouse_y = screen_height / frame_height * y
                    
                    pyautogui.moveTo(mouse_x, mouse_y)
                
                # ID 4 is the Thumb Tip
                if id == 4:
                    thumb_x = int(landmark.x * frame_width)
                    thumb_y = int(landmark.y * frame_height)
                    
                    # Draw a circle on the thumb
                    cv2.circle(frame, (thumb_x, thumb_y), 10, (0, 255, 255), cv2.FILLED)
                    
                    # 6. Check for Click (Distance between Index and Thumb)
                    # Simple math: difference between x and y coordinates
                    if abs(thumb_y - y) < 20: 
                        pyautogui.click()
                        pyautogui.sleep(1) # Sleep to avoid double clicking instantly

    # Show the video feed window
    cv2.imshow('AI Virtual Mouse', frame)
    
    # Press 'q' on keyboard to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()