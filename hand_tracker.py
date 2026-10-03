"""MediaPipe/OpenCV frame processing."""
import time
import cv2
import mediapipe as mp
from gesture_engine import classify_gesture, count_fingers, pinch_distance

class HandTracker:
    def __init__(self, max_hands=2, model_complexity=0, detection=0.6, tracking=0.55):
        self.mp_hands = mp.solutions.hands
        self.drawer = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(
            static_image_mode=False, max_num_hands=max(1, min(2, int(max_hands))),
            model_complexity=int(model_complexity),
            min_detection_confidence=float(detection),
            min_tracking_confidence=float(tracking))
        self.prev_time = time.perf_counter()
        self.fps = 0.0

    def process(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.hands.process(rgb)
        hands = []
        if result.multi_hand_landmarks:
            for idx, hand_lms in enumerate(result.multi_hand_landmarks):
                self.drawer.draw_landmarks(frame, hand_lms, self.mp_hands.HAND_CONNECTIONS)
                points = [(lm.x, lm.y, lm.z) for lm in hand_lms.landmark]
                handed = "Right"
                if result.multi_handedness and idx < len(result.multi_handedness):
                    handed = result.multi_handedness[idx].classification[0].label
                gesture = classify_gesture(points, handed)
                fingers = count_fingers(points, handed)
                hands.append({"landmarks": points, "handedness": handed, "gesture": gesture,
                              "finger_count": fingers, "pinch_distance": pinch_distance(points)})
        now = time.perf_counter()
        dt = now - self.prev_time
        if dt > 0:
            current = 1.0 / dt
            self.fps = current if not self.fps else self.fps * .85 + current * .15
        self.prev_time = now
        return frame, hands, self.fps

    def close(self):
        self.hands.close()
