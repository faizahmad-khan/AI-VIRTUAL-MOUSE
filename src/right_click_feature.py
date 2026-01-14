"""
Implementation of right-click functionality for AI Virtual Mouse
using middle finger + thumb pinch gesture.
"""

import cv2
import mediapipe as mp
import pyautogui
import numpy as np


def add_right_click_functionality():
    """
    This function demonstrates how to add right-click functionality
    using middle finger (landmark 12) and thumb (landmark 4) pinch.
    """
    
    # Configuration for right-click
    right_click_distance = 40  # Distance threshold for right-click
    
    # Initialize MediaPipe Hands
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7
    )
    
    # Start camera
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)
    
    while True:
        success, frame = cap.read()
        if not success:
            break
            
        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape
        
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        output = hands.process(rgb_frame)
        
        if output.multi_hand_landmarks:
            for hand_landmarks in output.multi_hand_landmarks:
                landmarks = hand_landmarks.landmark
                
                # Get coordinates for thumb (4) and middle finger (12)
                thumb_x = landmarks[4].x * w
                thumb_y = landmarks[4].y * h
                middle_x = landmarks[12].x * w
                middle_y = landmarks[12].y * h
                
                # Calculate distance between thumb and middle finger
                middle_thumb_distance = ((thumb_x - middle_x)**2 + (thumb_y - middle_y)**2) ** 0.5
                
                # Right-click detection
                if middle_thumb_distance < right_click_distance:
                    # Visual feedback for right-click (Red Circle)
                    cv2.circle(
                        frame, 
                        (int(middle_x), int(middle_y)), 
                        15, 
                        (0, 0, 255),  # Red color
                        cv2.FILLED
                    )
                    pyautogui.rightClick()
                    pyautogui.sleep(0.3)  # Prevent rapid right clicks
        
        cv2.imshow('Right-Click Demo', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()


# Alternative approach: Enhanced version of the original ai_mouse.py with right-click
def enhanced_main_with_right_click():
    """Enhanced main function with right-click functionality added."""
    
    # --- CONFIGURATION (Tweak these numbers!) ---
    smoothening = 8          # Higher = Smoother but slightly slower (Try 5 to 10)
    frame_reduction = 100    # Higher = You move your hand LESS to cover screen
    click_distance = 30      # Distance between fingers to trigger click
    right_click_distance = 40  # Distance for right-click
    double_click_distance = 40  # Distance between fingers to trigger double click
    double_click_time = 0.3     # Time in seconds between clicks for double click

    # Variables for smoothing logic
    plocX, plocY = 0, 0      # Previous Location
    clocX, clocY = 0, 0      # Current Location

    # Variables for double click logic
    last_click_time = 0      # Time of last click

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
        if not success:
            break
        
        # Flip frame for mirror effect
        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape
        
        # Draw the "Active Area" Box (Visual Guide)
        cv2.rectangle(
            frame, 
            (frame_reduction, frame_reduction), 
            (w - frame_reduction, h - frame_reduction), 
            (255, 0, 255), 
            2
        )
        
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        output = hands.process(rgb_frame)
        
        if output.multi_hand_landmarks:
            for hand_landmarks in output.multi_hand_landmarks:
                mp_draw.draw_landmarks(
                    frame, 
                    hand_landmarks, 
                    mp_hands.HAND_CONNECTIONS
                )
                
                landmarks = hand_landmarks.landmark
                
                # --- 1. Get Coordinates ---
                # Index Finger Tip (ID 8)
                index_x = landmarks[8].x * w
                index_y = landmarks[8].y * h
                
                # --- 2. Convert Coordinates (Mapping) ---
                # Map coordinates from camera frame to screen
                x3 = np.interp(
                    index_x,
                    (frame_reduction, w - frame_reduction),
                    (0, screen_width)
                )
                y3 = np.interp(
                    index_y,
                    (frame_reduction, h - frame_reduction),
                    (0, screen_height)
                )
                
                # --- 3. Apply Smoothing ---
                # Current = Previous + (Target - Previous) / Smoothing Amount
                clocX = plocX + (x3 - plocX) / smoothening
                clocY = plocY + (y3 - plocY) / smoothening
                
                # --- 4. Move Mouse ---
                pyautogui.moveTo(clocX, clocY)
                
                # Update Previous Location for next loop
                plocX, plocY = clocX, clocY

                # --- 5. Left Clicking Logic ---
                thumb_x = landmarks[4].x * w
                thumb_y = landmarks[4].y * h
                
                # Calculate distance between Index and Thumb
                distance = (
                    (index_x - thumb_x)**2 + 
                    (index_y - thumb_y)**2
                ) ** 0.5
                
                # Calculate distance between Middle Finger and Thumb for right-click
                middle_x = landmarks[12].x * w
                middle_y = landmarks[12].y * h
                right_distance = (
                    (middle_x - thumb_x)**2 + 
                    (middle_y - thumb_y)**2
                ) ** 0.5
                
                # Check for right-click first to avoid conflicts
                if right_distance < right_click_distance:
                    # Visual feedback for right click (Red Circle)
                    cv2.circle(
                        frame, 
                        (int(middle_x), int(middle_y)), 
                        15, 
                        (0, 0, 255),  # Red color
                        cv2.FILLED
                    )
                    pyautogui.rightClick()
                    pyautogui.sleep(0.3)  # Avoid unintended rapid right clicks
                elif distance < click_distance:
                    # Check for double click
                    current_time = pyautogui.time.time()
                    if current_time - last_click_time < double_click_time:
                        # Visual feedback for double click (Blue Circle)
                        cv2.circle(
                            frame, 
                            (int(index_x), int(index_y)), 
                            15, 
                            (255, 0, 0), 
                            cv2.FILLED
                        )
                        pyautogui.doubleClick()
                        last_click_time = 0  # Reset to prevent triple-click
                    else:
                        # Visual feedback for single click (Green Circle)
                        cv2.circle(
                            frame, 
                            (int(index_x), int(index_y)), 
                            15, 
                            (0, 255, 0), 
                            cv2.FILLED
                        )
                        pyautogui.click()
                        last_click_time = current_time
                    pyautogui.sleep(0.2)  # Avoid unintended rapid clicks

        cv2.imshow('AI Smooth Mouse with Right-Click', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    print("Demonstrating right-click functionality...")
    add_right_click_functionality()