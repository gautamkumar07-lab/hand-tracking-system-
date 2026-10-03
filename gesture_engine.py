"""Rule-based gesture classification and finger counting."""
from typing import Dict, List, Tuple

FINGER_TIPS = (8, 12, 16, 20)
FINGER_PIPS = (6, 10, 14, 18)

def count_fingers(landmarks: List[Tuple[float, float, float]], handedness: str = "Right") -> int:
    """Count extended fingers from normalized MediaPipe landmarks."""
    if not landmarks or len(landmarks) < 21:
        return 0
    count = sum(1 for tip, pip in zip(FINGER_TIPS, FINGER_PIPS)
                if landmarks[tip][1] < landmarks[pip][1])
    # Thumb extension is approximate and depends on handedness/camera mirroring.
    thumb_tip, thumb_ip = landmarks[4], landmarks[3]
    if (handedness.lower() == "right" and thumb_tip[0] < thumb_ip[0]) or \
       (handedness.lower() != "right" and thumb_tip[0] > thumb_ip[0]):
        count += 1
    return count

def classify_gesture(landmarks: List[Tuple[float, float, float]], handedness: str = "Right") -> str:
    """Return a readable gesture label using a lightweight heuristic."""
    if not landmarks or len(landmarks) < 21:
        return "unknown"
    fingers = [landmarks[t][1] < landmarks[p][1] for t, p in zip(FINGER_TIPS, FINGER_PIPS)]
    extended = sum(fingers)
    thumb_extended = count_fingers(landmarks, handedness) > extended
    if extended == 4 and thumb_extended:
        return "open_palm"
    if extended == 0 and not thumb_extended:
        # Distinguish a rough thumbs-up pose.
        if landmarks[4][1] < landmarks[3][1] and all(landmarks[t][1] > landmarks[p][1] for t,p in zip(FINGER_TIPS,FINGER_PIPS)):
            return "thumbs_up"
        return "fist"
    if fingers[0] and fingers[1] and not fingers[2] and not fingers[3]:
        return "peace"
    if fingers[0] and not any(fingers[1:]):
        return "pointing"
    if extended >= 3:
        return "open_palm"
    return "unknown"

def pinch_distance(landmarks: List[Tuple[float, float, float]]) -> float:
    if not landmarks or len(landmarks) < 21:
        return 1.0
    dx = landmarks[4][0] - landmarks[8][0]
    dy = landmarks[4][1] - landmarks[8][1]
    return (dx*dx + dy*dy) ** 0.5
