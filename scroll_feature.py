"""
Implementation of scroll functionality for AI Virtual Mouse
using two-finger up/down gestures.
"""

import cv2
import mediapipe as mp
import pyautogui
import numpy as np


def add_scroll_functionality():
    """
    This function demonstrates how to add scroll functionality
    using two-finger up/down gestures.
    """
    
    # Configuration for scrolling
    scroll_threshold = 20  # Minimum movement to trigger scroll
    scroll_sensitivity = 10  # How much to scroll per movement
    
    # Initialize MediaPipe Hands
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=2,  # Allow up to 2 hands for two-finger gesture
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7
    )
    
    # Start camera
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)
    
    # Variables to track previous positions for scroll calculation
    prev_middle_y = None
    prev_index_y = None
    
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
                
                # Get coordinates for index (8) and middle (12) fingers
                index_x = int(landmarks[8].x * w)
                index_y = int(landmarks[8].y * h)
                middle_x = int(landmarks[12].x * w)
                middle_y = int(landmarks[12].y * h)
                
                # Draw circles on index and middle fingers
                cv2.circle(frame, (index_x, index_y), 10, (255, 0, 0), cv2.FILLED)
                cv2.circle(frame, (middle_x, middle_y), 10, (255, 0, 0), cv2.FILLED)
                
                # Calculate average y position of both fingers
                avg_finger_y = (index_y + middle_y) / 2
                
                # If we have previous position data, calculate scroll
                if prev_middle_y is not None and prev_index_y is not None:
                    prev_avg_y = (prev_index_y + prev_middle_y) / 2
                    scroll_delta = prev_avg_y - avg_finger_y  # Positive = upward movement
                    
                    # Only scroll if movement exceeds threshold
                    if abs(scroll_delta) > scroll_threshold:
                        scroll_amount = int(scroll_delta / scroll_sensitivity)
                        if scroll_amount != 0:
                            pyautogui.scroll(scroll_amount)
                
                # Update previous positions
                prev_index_y = index_y
                prev_middle_y = middle_y
        else:
            # Reset previous positions when no hands are detected
            prev_index_y = None
            prev_middle_y = None
        
        cv2.imshow('Scroll Demo', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()


# Alternative approach: Enhanced version with scroll functionality
def enhanced_main_with_scroll():
    """Enhanced main function with scroll functionality added."""
    
    # --- CONFIGURATION (Tweak these numbers!) ---
    smoothening = 8          # Higher = Smoother but slightly slower (Try 5 to 10)
    frame_reduction = 100    # Higher = You move your hand LESS to cover screen
    click_distance = 30      # Distance between fingers to trigger click
    right_click_distance = 40  # Distance for right-click
    double_click_distance = 40  # Distance between fingers to trigger double click
    double_click_time = 0.3     # Time in seconds between clicks for double click
    scroll_threshold = 20       # Minimum movement to trigger scroll
    scroll_sensitivity = 10     # How much to scroll per movement

    # Variables for smoothing logic
    plocX, plocY = 0, 0      # Previous Location
    clocX, clocY = 0, 0      # Current Location

    # Variables for double click logic
    last_click_time = 0      # Time of last click

    # Variables for scroll logic
    prev_scroll_y = None
    scroll_mode_active = False  # Flag to indicate if we're in scroll mode

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
        max_num_hands=1,  # We'll still use one hand for this implementation
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
                
                # Get coordinates for all relevant fingers
                index_x = landmarks[8].x * w
                index_y = landmarks[8].y * h
                thumb_x = landmarks[4].x * w
                thumb_y = landmarks[4].y * h
                middle_x = landmarks[12].x * w
                middle_y = landmarks[12].y * h
                ring_x = landmarks[16].x * w
                ring_y = landmarks[16].y * h
                
                # Calculate distance between index and thumb for left click
                index_thumb_distance = ((index_x - thumb_x)**2 + (index_y - thumb_y)**2) ** 0.5
                
                # Calculate distance between middle and thumb for right click
                middle_thumb_distance = ((middle_x - thumb_x)**2 + (middle_y - thumb_y)**2) ** 0.5
                
                # Calculate distance between middle and ring for scroll mode activation
                middle_ring_distance = ((middle_x - ring_x)**2 + (middle_y - ring_y)**2) ** 0.5
                
                # Check if scroll mode should be activated (middle + ring fingers together)
                if middle_ring_distance < 30:  # Close together to activate scroll mode
                    scroll_mode_active = True
                    # Visual feedback for scroll mode (Yellow circle)
                    avg_x = int((middle_x + ring_x) / 2)
                    avg_y = int((middle_y + ring_y) / 2)
                    cv2.circle(frame, (avg_x, avg_y), 15, (0, 255, 255), cv2.FILLED)
                    
                    # Handle scrolling
                    if prev_scroll_y is not None:
                        scroll_delta = prev_scroll_y - middle_y  # Positive = upward movement
                        
                        # Only scroll if movement exceeds threshold
                        if abs(scroll_delta) > scroll_threshold:
                            scroll_amount = int(scroll_delta / scroll_sensitivity)
                            if scroll_amount != 0:
                                pyautogui.scroll(scroll_amount)
                    
                    # Update previous position for next scroll calculation
                    prev_scroll_y = middle_y
                else:
                    scroll_mode_active = False
                    prev_scroll_y = None  # Reset for next scroll session
                
                # If not in scroll mode, handle cursor movement and clicks
                if not scroll_mode_active:
                    # --- 1. Convert Coordinates (Mapping) ---
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
                    
                    # --- 2. Apply Smoothing ---
                    # Current = Previous + (Target - Previous) / Smoothing Amount
                    clocX = plocX + (x3 - plocX) / smoothening
                    clocY = plocY + (y3 - plocY) / smoothening
                    
                    # --- 3. Move Mouse ---
                    pyautogui.moveTo(clocX, clocY)
                    
                    # Update Previous Location for next loop
                    plocX, plocY = clocX, clocY

                    # Handle clicks only when not in scroll mode
                    if middle_thumb_distance < right_click_distance:
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
                    elif index_thumb_distance < click_distance:
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

        cv2.imshow('AI Smooth Mouse with Scroll', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    print("Demonstrating scroll functionality...")
    add_scroll_functionality()