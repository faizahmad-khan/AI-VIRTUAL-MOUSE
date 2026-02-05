# Unit Tests for AI Virtual Mouse

This directory contains unit tests for the AI Virtual Mouse project.

## Running Tests

To run all tests:
```bash
python -m pytest tests/
```

To run a specific test file:
```bash
python -m pytest tests/test_config_manager.py
```

To run with coverage:
```bash
python -m pytest --cov=src tests/
```

## Test Files

- `test_config_manager.py`: Tests for configuration management
- `test_gesture_detection.py`: Tests for gesture detection functions

## Adding New Tests

When adding new features, please add corresponding unit tests to ensure code quality and prevent regressions.
