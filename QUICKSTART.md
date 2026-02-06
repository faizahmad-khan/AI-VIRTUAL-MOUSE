# AI Virtual Mouse - Quick Start Guide

## Installation

1. **Clone the repository:**
   ```bash
   cd "AI VIRTUAL MOUSE"
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## First Time Setup

### 1. Calibrate Gestures (Recommended)

Run the calibration tool to optimize gesture detection for your hand:

```bash
python src/gesture_calibrator.py
```

Follow the on-screen instructions:
- Perform each gesture 5 times
- Press SPACE to move to the next step
- Press 's' to save calibration when complete

### 2. Configure Settings (Optional)

Launch the configuration GUI to adjust settings:

```bash
python src/config_gui.py
```

You can adjust:
- Cursor smoothness and sensitivity
- Click detection thresholds
- Scroll behavior
- Visual feedback
- Camera settings

## Running the Application

### Basic Usage

```bash
python src/combined_ai_mouse.py
```

### Gesture Controls

| Gesture | Action |
|---------|--------|
| Move index finger | Move cursor |
| Index + Thumb pinch | Left click |
| Index + Thumb double pinch | Double click |
| Middle + Thumb pinch | Right click |
| Middle + Ring fingers together + Move | Scroll |
| Index + Thumb pinch and hold (1 sec) | Drag and drop |
| Make fist for 2 seconds | Pause/Resume |
| Press 'q' | Quit application |

## Configuration File

Settings are stored in `config.yaml`. You can edit this file directly or use the GUI.

Key settings to adjust:
- `cursor.smoothening`: Higher = smoother cursor (5-15)
- `cursor.frame_reduction`: Control how much hand movement covers the screen
- `clicks.left_click_distance`: Pinch sensitivity for clicking

## Troubleshooting

### Camera not working
- Check that no other application is using the camera
- Try changing `camera.device_id` in config.yaml (usually 0 or 1)

### Gestures not responding
- Run the calibration tool to adjust for your hand size
- Ensure good lighting conditions
- Keep your hand within the purple rectangle
- Adjust distance thresholds in config.yaml or GUI

### Cursor too sensitive/slow
- Adjust `cursor.smoothening` (higher = smoother but slower)
- Adjust `cursor.frame_reduction` (higher = less hand movement needed)

## Logs

Application logs are stored in `logs/ai_mouse.log` for troubleshooting.

## Running Tests

To verify installation:

```bash
python -m pytest tests/
```

## Advanced Features

- **FPS Counter**: Enabled by default (top-right corner)
- **Logging**: Check `logs/ai_mouse.log` for detailed information
- **Pause Mode**: Make a fist for 2 seconds to pause/resume tracking
- **Error Recovery**: Application gracefully handles camera disconnections

## Support

For issues or questions, check:
- Logs in `logs/ai_mouse.log`
- README.md for detailed documentation
- Configuration file comments in `config.yaml`
