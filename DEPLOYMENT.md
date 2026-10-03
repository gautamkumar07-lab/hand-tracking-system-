# Deployment Guide

## Desktop distribution
This app requires a local webcam and graphical desktop, so deploy it as a desktop application rather than a headless web service.

1. Validate on each target OS and Python version.
2. Create a clean virtual environment and install pinned/validated dependencies.
3. Keep `config.json` editable for camera and performance settings.
4. Include `data/` as a writable per-user application-data directory in a packaged installer.
5. Optionally package with PyInstaller after validating MediaPipe model assets: `pyinstaller --noconfirm --windowed --name HandTrackingSystem main.py`.
6. Test camera permissions, screenshot storage, CSV export, and mouse failsafe on target devices.

## Analytics API
Run locally using Uvicorn. Bind to `127.0.0.1` by default. Do not expose this demo API publicly without authentication, HTTPS, monitoring, rate limits, and access controls.

## Production hardening checklist
- Lock and audit dependencies; build repeatable installers.
- Add automated CI on Windows/macOS/Linux.
- Test gesture accuracy against a representative dataset.
- Add consent notices and retention controls for datasets and analytics.
- Validate keyboard/mouse accessibility and emergency stop.
- Add API authentication if remote access is needed.
