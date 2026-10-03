# Architecture

```text
Webcam
  └─ OpenCV frame capture + frame-size controls
      └─ MediaPipe Hands
          ├─ Landmark overlay / multi-hand tracking
          ├─ Gesture engine (finger count, pose heuristics, pinch)
          ├─ Optional mouse / drawing / screenshot controls
          └─ Event logger ── SQLite database ── CSV export
Desktop dashboard (Tkinter) displays camera, gesture, hand count and FPS.
Optional FastAPI service exposes read-only local analytics.
Dataset recorder writes labeled landmark vectors to CSV.
Training script builds a scikit-learn model artifact from collected samples.
```

Modules are separated by responsibility. Webcam inference runs locally; frames are not uploaded. OS-level controls are opt-in or invoked explicitly from the dashboard. SQLite is the default local store.
