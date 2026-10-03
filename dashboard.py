"""Tkinter desktop dashboard."""
import tkinter as tk
from tkinter import ttk, messagebox
import cv2
from PIL import Image, ImageTk

class Dashboard:
    def __init__(self, root, controller):
        self.root, self.controller = root, controller
        root.title("Hand Tracking System | Control Center")
        root.geometry("1120x760")
        root.minsize(820, 600)
        root.configure(bg="#f3f5fb")
        style = ttk.Style()
        try: style.theme_use("clam")
        except Exception: pass
        style.configure("TFrame", background="#f3f5fb")
        style.configure("Card.TFrame", background="#ffffff")
        style.configure("TLabel", background="#f3f5fb", foreground="#22243a", font=("Segoe UI", 10))
        style.configure("Title.TLabel", font=("Segoe UI", 22, "bold"))
        style.configure("CardTitle.TLabel", background="#ffffff", font=("Segoe UI", 11, "bold"))
        header = ttk.Frame(root, padding=(22,18)); header.pack(fill="x")
        ttk.Label(header, text="Hand Tracking System", style="Title.TLabel").pack(side="left")
        ttk.Label(header, text="COMPUTER VISION CONTROL CENTER").pack(side="right")
        body = ttk.Frame(root, padding=(18,0,18,18)); body.pack(fill="both", expand=True)
        left = ttk.Frame(body, style="Card.TFrame", padding=14); left.pack(side="left", fill="both", expand=True)
        right = ttk.Frame(body, style="Card.TFrame", padding=16); right.pack(side="right", fill="y", padx=(14,0))
        ttk.Label(left, text="Live camera preview", style="CardTitle.TLabel").pack(anchor="w", pady=(0,10))
        self.preview = ttk.Label(left, text="Starting webcam…", background="#181a2a", foreground="#fff", anchor="center")
        self.preview.pack(fill="both", expand=True)
        self.status = ttk.Label(left, text="Initializing…", background="#fff")
        self.status.pack(anchor="w", pady=(10,0))
        ttk.Label(right, text="CONTROL PANEL", style="CardTitle.TLabel").pack(anchor="w", pady=(0,12))
        self.gesture = tk.StringVar(value="Gesture: —")
        self.fingers = tk.StringVar(value="Fingers: 0")
        self.fps = tk.StringVar(value="FPS: 0")
        self.hands = tk.StringVar(value="Hands detected: 0")
        for var in (self.gesture,self.fingers,self.fps,self.hands):
            ttk.Label(right, textvariable=var, background="#ffffff").pack(anchor="w", pady=6)
        ttk.Separator(right).pack(fill="x", pady=12)
        self.mouse_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(right, text="Enable mouse control", variable=self.mouse_var,
                        command=lambda: self.controller.set_mouse(self.mouse_var.get())).pack(anchor="w", pady=5)
        self.draw_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(right, text="Virtual drawing board", variable=self.draw_var,
                        command=lambda: self.controller.set_drawing(self.draw_var.get())).pack(anchor="w", pady=5)
        self.record_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(right, text="Record gesture dataset", variable=self.record_var,
                        command=lambda: self.controller.set_recording(self.record_var.get())).pack(anchor="w", pady=5)
        self.label_var = tk.StringVar(value="open_palm")
        ttk.Label(right, text="Dataset label", background="#fff").pack(anchor="w", pady=(12,3))
        ttk.Entry(right, textvariable=self.label_var, width=24).pack(fill="x")
        ttk.Button(right, text="Set label", command=lambda: self.controller.set_label(self.label_var.get())).pack(fill="x", pady=(5,10))
        ttk.Button(right, text="Capture screenshot", command=self.controller.screenshot).pack(fill="x", pady=4)
        ttk.Button(right, text="Export analytics CSV", command=self.controller.export_analytics).pack(fill="x", pady=4)
        ttk.Button(right, text="Volume up", command=lambda: self.controller.volume(75)).pack(fill="x", pady=4)
        ttk.Button(right, text="Brightness 75%", command=lambda: self.controller.brightness(75)).pack(fill="x", pady=4)
        ttk.Button(right, text="Quit", command=self.controller.stop).pack(fill="x", pady=(14,0))
        self.root.protocol("WM_DELETE_WINDOW", self.controller.stop)

    def update(self, frame, hands, fps):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(rgb)
        max_w, max_h = 760, 560
        image.thumbnail((max_w, max_h))
        photo = ImageTk.PhotoImage(image=image)
        self.preview.configure(image=photo, text="")
        self.preview.image = photo
        self.gesture.set("Gesture: " + (hands[0]["gesture"] if hands else "no hand"))
        self.fingers.set("Fingers: " + (str(hands[0]["finger_count"]) if hands else "0"))
        self.fps.set(f"FPS: {fps:.1f}")
        self.hands.set(f"Hands detected: {len(hands)}")
        self.status.configure(text="Camera active · processing locally")
