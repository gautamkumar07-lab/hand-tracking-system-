"""Application controller and desktop entry point."""
import csv
import json
import os
import time
from datetime import datetime
import cv2
import numpy as np
import tkinter as tk
from tkinter import messagebox
from hand_tracker import HandTracker
from dashboard import Dashboard
from controls import SystemControls
import database

CONFIG_PATH = "config.json"

class App:
    def __init__(self):
        with open(CONFIG_PATH, encoding="utf-8") as f:
            self.config = json.load(f)
        self.root = tk.Tk()
        self.controls = SystemControls()
        self.tracker = None
        self.camera = None
        self.running = True
        self.drawing = False
        self.recording = False
        self.label = self.config.get("gesture_label", "open_palm")
        self.last_click = 0.0
        self.last_gesture = ""
        self.last_event_time = 0.0
        self.draw_layer = None
        self.prev_point = None
        self.dashboard = Dashboard(self.root, self)
        database.init_db()
        os.makedirs("data/screenshots", exist_ok=True)
        os.makedirs("models", exist_ok=True)
        self._start_camera()
        self.root.after(10, self.tick)

    def _start_camera(self):
        self.camera = cv2.VideoCapture(int(self.config.get("camera_index", 0)))
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, int(self.config.get("frame_width", 960)))
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, int(self.config.get("frame_height", 540)))
        if not self.camera.isOpened():
            messagebox.showerror("Webcam unavailable", "Could not open the webcam. Check permissions and camera_index in config.json.")
            self.running = False
            self.root.after(100, self.root.destroy)
            return
        self.tracker = HandTracker(self.config.get("max_hands",2), self.config.get("model_complexity",0),
                                   self.config.get("min_detection_confidence",.6), self.config.get("min_tracking_confidence",.55))

    def set_mouse(self, enabled):
        result = self.controls.set_mouse_enabled(enabled)
        if enabled and not result:
            messagebox.showwarning("Mouse control unavailable", "PyAutoGUI is not available. Install requirements and check desktop permissions.")
        database.log_event("mouse_control", details=f"enabled={result}")
    def set_drawing(self, enabled):
        self.drawing = enabled
        self.prev_point = None
        database.log_event("drawing_mode", details=f"enabled={enabled}")
    def set_recording(self, enabled):
        self.recording = enabled
        database.log_event("dataset_recording", details=f"enabled={enabled},label={self.label}")
    def set_label(self, label):
        self.label = "".join(c for c in label.strip() if c.isalnum() or c in "_-")[:40] or "unlabeled"
    def screenshot(self):
        if getattr(self, "last_frame", None) is None:
            messagebox.showinfo("Screenshot", "No camera frame is available yet."); return
        path = f"data/screenshots/hand_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        cv2.imwrite(path, self.last_frame)
        database.log_event("screenshot", details=path)
        messagebox.showinfo("Screenshot saved", f"Saved to {path}")
    def export_analytics(self):
        path = database.export_csv()
        messagebox.showinfo("Analytics exported", f"Saved to {path}")
    def volume(self, level):
        ok, message = self.controls.set_volume(level)
        database.log_event("volume_control", details=message)
        messagebox.showinfo("Volume control", message)
    def brightness(self, level):
        ok, message = self.controls.set_brightness(level)
        database.log_event("brightness_control", details=message)
        messagebox.showinfo("Brightness control", message)
    def tick(self):
        if not self.running: return
        if self.camera and self.tracker:
            ok, frame = self.camera.read()
            if ok:
                frame = cv2.flip(frame, 1)
                frame, hands, fps = self.tracker.process(frame)
                self.last_frame = frame.copy()
                if self.draw_layer is None or self.draw_layer.shape != frame.shape:
                    self.draw_layer = np.zeros_like(frame)
                if self.drawing and hands:
                    points = hands[0]["landmarks"]
                    # Draw while index is raised and other three fingers are folded.
                    x, y = int(points[8][0]*frame.shape[1]), int(points[8][1]*frame.shape[0])
                    if points[8][1] < points[6][1] and points[12][1] > points[10][1]:
                        if self.prev_point:
                            cv2.line(self.draw_layer, self.prev_point, (x,y), (100,210,255), 4)
                        self.prev_point = (x,y)
                    else: self.prev_point = None
                    frame = cv2.addWeighted(frame, 1, self.draw_layer, .8, 0)
                if hands:
                    first = hands[0]
                    cv2.putText(frame, f"{first['gesture']} | {first['finger_count']} fingers", (18,35),
                                cv2.FONT_HERSHEY_SIMPLEX, .8, (90,240,170), 2)
                    if self.controls.mouse_enabled:
                        p = first["landmarks"][8]
                        self.controls.move_cursor(1-p[0], p[1])
                        pinching = first["pinch_distance"] < .045
                        now = time.monotonic()
                        if pinching and now-self.last_click > .45:
                            self.controls.click(); self.last_click=now
                            database.log_event("gesture_click", first["gesture"], first["finger_count"], fps)
                    if first["gesture"] != self.last_gesture and time.monotonic()-self.last_event_time > .7:
                        database.log_event("gesture_detected", first["gesture"], first["finger_count"], fps)
                        self.last_gesture = first["gesture"]; self.last_event_time=time.monotonic()
                    if self.recording:
                        path = "data/gesture_dataset.csv"
                        new_file = not os.path.exists(path)
                        with open(path,"a",newline="",encoding="utf-8") as f:
                            writer=csv.writer(f)
                            if new_file: writer.writerow(["label"]+[f"x{i}" for i in range(21)]+[f"y{i}" for i in range(21)]+[f"z{i}" for i in range(21)])
                            writer.writerow([self.label]+[round(p[0],6) for p in first["landmarks"]]+[round(p[1],6) for p in first["landmarks"]]+[round(p[2],6) for p in first["landmarks"]])
                self.dashboard.update(frame, hands, fps)
        self.root.after(1, self.tick)
    def stop(self):
        self.running = False
        try:
            if self.camera: self.camera.release()
            if self.tracker: self.tracker.close()
            self.controls.mouse_up()
        finally:
            self.root.destroy()
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    App().run()
