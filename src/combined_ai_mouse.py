"""
Combined AI Virtual Mouse with all features:
- Cursor movement with index finger
- Left click with index finger + thumb pinch
- Right click with middle finger + thumb pinch
- Double click detection
- Drag and drop functionality
- Scroll functionality
- Configuration management
- Error handling and logging
- Pause/resume functionality
"""

import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time
import logging
from pathlib import Path
import sys

# Import custom modules
try:
    from config_manager import ConfigManager
    from logger_setup import setup_logger, PerformanceLogger
except ImportError:
    # Fallback if modules not in same directory
    sys.path.append(str(Path(__file__).parent))
    from config_manager import ConfigManager
    from logger_setup import setup_logger, PerformanceLogger


def calculate_distance(x1, y1, x2, y2):
    """Calculate Euclidean distance between two points."""
    return ((x1 - x2)**2 + (y1 - y2)**2) ** 0.5


def is_fist_gesture(landmarks, w, h):
    """
    Detect fist gesture for pause/resume.
    Returns True if all fingertips are close to palm.
    """
    # Get palm center (landmark 0)
    palm_x = landmarks[0].x * w
    palm_y = landmarks[0].y * h
    
    # Check if all fingertips (8, 12, 16, 20) are close to palm
    fingertips = [8, 12, 16, 20]  # Index, middle, ring, pinky
    threshold = 80  # Distance threshold for fist detection
    
    for tip_id in fingertips:
        tip_x = landmarks[tip_id].x * w
        tip_y = landmarks[tip_id].y * h
        distance = calculate_distance(palm_x, palm_y, tip_x, tip_y)
        if distance > threshold:
            return False
    
    return True


