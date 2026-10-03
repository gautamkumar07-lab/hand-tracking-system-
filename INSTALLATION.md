# Installation Guide

## Requirements
- 64-bit Windows, macOS, or Linux desktop
- Python 3.10 or 3.11 recommended
- Webcam and GUI session
- Working camera permissions

## Setup
1. Install Python and enable the option to add it to PATH.
2. Extract the project ZIP.
3. Open a terminal in the `HandTrackingSystem` directory.
4. Create and activate a virtual environment:
   - Windows: `python -m venv .venv` then `.venv\\Scripts\\activate`
   - macOS/Linux: `python3 -m venv .venv` then `source .venv/bin/activate`
5. Install dependencies: `python -m pip install -r requirements.txt`
6. Launch: `python main.py`

## Troubleshooting
- If the webcam does not open, close other apps using it and change `camera_index` in `config.json` to 1 or another available index.
- If MediaPipe fails to install, try Python 3.10/3.11 and update pip.
- On Linux, Tkinter may require your distribution's `python3-tk` package.
- macOS may ask for camera and accessibility permissions.
- Mouse control is off by default. Enable it only after reviewing the safety note.
