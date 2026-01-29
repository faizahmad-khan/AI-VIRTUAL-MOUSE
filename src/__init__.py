"""
AI Virtual Mouse - A computer vision-based virtual mouse application

This package allows you to control your computer cursor using hand gestures
captured through your webcam. It uses MediaPipe for hand tracking and
PyAutoGUI for mouse control.

Features:
- Cursor movement with index finger
- Left click with index finger + thumb pinch
- Right click with middle finger + thumb pinch
- Double click detection
- Drag and drop functionality
- Scroll functionality
"""

__version__ = "1.0.0"
__author__ = "Faiz Ahmad Khan"
__license__ = "MIT"

# Define what gets imported with "from ai_virtual_mouse import *"
__all__ = ['main']

# Import main modules to make them accessible when importing the package
try:
    from .combined_ai_mouse import main
except ImportError:
    pass