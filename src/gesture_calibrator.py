"""
Gesture Calibration Mode for AI Virtual Mouse
Helps users calibrate gesture thresholds based on their hand size.
"""

import cv2
import mediapipe as mp
import numpy as np
import yaml
from pathlib import Path
import logging


class GestureCalibrator:
    """Calibrate gesture detection thresholds based on user's hand."""
    
    def __init__(self):
        self.logger = logging.getLogger("gesture_calibrator")
        
        # Storage for measurements
        self.measurements = {
            'pinch_distances': [],
            'open_distances': [],
            'finger_spacings': []
        }
        
        self.calibration_step = 0
        self.max_steps = 5
        
        # Setup MediaPipe
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
        self.mp_draw = mp.solutions.drawing_utils
    
    def calculate_distance(self, x1, y1, x2, y2):
        """Calculate Euclidean distance between two points."""
        return np.sqrt((x1 - x2)**2 + (y1 - y2)**2)
    
    def get_instruction(self):
        """Get current calibration instruction."""
        instructions = [
            "Pinch index finger and thumb together (5 times)",
            "Spread index finger and thumb apart (5 times)",
            "Pinch middle finger and thumb together (5 times)",
            "Bring middle and ring fingers together (5 times)",
            "Open all fingers wide (5 times)"
        ]
        
        if self.calibration_step < len(instructions):
            return instructions[self.calibration_step]
        return "Calibration complete! Press 's' to save or 'q' to quit."
    
    def process_frame(self, frame, landmarks, w, h):
        """Process frame based on current calibration step."""
        if self.calibration_step >= self.max_steps:
            return
        
        # Get relevant landmark positions
        index_x = landmarks[8].x * w
        index_y = landmarks[8].y * h
        thumb_x = landmarks[4].x * w
        thumb_y = landmarks[4].y * h
        middle_x = landmarks[12].x * w
        middle_y = landmarks[12].y * h
        ring_x = landmarks[16].x * w
        ring_y = landmarks[16].y * h
        
        # Measure based on current step
        if self.calibration_step == 0:
            # Pinch measurement (closed)
            distance = self.calculate_distance(index_x, index_y, thumb_x, thumb_y)
            if distance < 50:  # Only record if actually pinching
                self.measurements['pinch_distances'].append(distance)
                cv2.circle(frame, (int(index_x), int(index_y)), 15, (0, 255, 0), cv2.FILLED)
        
        elif self.calibration_step == 1:
            # Open hand measurement
            distance = self.calculate_distance(index_x, index_y, thumb_x, thumb_y)
            if distance > 80:  # Only record if spread apart
                self.measurements['open_distances'].append(distance)
                cv2.circle(frame, (int(index_x), int(index_y)), 15, (255, 0, 0), cv2.FILLED)
        
        elif self.calibration_step == 2:
            # Right-click pinch measurement
            distance = self.calculate_distance(middle_x, middle_y, thumb_x, thumb_y)
            if distance < 60:
                self.measurements['pinch_distances'].append(distance)
                cv2.circle(frame, (int(middle_x), int(middle_y)), 15, (0, 0, 255), cv2.FILLED)
        
        elif self.calibration_step == 3:
            # Scroll gesture measurement
            distance = self.calculate_distance(middle_x, middle_y, ring_x, ring_y)
            if distance < 50:
                self.measurements['finger_spacings'].append(distance)
                avg_x = int((middle_x + ring_x) / 2)
                avg_y = int((middle_y + ring_y) / 2)
                cv2.circle(frame, (avg_x, avg_y), 15, (0, 255, 255), cv2.FILLED)
        
        elif self.calibration_step == 4:
            # Wide open hand
            distance = self.calculate_distance(index_x, index_y, thumb_x, thumb_y)
            self.measurements['open_distances'].append(distance)
    
    def calculate_thresholds(self):
        """Calculate recommended thresholds based on measurements."""
        results = {}
        
        # Calculate left click distance (pinch threshold)
        if self.measurements['pinch_distances']:
            avg_pinch = np.mean(self.measurements['pinch_distances'])
            std_pinch = np.std(self.measurements['pinch_distances'])
            results['left_click_distance'] = int(avg_pinch + std_pinch * 1.5)
        
        # Calculate right click distance
        if len(self.measurements['pinch_distances']) > 5:
            # Use later measurements (from step 2) for right-click
            right_click_pinches = self.measurements['pinch_distances'][5:]
            avg_right = np.mean(right_click_pinches) if right_click_pinches else avg_pinch
            results['right_click_distance'] = int(avg_right + std_pinch * 1.5)
        
        # Calculate scroll activation distance
        if self.measurements['finger_spacings']:
            avg_spacing = np.mean(self.measurements['finger_spacings'])
            std_spacing = np.std(self.measurements['finger_spacings'])
            results['scroll_activation_distance'] = int(avg_spacing + std_spacing * 1.5)
        
        return results
    
    def save_calibration(self, config_path=None):
        """Save calibrated values to config file."""
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config.yaml"
        
        thresholds = self.calculate_thresholds()
        
        try:
            # Load existing config
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            
            # Update with calibrated values
            if 'left_click_distance' in thresholds:
                config['clicks']['left_click_distance'] = thresholds['left_click_distance']
            if 'right_click_distance' in thresholds:
                config['clicks']['right_click_distance'] = thresholds['right_click_distance']
            if 'scroll_activation_distance' in thresholds:
                config['scroll']['activation_distance'] = thresholds['scroll_activation_distance']
            
            # Save back to file
            with open(config_path, 'w') as f:
                yaml.dump(config, f, default_flow_style=False, sort_keys=False)
            
            self.logger.info(f"Calibration saved: {thresholds}")
            return True, thresholds
        
        except Exception as e:
            self.logger.error(f"Failed to save calibration: {e}")
            return False, None
    
    def run(self):
        """Run the calibration process."""
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        print("=" * 60)
        print("GESTURE CALIBRATION MODE")
        print("=" * 60)
        print("Follow the on-screen instructions to calibrate gestures.")
        print("Press SPACE to move to next step")
        print("Press 's' to save calibration")
        print("Press 'q' to quit without saving")
        print("=" * 60)
        
        try:
            while True:
                success, frame = cap.read()
                if not success:
                    break
                
                frame = cv2.flip(frame, 1)
                h, w, _ = frame.shape
                
                # Process frame
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                output = self.hands.process(rgb_frame)
                
                # Display instruction
                instruction = self.get_instruction()
                cv2.putText(frame, instruction, (10, 40), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                
                # Display step progress
                step_text = f"Step {self.calibration_step + 1}/{self.max_steps}"
                cv2.putText(frame, step_text, (10, 80), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                
                # Display measurement count for current step
                if self.calibration_step < self.max_steps:
                    if self.calibration_step in [0, 2]:
                        count = len(self.measurements['pinch_distances']) % 5
                    elif self.calibration_step in [1, 4]:
                        count = len(self.measurements['open_distances']) % 5
                    elif self.calibration_step == 3:
                        count = len(self.measurements['finger_spacings'])
                    
                    cv2.putText(frame, f"Measurements: {count}/5", (10, 120), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
                
                # Process hand landmarks
                if output.multi_hand_landmarks:
                    for hand_landmarks in output.multi_hand_landmarks:
                        self.mp_draw.draw_landmarks(
                            frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                        
                        self.process_frame(frame, hand_landmarks.landmark, w, h)
                
                # Display help
                cv2.putText(frame, "SPACE: Next | 's': Save | 'q': Quit", (10, h-20), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
                
                cv2.imshow('Gesture Calibration', frame)
                
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    print("Calibration cancelled")
                    break
                elif key == ord(' '):
                    if self.calibration_step < self.max_steps:
                        self.calibration_step += 1
                        print(f"Moving to step {self.calibration_step + 1}")
                elif key == ord('s'):
                    if self.calibration_step >= self.max_steps:
                        success, thresholds = self.save_calibration()
                        if success:
                            print("\n" + "=" * 60)
                            print("Calibration saved successfully!")
                            print("Recommended thresholds:")
                            for key, value in thresholds.items():
                                print(f"  {key}: {value}")
                            print("=" * 60)
                        else:
                            print("Failed to save calibration")
                        break
                    else:
                        print("Complete all calibration steps first!")
        
        finally:
            cap.release()
            cv2.destroyAllWindows()
            self.hands.close()


def main():
    """Run calibration tool."""
    logging.basicConfig(level=logging.INFO)
    calibrator = GestureCalibrator()
    calibrator.run()


if __name__ == "__main__":
    main()
