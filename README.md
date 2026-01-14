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

All required packages are listed in [requirements.txt](requirements.txt).

## 🔧 Installation

1. Clone or download this repository:
   ```bash
   git clone https://github.com/yourusername/ai-virtual-mouse.git
   cd ai-virtual-mouse
   ```

2. Install required packages:
   ```bash
   pip install -r requirements.txt
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

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please make sure to update tests as appropriate and adhere to the code style guidelines.

## 🐛 Issues

If you encounter any bugs or have feature requests, please [open an issue](https://github.com/yourusername/ai-virtual-mouse/issues) with a clear description and reproduction steps.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- MediaPipe for the hand tracking capabilities
- OpenCV for computer vision processing
- PyAutoGUI for mouse control automation
- NumPy for mathematical computations

## 📞 Contact

If you have any questions, feel free to reach out or open an issue in the repository.

## 💰 Support

If this project helped you, consider supporting the development:

[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/)
[![PayPal](https://img.shields.io/badge/PayPal-00457C?style=for-the-badge&logo=paypal&logoColor=white)](https://paypal.me/)

## 🚀 Future Scope

### Future Enhancements & Scalability

**Right-Click Functionality**: Implement a gesture using the Middle Finger (ID 12) and Thumb (ID 4). A "pinch" between these two would trigger a context menu, separating it from the left-click (Index + Thumb).

**Scroll Mode**: Introduce a "Two-Finger Up" state (Index and Middle fingers extended). Mapping the vertical movement of the hand in this state to pyautogui.scroll() would allow for natural webpage navigation.

**Drag & Drop**: Enhance the click logic to detect a "held pinch." If the distance remains small for more than 1 second while moving, the system would execute pyautogui.mouseDown() to drag files and pyautogui.mouseUp() to release them.

**AI Virtual Keyboard**: Integrate a virtual on-screen keyboard that allows users to type by hovering over keys, making the tool a complete hardware replacement for users with physical disabilities.

## 📁 Project Structure
The project is organized as follows:
```
AI VIRTUAL MOUSE/
├── src/                   # Source code files
│   ├── ai_mouse.py        # Main application logic
│   ├── right_click_feature.py    # Right-click functionality
│   ├── scroll_feature.py         # Scroll functionality
│   └── drag_drop_feature.py      # Drag and drop functionality
├── docs/                  # Documentation files
├── tests/                 # Test files (future addition)
├── README.md              # Main project documentation
├── requirements.txt       # Python dependencies
├── setup.py               # Package setup configuration
└── LICENSE              # License information
```