def main():
    """Main function to run the combined AI Virtual Mouse application with all features."""
    
    # Load configuration
    try:
        config = ConfigManager()
        logger = setup_logger(
            log_file=config.get('logging.file', 'logs/ai_mouse.log'),
            level=config.get('logging.level', 'INFO'),
            max_bytes=config.get('logging.max_file_size', 10485760),
            backup_count=config.get('logging.backup_count', 3),
            console=config.get('logging.console', True)
        )
        logger.info("=" * 60)
        logger.info("AI Virtual Mouse starting...")
        logger.info("=" * 60)
    except Exception as e:
        print(f"Error loading configuration: {e}")
        print("Using default settings...")
        # Fallback to default settings
        logger = setup_logger()
        config = None
    
    # Performance logger
    perf_logger = PerformanceLogger(logger)
    
    # Load settings from config or use defaults
    if config:
        cursor_settings = config.get_cursor_settings()
        click_settings = config.get_click_settings()
        scroll_settings = config.get_scroll_settings()
        drag_settings = config.get_drag_settings()
        camera_settings = config.get_camera_settings()
        hand_settings = config.get_hand_detection_settings()
        visual_settings = config.get_visual_settings()
        perf_settings = config.get_performance_settings()
        accessibility_settings = config.get_accessibility_settings()
        
        smoothening = cursor_settings['smoothening']
        frame_reduction = cursor_settings['frame_reduction']
        click_distance = click_settings['left_click_distance']
        right_click_distance = click_settings['right_click_distance']
        double_click_time = click_settings['double_click_time']
        scroll_threshold = scroll_settings['threshold']
        scroll_sensitivity = scroll_settings['sensitivity']
        scroll_activation_distance = scroll_settings['activation_distance']
        drag_hold_duration = drag_settings['hold_duration']
    else:
        # Default values
        smoothening = 5
        frame_reduction = 100
        click_distance = 30
        right_click_distance = 40
        double_click_time = 0.3
        scroll_threshold = 20
        scroll_sensitivity = 10
        scroll_activation_distance = 30
        drag_hold_duration = 1.0
        perf_settings = {'enable_fps_counter': True}
        visual_settings = {'show_landmarks': True, 'show_active_area': True, 'show_instructions': True}
        accessibility_settings = {'enable_pause_gesture': True, 'pause_detection_time': 2.0}
    
    logger.info(f"Settings loaded - Smoothening: {smoothening}, Frame reduction: {frame_reduction}")

    logger.info(f"Settings loaded - Smoothening: {smoothening}, Frame reduction: {frame_reduction}")

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
    
    # Variables for pause/resume functionality
    is_paused = False
    fist_start_time = None
    pause_gesture_enabled = accessibility_settings.get('enable_pause_gesture', True)
    pause_detection_time = accessibility_settings.get('pause_detection_time', 2.0)
    
    # Variables for FPS calculation
    fps = 0
    frame_time = 0
    prev_time = time.time()

    # 1. Setup Camera
    try:
        if config:
            camera_id = camera_settings['device_id']
            cam_width = camera_settings['width']
            cam_height = camera_settings['height']
        else:
            camera_id = 0
            cam_width = 640
            cam_height = 480
        
        cap = cv2.VideoCapture(camera_id)
        
        if not cap.isOpened():
            logger.error(f"Failed to open camera with ID {camera_id}")
            raise RuntimeError(f"Cannot access camera {camera_id}")
        
        # Set camera resolution explicitly for better performance
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, cam_width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, cam_height)
        
        logger.info(f"Camera initialized: {cam_width}x{cam_height}")
    except Exception as e:
        logger.error(f"Camera initialization error: {e}")
        raise

    screen_width, screen_height = pyautogui.size()
    logger.info(f"Screen resolution: {screen_width}x{screen_height}")

    # 2. Setup Hand Detector
    try:
        mp_hands = mp.solutions.hands
        if config:
            hands = mp_hands.Hands(
                static_image_mode=False,
                max_num_hands=hand_settings['max_num_hands'],
                min_detection_confidence=hand_settings['min_detection_confidence'],
                min_tracking_confidence=hand_settings['min_tracking_confidence']
            )
        else:
            hands = mp_hands.Hands(
                static_image_mode=False,
                max_num_hands=1,
                min_detection_confidence=0.7,
                min_tracking_confidence=0.7
            )
        mp_draw = mp.solutions.drawing_utils
        logger.info("Hand detector initialized successfully")
    except Exception as e:
        logger.error(f"Hand detector initialization error: {e}")
        cap.release()
        raise

    logger.info("Starting main loop...")
    
    try:
        while True:
            loop_start_time = time.time()
            
            success, frame = cap.read()
            if not success:
                logger.warning("Failed to read frame from camera")
                break
            
            # Flip frame for mirror effect
            frame = cv2.flip(frame, 1)
            h, w, _ = frame.shape
        
            # Display pause status
            if is_paused:
                cv2.putText(frame, "PAUSED - Make fist for 2 sec to resume", (10, 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            
            # Draw the "Active Area" Box (Visual Guide)
            if visual_settings.get('show_active_area', True):
                cv2.rectangle(
                    frame, 
                    (frame_reduction, frame_reduction), 
                    (w - frame_reduction, h - frame_reduction), 
                    tuple(visual_settings.get('colors', {}).get('active_area', [255, 0, 255])),
                    2
                )
            
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            output = hands.process(rgb_frame)
            
            if output.multi_hand_landmarks:
                for hand_landmarks in output.multi_hand_landmarks:
                    # Draw landmarks if enabled
                    if visual_settings.get('show_landmarks', True):
                        mp_draw.draw_landmarks(
                            frame, 
                            hand_landmarks, 
                            mp_hands.HAND_CONNECTIONS
                        )
                    
                    landmarks = hand_landmarks.landmark
                    
                    # Check for fist gesture (pause/resume)
                    if pause_gesture_enabled:
                        if is_fist_gesture(landmarks, w, h):
                            if fist_start_time is None:
                                fist_start_time = time.time()
                            elif time.time() - fist_start_time >= pause_detection_time:
                                is_paused = not is_paused
                                fist_start_time = None
                                logger.info(f"Application {'paused' if is_paused else 'resumed'}")
                                # Release mouse if paused while dragging
                                if is_paused and is_dragging:
                                    pyautogui.mouseUp()
                                    is_dragging = False
                        else:
                            fist_start_time = None
                    
                    # Skip gesture processing if paused
                    if is_paused:
                        continue
                    
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
                index_thumb_distance = calculate_distance(index_x, index_y, thumb_x, thumb_y)
                middle_thumb_distance = calculate_distance(middle_x, middle_y, thumb_x, thumb_y)
                middle_ring_distance = calculate_distance(middle_x, middle_y, ring_x, ring_y)
                
                current_time = time.time()
                
                # Check if scroll mode should be activated (middle + ring fingers together)
                if middle_ring_distance < scroll_activation_distance:  # Close together to activate scroll mode
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

            # Draw FPS counter
            if perf_settings.get('enable_fps_counter', True):
                curr_time = time.time()
                fps = 1 / (curr_time - prev_time) if (curr_time - prev_time) > 0 else 0
                prev_time = curr_time
                cv2.putText(frame, f"FPS: {int(fps)}", (w-120, 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            # Draw instructions on frame
            if visual_settings.get('show_instructions', True):
                cv2.putText(frame, "Pinch and hold for 1 sec to drag", (10, h-80), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                cv2.putText(frame, "Middle+Ring to scroll, Middle+Thumb for right-click", (10, h-60), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                cv2.putText(frame, "Index+Thumb for left click/double-click", (10, h-40), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                cv2.putText(frame, "Make fist for 2 sec to pause/resume", (10, h-20), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            # Log performance
            if perf_settings.get('log_performance', False):
                perf_logger.log_frame(time.time() - loop_start_time)

            cv2.imshow('AI Virtual Mouse - All Features', frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                logger.info("User requested quit")
                break
            elif key == ord('p') and not pause_gesture_enabled:
                is_paused = not is_paused
                logger.info(f"Application {'paused' if is_paused else 'resumed'} (keyboard)")
    
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
    except Exception as e:
        logger.error(f"Unexpected error in main loop: {e}", exc_info=True)
    finally:
        # Make sure to release mouse if still dragging when quitting
        if is_dragging:
            try:
                pyautogui.mouseUp()
            except:
                pass
        
        # Cleanup resources
        try:
            cap.release()
            cv2.destroyAllWindows()
            hands.close()
            logger.info("Application closed successfully")
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")


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