"""
AI Virtual Mouse - A computer vision-based virtual mouse application

This package allows you to control your computer cursor using hand gestures
captured through your webcam. It uses MediaPipe for hand tracking and
PyAutoGUI for mouse control.
"""

__version__ = "1.0.0"
__author__ = "Faiz Ahmad Khan"
__email__ = "your-email@example.com"
__license__ = "MIT"

# Define what gets imported with "from ai_virtual_mouse import *"
__all__ = [
    'main',
    'enhanced_main_with_right_click',
    'add_right_click_functionality',
    'enhanced_main_with_scroll',
    'add_scroll_functionality',
    'enhanced_main_with_drag_drop',
    'add_drag_and_drop_functionality',
]

# Import main modules to make them accessible when importing the package
try:
    from .ai_mouse import main
except ImportError:
    pass

try:
    from .right_click_feature import (
        add_right_click_functionality,
        enhanced_main_with_right_click
    )
except ImportError:
    pass

try:
    from .scroll_feature import (
        add_scroll_functionality,
        enhanced_main_with_scroll
    )
except ImportError:
    pass

try:
    from .drag_drop_feature import (
        add_drag_and_drop_functionality,
        enhanced_main_with_drag_drop
    )
except ImportError:
    pass