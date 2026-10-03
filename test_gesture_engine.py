import unittest
from gesture_engine import classify_gesture, count_fingers, pinch_distance

class GestureEngineTests(unittest.TestCase):
    def test_invalid_landmarks(self):
        self.assertEqual(classify_gesture([]), "unknown")
        self.assertEqual(count_fingers([]), 0)
        self.assertGreater(pinch_distance([]), .9)

    def test_landmark_count_guard(self):
        self.assertEqual(classify_gesture([(0,0,0)]*5), "unknown")
        self.assertEqual(count_fingers([(0,0,0)]*5), 0)

if __name__ == "__main__":
    unittest.main()
