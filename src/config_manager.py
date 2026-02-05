"""
Configuration Manager for AI Virtual Mouse
Handles loading, saving, and validation of configuration settings.
"""

import yaml
import os
from pathlib import Path
from typing import Any, Dict, Optional
import logging


class ConfigManager:
    """Manages configuration settings for the AI Virtual Mouse application."""
    
    DEFAULT_CONFIG_PATH = Path(__file__).parent.parent / "config.yaml"
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the configuration manager.
        
        Args:
            config_path: Optional path to config file. Uses default if not provided.
        """
        self.config_path = Path(config_path) if config_path else self.DEFAULT_CONFIG_PATH
        self.config: Dict[str, Any] = {}
        self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """
        Load configuration from YAML file.
        
        Returns:
            Dictionary containing configuration settings.
        
        Raises:
            FileNotFoundError: If config file doesn't exist.
            yaml.YAMLError: If config file is malformed.
        """
        try:
            if not self.config_path.exists():
                raise FileNotFoundError(f"Config file not found: {self.config_path}")
            
            with open(self.config_path, 'r') as f:
                self.config = yaml.safe_load(f)
            
            # Validate configuration
            self._validate_config()
            
            logging.info(f"Configuration loaded from {self.config_path}")
            return self.config
            
        except yaml.YAMLError as e:
            logging.error(f"Error parsing config file: {e}")
            raise
        except Exception as e:
            logging.error(f"Error loading config: {e}")
            raise
    
    def save_config(self) -> None:
        """Save current configuration to YAML file."""
        try:
            with open(self.config_path, 'w') as f:
                yaml.dump(self.config, f, default_flow_style=False, sort_keys=False)
            logging.info(f"Configuration saved to {self.config_path}")
        except Exception as e:
            logging.error(f"Error saving config: {e}")
            raise
    
    def _validate_config(self) -> None:
        """Validate configuration values are within acceptable ranges."""
        validations = [
            ('cursor.smoothening', 1, 15),
            ('cursor.frame_reduction', 50, 200),
            ('clicks.left_click_distance', 20, 50),
            ('clicks.right_click_distance', 30, 60),
            ('clicks.double_click_time', 0.1, 0.5),
            ('scroll.threshold', 10, 40),
            ('scroll.sensitivity', 5, 20),
            ('scroll.activation_distance', 20, 50),
            ('drag.hold_duration', 0.5, 2.0),
        ]
        
        for key, min_val, max_val in validations:
            value = self.get(key)
            if value is not None and not (min_val <= value <= max_val):
                logging.warning(f"Config value {key}={value} outside recommended range [{min_val}, {max_val}]")
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value using dot notation.
        
        Args:
            key: Configuration key in dot notation (e.g., 'cursor.smoothening')
            default: Default value if key not found
        
        Returns:
            Configuration value or default
        """
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any) -> None:
        """
        Set a configuration value using dot notation.
        
        Args:
            key: Configuration key in dot notation (e.g., 'cursor.smoothening')
            value: Value to set
        """
        keys = key.split('.')
        config = self.config
        
        # Navigate to the parent dictionary
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        # Set the value
        config[keys[-1]] = value
        logging.debug(f"Config updated: {key} = {value}")
    
    def get_cursor_settings(self) -> Dict[str, Any]:
        """Get cursor-related settings."""
        return {
            'smoothening': self.get('cursor.smoothening', 5),
            'frame_reduction': self.get('cursor.frame_reduction', 100),
        }
    
    def get_click_settings(self) -> Dict[str, Any]:
        """Get click-related settings."""
        return {
            'left_click_distance': self.get('clicks.left_click_distance', 30),
            'right_click_distance': self.get('clicks.right_click_distance', 40),
            'double_click_time': self.get('clicks.double_click_time', 0.3),
        }
    
    def get_scroll_settings(self) -> Dict[str, Any]:
        """Get scroll-related settings."""
        return {
            'threshold': self.get('scroll.threshold', 20),
            'sensitivity': self.get('scroll.sensitivity', 10),
            'activation_distance': self.get('scroll.activation_distance', 30),
        }
    
    def get_drag_settings(self) -> Dict[str, Any]:
        """Get drag-related settings."""
        return {
            'hold_duration': self.get('drag.hold_duration', 1.0),
        }
    
    def get_camera_settings(self) -> Dict[str, Any]:
        """Get camera-related settings."""
        return {
            'device_id': self.get('camera.device_id', 0),
            'width': self.get('camera.width', 640),
            'height': self.get('camera.height', 480),
            'fps': self.get('camera.fps', 30),
        }
    
    def get_hand_detection_settings(self) -> Dict[str, Any]:
        """Get hand detection settings."""
        return {
            'max_num_hands': self.get('hand_detection.max_num_hands', 1),
            'min_detection_confidence': self.get('hand_detection.min_detection_confidence', 0.7),
            'min_tracking_confidence': self.get('hand_detection.min_tracking_confidence', 0.7),
        }
    
    def get_visual_settings(self) -> Dict[str, Any]:
        """Get visual feedback settings."""
        return {
            'show_landmarks': self.get('visual.show_landmarks', True),
            'show_active_area': self.get('visual.show_active_area', True),
            'show_instructions': self.get('visual.show_instructions', True),
            'feedback_circle_size': self.get('visual.feedback_circle_size', 15),
            'colors': self.get('visual.colors', {}),
        }
    
    def get_performance_settings(self) -> Dict[str, Any]:
        """Get performance-related settings."""
        return {
            'enable_fps_counter': self.get('performance.enable_fps_counter', True),
            'log_performance': self.get('performance.log_performance', False),
        }
    
    def get_accessibility_settings(self) -> Dict[str, Any]:
        """Get accessibility settings."""
        return {
            'enable_sound_feedback': self.get('accessibility.enable_sound_feedback', False),
            'enable_pause_gesture': self.get('accessibility.enable_pause_gesture', True),
            'pause_detection_time': self.get('accessibility.pause_detection_time', 2.0),
        }
    
    def reset_to_defaults(self) -> None:
        """Reset configuration to default values."""
        logging.info("Resetting configuration to defaults")
        # This would reload from a default config template
        # For now, just reload the existing config file
        self.load_config()


if __name__ == "__main__":
    # Test the configuration manager
    logging.basicConfig(level=logging.INFO)
    
    config = ConfigManager()
    print("Cursor settings:", config.get_cursor_settings())
    print("Click settings:", config.get_click_settings())
    print("Scroll settings:", config.get_scroll_settings())
    
    # Test set and get
    config.set('cursor.smoothening', 7)
    print("Updated smoothening:", config.get('cursor.smoothening'))
