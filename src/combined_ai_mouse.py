"""
Combined AI Virtual Mouse with all features:
- Cursor movement with index finger
- Left click with index finger + thumb pinch
- Right click with middle finger + thumb pinch
- Double click detection
- Drag and drop functionality
- Scroll functionality
"""

import cv2
import mediapipe as mp
import pyautogui
import numpy as np


def main():
    """Main function to run the combined AI Virtual Mouse application with all features."""
    
    # --- CONFIGURATION (Tweak these numbers!) ---
    smoothening = 5             # Higher = Smoother but slightly slower (Try 5 to 10)
    frame_reduction = 100        # Higher = You move your hand LESS to cover screen
    click_distance = 30          # Distance between fingers to trigger click
    right_click_distance = 40    # Distance for right-click
    double_click_time = 0.3      # Time in seconds between clicks for double click
    scroll_threshold = 20        # Minimum movement to trigger scroll
    scroll_sensitivity = 10      # How much to scroll per movement
    drag_hold_duration = 1.0     # Duration to hold pinch to initiate drag (in seconds)

    # Variables for smoothing logic
    plocX, plocY = 0, 0      # Previous Location
    clocX, clocY = 0, 0      # Current Location

    # Variables for double click logic
    last_click_time = 0      # Time of last click

    # Variables for scroll logic
    prev_scroll_y = None
    scroll_mode_active = False  # Flag to indicate if we're in scroll mode

    # Variables for drag and drop logic
    pinch_start_time = None
    is_dragging = False
    
    # Variables for click state tracking
    left_click_prev = False  # Track if left click was triggered in previous frame
    right_click_prev = False  # Track if right click was triggered in previous frame

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
                
                # Get coordinates for all relevant fingers
                index_x = landmarks[8].x * w
                index_y = landmarks[8].y * h
                thumb_x = landmarks[4].x * w
                thumb_y = landmarks[4].y * h
                middle_x = landmarks[12].x * w
                middle_y = landmarks[12].y * h
                ring_x = landmarks[16].x * w
                ring_y = landmarks[16].y * h
                
                # Calculate distances between fingers
                index_thumb_distance = ((index_x - thumb_x)**2 + (index_y - thumb_y)**2) ** 0.5
                middle_thumb_distance = ((middle_x - thumb_x)**2 + (middle_y - thumb_y)**2) ** 0.5
                middle_ring_distance = ((middle_x - ring_x)**2 + (middle_y - ring_y)**2) ** 0.5
                
                current_time = pyautogui.time.time()
                
                # Check if scroll mode should be activated (middle + ring fingers together)
                if middle_ring_distance < 30:  # Close together to activate scroll mode
                    scroll_mode_active = True
                    # Disable drag when in scroll mode
                    if is_dragging:
                        pyautogui.mouseUp()
                        is_dragging = False
                        pinch_start_time = None
                    
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
                
                # If not in scroll mode, handle cursor movement and clicks/drag
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

                    # Handle drag and drop functionality
                    if index_thumb_distance < click_distance:
                        # Visual feedback for pinch (Green Circle)
                        cv2.circle(
                            frame, 
                            (int(index_x), int(index_y)), 
                            15, 
                            (0, 255, 0), 
                            cv2.FILLED
                        )
                        
                        if pinch_start_time is None:
                            # Start timing the pinch
                            pinch_start_time = current_time
                        elif not is_dragging and (current_time - pinch_start_time) >= drag_hold_duration:
                            # Initiate drag
                            pyautogui.mouseDown()
                            is_dragging = True
                            # Change visual feedback to indicate drag (Blue Circle)
                            cv2.circle(
                                frame, 
                                (int(index_x), int(index_y)), 
                                20, 
                                (255, 0, 0), 
                                cv2.FILLED
                            )
                    else:
                        # Not pinching anymore
                        if is_dragging:
                            # Release the drag
                            pyautogui.mouseUp()
                            is_dragging = False
                        pinch_start_time = None

                    # Track right-click state to avoid repeated triggering
                    # Handle right click (only when not dragging)
                    if middle_thumb_distance < right_click_distance and not is_dragging and not right_click_prev:
                        # Visual feedback for right click (Red Circle)
                        cv2.circle(
                            frame,
                            (int(middle_x), int(middle_y)),
                            15,
                            (0, 0, 255),  # Red color
                            cv2.FILLED
                        )
                        pyautogui.rightClick()
                        right_click_prev = True  # Mark as triggered to prevent repeated triggering
                    elif middle_thumb_distance >= right_click_distance:
                        right_click_prev = False  # Reset when fingers are apart

                    # Handle left click (only when not dragging and not right clicking)
                    if index_thumb_distance < click_distance and not is_dragging and middle_thumb_distance >= right_click_distance and not left_click_prev:
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
                        left_click_prev = True  # Mark as triggered
                    elif index_thumb_distance >= click_distance:
                        left_click_prev = False  # Reset when fingers are apart

        # Draw instructions on frame
        cv2.putText(frame, "Pinch and hold for 1 sec to drag", (10, h-60), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(frame, "Middle+Ring to scroll, Middle+Thumb for right-click", (10, h-40), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(frame, "Index+Thumb for left click/double-click", (10, h-20), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        cv2.imshow('AI Virtual Mouse - All Features', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Make sure to release mouse if still dragging when quitting
    if is_dragging:
        pyautogui.mouseUp()
    
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    print("Starting AI Virtual Mouse with all features...")
    print("Instructions:")
    print("- Move index finger to move cursor")
    print("- Pinch index finger and thumb for left click")
    print("- Pinch middle finger and thumb for right click")
    print("- Bring middle and ring fingers together for scroll mode")
    print("- Pinch and hold index finger and thumb for 1 second to drag")
    print("- Press 'q' to quit")
    main()