# Project Structure

## Overview
The AI Virtual Mouse project follows a clean and organized structure that separates source code from configuration and documentation files.

## Directory Structure
```
AI VIRTUAL MOUSE/
├── src/                   # Source code files
│   ├── __init__.py        # Package initialization
│   ├── ai_mouse.py        # Main application logic
│   ├── right_click_feature.py    # Right-click functionality
│   ├── scroll_feature.py         # Scroll functionality  
│   └── drag_drop_feature.py      # Drag and drop functionality
├── docs/                  # Documentation files
│   ├── README.md          # Documentation overview
│   ├── contributing.md    # Contribution guidelines
│   ├── license-details.md # Detailed license information
│   └── project_structure.md # This file
├── tests/                 # Test files (future addition)
├── README.md              # Main project documentation
├── requirements.txt       # Python dependencies
├── setup.py               # Package setup configuration
├── LICENSE              # License information
└── .gitignore           # Git ignore rules
```

## Key Changes
- All source code is now located in the `src/` directory for better organization
- The package can be imported using `from src import ai_mouse` or `import src`
- Entry point in setup.py updated to `src.ai_mouse:main`
- Proper relative imports are used in `__init__.py` to expose public APIs
- Standard files (README.md, LICENSE, requirements.txt) remain in root for visibility