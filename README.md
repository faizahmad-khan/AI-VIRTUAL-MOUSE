# AI Virtual Mouse

A computer vision-based virtual mouse application that allows you to control your computer cursor using hand gestures captured through your webcam. This project uses MediaPipe for hand tracking and PyAutoGUI for mouse control.

## 🚀 Features

- **Hand Tracking**: Uses MediaPipe's hand detection model to track finger movements
- **Smooth Cursor Control**: Implements smoothing algorithm for fluid cursor movement
- **Gesture-Based Clicking**: Automatically detects finger pinch gestures for clicking
- **Configurable Settings**: Adjustable parameters for sensitivity and responsiveness

## 🛠️ How It Works

The AI Virtual Mouse tracks your index finger tip to move the cursor and recognizes clicks when your thumb and index finger come close together. The system maps hand movements within a designated area of the camera frame to your entire screen space.

### Key Components:

1. **Hand Detection**: MediaPipe Hands model detects hand landmarks in real-time
2. **Coordinate Mapping**: Maps hand positions from camera frame to screen coordinates
3. **Smoothing Algorithm**: Reduces cursor jitter for smoother movement
4. **Click Detection**: Measures distance between thumb and index finger to trigger clicks

## 📋 Requirements

- Python 3.7 or higher
- OpenCV (`cv2`)
- MediaPipe
- PyAutoGUI
- NumPy

## 🔧 Installation

1. Clone or download this repository:
   ```bash
   git clone https://github.com/yourusername/ai-virtual-mouse.git
   cd ai-virtual-mouse
   ```

2. Install required packages:
   ```bash
   pip install opencv-python mediapipe pyautogui numpy
   ```

## 🎮 Usage

1. Run the script:
   ```bash
   python ai_mouse.py
   ```

2. Position your hand within the purple rectangle shown on the camera feed
3. Move your **index finger** (pointing finger) to control the cursor
4. Bring your **thumb and index finger** together to perform a click
5. Press 'q' to quit the application

## ✋ Hand Gestures

- **Cursor Movement**: Move your index finger (landmark ID 8) within the purple tracking area to move the mouse cursor
- **Left Click**: Touch your thumb (landmark ID 4) to your index finger tip - a green circle will appear as visual feedback
- **Double Click**: Touch your thumb to your index finger tip twice in quick succession (within 0.3 seconds) - a blue circle will appear as visual feedback
- **Active Area**: Keep your hand within the purple rectangle for optimal tracking

## ⚙️ Configuration

The script includes configurable parameters at the top of `ai_mouse.py`:

- `smoothening`: Controls cursor smoothness (higher = smoother but slower response)
- `frame_reduction`: Defines the border area around the screen (higher = less hand movement needed)
- `click_distance`: Distance threshold for detecting clicks (in pixels)
- `double_click_time`: Time threshold for double-click detection (in seconds)

Adjust these values based on your preference and camera setup.

## 📷 Visual Feedback

- **Purple Rectangle**: Active tracking area
- **Green Circle**: Visual feedback when a single click is detected
- **Blue Circle**: Visual feedback when a double-click is detected
- **Hand Landmarks**: Shows tracked hand points in real-time

## ⚠️ Notes

- Ensure good lighting conditions for optimal hand tracking
- The camera should have a clear view of your hand
- Initial calibration might be needed for optimal performance
- The application requires constant camera access

## 🤝 Contributing

Contributions are welcome! Feel free to submit issues or pull requests for improvements.

## 📄 License

This project is open-source and available under the MIT License.