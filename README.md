# Hand Tracking System
Advanced Computer Vision System | Python · OpenCV · MediaPipe

A modular desktop prototype for webcam hand tracking, gesture recognition, mouse interaction, virtual drawing, capture tools, analytics, and a local SQLite event log.

## Features mapped to the 20 contributions
1. Webcam integration — OpenCV camera capture.
2. Hand detection — MediaPipe Hands landmarks.
3. Multi-hand tracking — configurable tracking of up to two hands.
4. Finger counting — thumb and finger extension heuristic.
5. Gesture recognition — open palm, fist, peace, thumbs-up, pointing.
6. Mouse control — optional PyAutoGUI integration.
7. Cursor tracking — index-finger mapped to screen coordinates.
8. Drag and drop — pinch-and-hold interaction (optional mouse control).
9. Click detection — pinch gesture / click cooldown.
10. Screenshot capture — save annotated camera frame to `data/screenshots/`.
11. FPS monitor — live FPS estimate on preview.
12. Landmark visualization — hand skeleton and landmark overlay.
13. Volume control — optional OS adapter; safely reports if unsupported.
14. Brightness control — optional `screen_brightness_control` adapter.
15. Virtual drawing board — index-finger drawing mode.
16. Gesture dataset generator — records landmark vectors to CSV.
17. Training module — trains a small scikit-learn gesture classifier from CSV.
18. GUI dashboard — Tkinter control panel and live video preview.
19. Performance optimization — configurable frame width, model complexity, and detection confidence.
20. Analytics logging — SQLite event log and CSV export.

## Quick start
Recommended: Python 3.10 or 3.11. A webcam and a desktop session are required for live tracking.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python main.py
```

If MediaPipe installation fails, use Python 3.10/3.11 and a compatible 64-bit environment. Camera index can be changed in Settings or `config.json`.

## Run the API (optional)
```bash
pip install -r requirements-api.txt
uvicorn revive_api:app --host 127.0.0.1 --port 8000
```
API docs are at `http://127.0.0.1:8000/docs`.

## Dataset and model
1. Start the desktop app and enable **Record dataset**.
2. Choose a label, e.g. `open_palm`, `fist`, `peace`.
3. Collect samples with varied hand positions and lighting.
4. Run `python train_model.py --csv data/gesture_dataset.csv --output models/gesture_model.joblib`.
5. The model is optional; the application has built-in heuristic gestures.

## Safety and privacy
Frames are processed locally. No video is uploaded. Mouse control is disabled by default and must be enabled by the user. Keep control disabled while collecting data or when other applications could be affected. Volume/brightness features depend on OS permissions and compatible optional packages.

## Repository structure
```text
HandTrackingSystem/
├── main.py
├── hand_tracker.py
├── gesture_engine.py
├── controls.py
├── database.py
├── dashboard.py
├── revive_api.py
├── train_model.py
├── config.json
├── requirements.txt
├── requirements-api.txt
├── docs/
│   ├── API.md
│   ├── INSTALLATION.md
│   ├── DEPLOYMENT.md
│   └── ARCHITECTURE.md
├── screenshots/
│   └── dashboard-preview.svg
├── data/
│   └── .gitkeep
├── models/
│   └── .gitkeep
└── tests/
    └── test_gesture_engine.py
```

## Scope
This is a runnable portfolio-grade prototype, not a certified production system. OS-level mouse, volume, and brightness control varies by platform; the webcam and GUI require a local desktop session. For production use, add signed installers, device permission UX, automated cross-platform testing, model evaluation, access controls for the API, and privacy review.
