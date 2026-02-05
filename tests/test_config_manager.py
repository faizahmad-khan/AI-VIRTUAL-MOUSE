"""
Unit tests for AI Virtual Mouse configuration manager.
"""

import unittest
import tempfile
import yaml
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from config_manager import ConfigManager


class TestConfigManager(unittest.TestCase):
    """Test cases for ConfigManager class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a temporary config file
        self.temp_dir = tempfile.mkdtemp()
        self.config_path = Path(self.temp_dir) / "test_config.yaml"
        
        # Write test configuration
        test_config = {
            'cursor': {
                'smoothening': 5,
                'frame_reduction': 100
            },
            'clicks': {
                'left_click_distance': 30,
                'right_click_distance': 40,
                'double_click_time': 0.3
            },
            'scroll': {
                'threshold': 20,
                'sensitivity': 10,
                'activation_distance': 30
            }
        }
        
        with open(self.config_path, 'w') as f:
            yaml.dump(test_config, f)
    
    def tearDown(self):
        """Clean up test fixtures."""
        if self.config_path.exists():
            self.config_path.unlink()
        Path(self.temp_dir).rmdir()
    
    def test_load_config(self):
        """Test loading configuration from file."""
        config_manager = ConfigManager(self.config_path)
        self.assertIsNotNone(config_manager.config)
        self.assertEqual(config_manager.get('cursor.smoothening'), 5)
    
    def test_get_value(self):
        """Test getting configuration values."""
        config_manager = ConfigManager(self.config_path)
        
        # Test existing key
        self.assertEqual(config_manager.get('cursor.smoothening'), 5)
        self.assertEqual(config_manager.get('clicks.left_click_distance'), 30)
        
        # Test non-existing key with default
        self.assertEqual(config_manager.get('nonexistent.key', 'default'), 'default')
    
    def test_set_value(self):
        """Test setting configuration values."""
        config_manager = ConfigManager(self.config_path)
        
        # Set a value
        config_manager.set('cursor.smoothening', 10)
        self.assertEqual(config_manager.get('cursor.smoothening'), 10)
        
        # Set a new nested value
        config_manager.set('new.section.key', 'value')
        self.assertEqual(config_manager.get('new.section.key'), 'value')
    
    def test_save_config(self):
        """Test saving configuration to file."""
        config_manager = ConfigManager(self.config_path)
        
        # Modify configuration
        config_manager.set('cursor.smoothening', 7)
        config_manager.save_config()
        
        # Load again and verify
        new_config_manager = ConfigManager(self.config_path)
        self.assertEqual(new_config_manager.get('cursor.smoothening'), 7)
    
    def test_get_cursor_settings(self):
        """Test getting cursor settings."""
        config_manager = ConfigManager(self.config_path)
        cursor_settings = config_manager.get_cursor_settings()
        
        self.assertIn('smoothening', cursor_settings)
        self.assertIn('frame_reduction', cursor_settings)
        self.assertEqual(cursor_settings['smoothening'], 5)
    
    def test_get_click_settings(self):
        """Test getting click settings."""
        config_manager = ConfigManager(self.config_path)
        click_settings = config_manager.get_click_settings()
        
        self.assertIn('left_click_distance', click_settings)
        self.assertIn('right_click_distance', click_settings)
        self.assertIn('double_click_time', click_settings)
    
    def test_get_scroll_settings(self):
        """Test getting scroll settings."""
        config_manager = ConfigManager(self.config_path)
        scroll_settings = config_manager.get_scroll_settings()
        
        self.assertIn('threshold', scroll_settings)
        self.assertIn('sensitivity', scroll_settings)
        self.assertIn('activation_distance', scroll_settings)


class TestConfigValidation(unittest.TestCase):
    """Test configuration validation."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.config_path = Path(self.temp_dir) / "test_config.yaml"
    
    def tearDown(self):
        """Clean up test fixtures."""
        if self.config_path.exists():
            self.config_path.unlink()
        Path(self.temp_dir).rmdir()
    
    def test_valid_config(self):
        """Test that valid configuration loads without warnings."""
        valid_config = {
            'cursor': {
                'smoothening': 5,
                'frame_reduction': 100
            }
        }
        
        with open(self.config_path, 'w') as f:
            yaml.dump(valid_config, f)
        
        # Should not raise exception
        config_manager = ConfigManager(self.config_path)
        self.assertIsNotNone(config_manager.config)
    
    def test_missing_file(self):
        """Test behavior when config file is missing."""
        with self.assertRaises(FileNotFoundError):
            ConfigManager(self.config_path)


if __name__ == '__main__':
    unittest.main()
