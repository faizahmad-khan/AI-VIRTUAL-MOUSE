"""
Configuration GUI for AI Virtual Mouse
Provides a graphical interface to adjust settings in real-time.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import yaml
from pathlib import Path
from config_manager import ConfigManager
import logging


class ConfigGUI:
    """GUI for configuring AI Virtual Mouse settings."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("AI Virtual Mouse - Configuration")
        self.root.geometry("800x700")
        self.root.resizable(True, True)
        
        # Load configuration
        try:
            self.config_manager = ConfigManager()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load configuration: {e}")
            return
        
        self.create_widgets()
        self.load_values()
    
    def create_widgets(self):
        """Create all GUI widgets."""
        # Create notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create tabs
        cursor_frame = ttk.Frame(notebook)
        clicks_frame = ttk.Frame(notebook)
        scroll_frame = ttk.Frame(notebook)
        drag_frame = ttk.Frame(notebook)
        camera_frame = ttk.Frame(notebook)
        visual_frame = ttk.Frame(notebook)
        accessibility_frame = ttk.Frame(notebook)
        
        notebook.add(cursor_frame, text="Cursor")
        notebook.add(clicks_frame, text="Clicks")
        notebook.add(scroll_frame, text="Scroll")
        notebook.add(drag_frame, text="Drag")
        notebook.add(camera_frame, text="Camera")
        notebook.add(visual_frame, text="Visual")
        notebook.add(accessibility_frame, text="Accessibility")
        
        # Store widget references
        self.widgets = {}
        
        # === CURSOR TAB ===
        self.create_slider(cursor_frame, "Smoothening:", "cursor.smoothening", 1, 15, 0)
        self.create_slider(cursor_frame, "Frame Reduction:", "cursor.frame_reduction", 50, 200, 1)
        
        # === CLICKS TAB ===
        self.create_slider(clicks_frame, "Left Click Distance:", "clicks.left_click_distance", 20, 50, 0)
        self.create_slider(clicks_frame, "Right Click Distance:", "clicks.right_click_distance", 30, 60, 1)
        self.create_slider(clicks_frame, "Double Click Time (sec):", "clicks.double_click_time", 0.1, 0.5, 2, resolution=0.01)
        
        # === SCROLL TAB ===
        self.create_slider(scroll_frame, "Scroll Threshold:", "scroll.threshold", 10, 40, 0)
        self.create_slider(scroll_frame, "Scroll Sensitivity:", "scroll.sensitivity", 5, 20, 1)
        self.create_slider(scroll_frame, "Activation Distance:", "scroll.activation_distance", 20, 50, 2)
        
        # === DRAG TAB ===
        self.create_slider(drag_frame, "Hold Duration (sec):", "drag.hold_duration", 0.5, 2.0, 0, resolution=0.1)
        
        # === CAMERA TAB ===
        self.create_slider(camera_frame, "Device ID:", "camera.device_id", 0, 3, 0)
        self.create_slider(camera_frame, "Width:", "camera.width", 320, 1920, 1)
        self.create_slider(camera_frame, "Height:", "camera.height", 240, 1080, 2)
        self.create_slider(camera_frame, "FPS:", "camera.fps", 15, 60, 3)
        
        # === VISUAL TAB ===
        self.create_checkbox(visual_frame, "Show Hand Landmarks", "visual.show_landmarks", 0)
        self.create_checkbox(visual_frame, "Show Active Area", "visual.show_active_area", 1)
        self.create_checkbox(visual_frame, "Show Instructions", "visual.show_instructions", 2)
        self.create_slider(visual_frame, "Feedback Circle Size:", "visual.feedback_circle_size", 10, 30, 3)
        
        # === ACCESSIBILITY TAB ===
        self.create_checkbox(accessibility_frame, "Enable Pause Gesture", "accessibility.enable_pause_gesture", 0)
        self.create_slider(accessibility_frame, "Pause Detection Time:", "accessibility.pause_detection_time", 1.0, 3.0, 1, resolution=0.1)
        
        # === BUTTONS ===
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Button(button_frame, text="Save Configuration", command=self.save_config).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Reset to Defaults", command=self.reset_defaults).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Reload", command=self.reload_config).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Close", command=self.root.quit).pack(side='right', padx=5)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side='bottom', fill='x')
    
    def create_slider(self, parent, label, config_key, min_val, max_val, row, resolution=1):
        """Create a slider widget with label and value display."""
        frame = ttk.Frame(parent)
        frame.grid(row=row, column=0, sticky='ew', padx=20, pady=10)
        parent.columnconfigure(0, weight=1)
        
        # Label
        ttk.Label(frame, text=label, width=25).pack(side='left')
        
        # Value display
        value_var = tk.DoubleVar()
        value_label = ttk.Label(frame, textvariable=value_var, width=8)
        value_label.pack(side='right', padx=5)
        
        # Slider
        slider = ttk.Scale(
            frame, 
            from_=min_val, 
            to=max_val, 
            variable=value_var, 
            orient='horizontal',
            length=300
        )
        slider.pack(side='right', padx=5)
        
        # Store reference
        self.widgets[config_key] = value_var
        
        return value_var
    
    def create_checkbox(self, parent, label, config_key, row):
        """Create a checkbox widget."""
        frame = ttk.Frame(parent)
        frame.grid(row=row, column=0, sticky='w', padx=20, pady=10)
        parent.columnconfigure(0, weight=1)
        
        var = tk.BooleanVar()
        checkbox = ttk.Checkbutton(frame, text=label, variable=var)
        checkbox.pack(side='left')
        
        # Store reference
        self.widgets[config_key] = var
        
        return var
    
    def load_values(self):
        """Load values from configuration into widgets."""
        for key, widget_var in self.widgets.items():
            value = self.config_manager.get(key)
            if value is not None:
                widget_var.set(value)
    
    def save_config(self):
        """Save configuration from widgets."""
        try:
            # Update config manager with widget values
            for key, widget_var in self.widgets.items():
                value = widget_var.get()
                self.config_manager.set(key, value)
            
            # Save to file
            self.config_manager.save_config()
            
            self.status_var.set("Configuration saved successfully!")
            messagebox.showinfo("Success", "Configuration saved successfully!\n\nRestart the application for changes to take effect.")
        except Exception as e:
            self.status_var.set(f"Error saving configuration: {e}")
            messagebox.showerror("Error", f"Failed to save configuration:\n{e}")
    
    def reset_defaults(self):
        """Reset configuration to default values."""
        if messagebox.askyesno("Confirm Reset", "Are you sure you want to reset all settings to defaults?"):
            try:
                self.config_manager.reset_to_defaults()
                self.load_values()
                self.status_var.set("Configuration reset to defaults")
                messagebox.showinfo("Success", "Configuration reset to defaults!")
            except Exception as e:
                self.status_var.set(f"Error resetting configuration: {e}")
                messagebox.showerror("Error", f"Failed to reset configuration:\n{e}")
    
    def reload_config(self):
        """Reload configuration from file."""
        try:
            self.config_manager.load_config()
            self.load_values()
            self.status_var.set("Configuration reloaded from file")
        except Exception as e:
            self.status_var.set(f"Error reloading configuration: {e}")
            messagebox.showerror("Error", f"Failed to reload configuration:\n{e}")


def main():
    """Launch the configuration GUI."""
    root = tk.Tk()
    app = ConfigGUI(root)
    root.mainloop()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
