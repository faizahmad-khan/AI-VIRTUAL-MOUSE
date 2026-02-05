"""
Unit tests for gesture detection utilities.
"""

import unittest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from combined_ai_mouse import calculate_distance, is_fist_gesture


class TestGestrueDetection(unittest.TestCase):
    """Test cases for gesture detection functions."""
    
    def test_calculate_distance(self):
        """Test distance calculation."""
        # Test with known values
        distance = calculate_distance(0, 0, 3, 4)
        self.assertEqual(distance, 5.0)
        
        # Test with same point
        distance = calculate_distance(10, 10, 10, 10)
        self.assertEqual(distance, 0.0)
        
        # Test with negative coordinates
        distance = calculate_distance(-3, -4, 0, 0)
        self.assertEqual(distance, 5.0)
    
    def test_calculate_distance_float(self):
        """Test distance calculation with float values."""
        distance = calculate_distance(1.5, 2.5, 4.5, 6.5)
        self.assertAlmostEqual(distance, 5.0, places=1)


class MockLandmark:
    """Mock MediaPipe landmark for testing."""
    def __init__(self, x, y):
        self.x = x
        self.y = y


class TestFistGesture(unittest.TestCase):
    """Test fist gesture detection."""
    
    def create_landmarks(self, fingertip_positions):
        """
        Create mock landmarks for testing.
        
        Args:
            fingertip_positions: List of (x, y) tuples for fingertips [8, 12, 16, 20]
        """
        landmarks = [None] * 21
        
        # Palm center (landmark 0)
        landmarks[0] = MockLandmark(0.5, 0.5)
        
        # Fingertips (8, 12, 16, 20)
        landmark_ids = [8, 12, 16, 20]
        for i, (x, y) in enumerate(fingertip_positions):
            landmarks[landmark_ids[i]] = MockLandmark(x, y)
        
        return landmarks
    
    def test_fist_gesture_closed(self):
        """Test that closed fist is detected."""
        # All fingertips close to palm center
        fingertips = [(0.51, 0.51), (0.52, 0.52), (0.51, 0.49), (0.50, 0.48)]
        landmarks = self.create_landmarks(fingertips)
        
        result = is_fist_gesture(landmarks, 640, 480)
        self.assertTrue(result)
    
    def test_fist_gesture_open(self):
        """Test that open hand is not detected as fist."""
        # Fingertips far from palm center
        fingertips = [(0.7, 0.3), (0.8, 0.4), (0.9, 0.5), (0.85, 0.6)]
        landmarks = self.create_landmarks(fingertips)
        
        result = is_fist_gesture(landmarks, 640, 480)
        self.assertFalse(result)
    
    def test_fist_gesture_partial(self):
        """Test that partially closed hand is not detected as fist."""
        # Some fingertips close, some far
        fingertips = [(0.51, 0.51), (0.52, 0.52), (0.8, 0.3), (0.85, 0.4)]
        landmarks = self.create_landmarks(fingertips)
        
        result = is_fist_gesture(landmarks, 640, 480)
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
