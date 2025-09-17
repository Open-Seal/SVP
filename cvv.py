import sys
import os
import cv2
import math
import time
import mediapipe as mp
from collections import deque
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer

os.environ['QT_QPA_PLATFORM'] = 'wayland'

screen_w, screen_h = 1920, 1080
CLICK_THRESHOLD = 0.04

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 960)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

def distance(p1, p2):
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

class CameraWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hand Gesture Visualizer (Wayland)")
        self.label = QLabel()
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)
        self.gesture_text = ""
        self.cursor_pos = (0, 0)
        self.gesture_history = deque(maxlen=5) 
        self.last_time = time.time()
        self.fps = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def get_stable_gesture(self, gesture):
        self.gesture_history.append(gesture)
        return max(set(self.gesture_history), key=self.gesture_history.count)

    def update_frame(self):
        ret, frame = cap.read()
        if not ret:
            return
        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb)
        h, w, _ = frame.shape
        gesture = "None"
        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                ix, iy = hand_landmarks.landmark[8].x, hand_landmarks.landmark[8].y
                tx, ty = hand_landmarks.landmark[4].x, hand_landmarks.landmark[4].y
                mx, my = hand_landmarks.landmark[12].x, hand_landmarks.landmark[12].y
                self.cursor_pos = (int(ix * screen_w), int(iy * screen_h))
                if distance((ix, iy), (tx, ty)) < CLICK_THRESHOLD:
                    gesture = "Left Click"
                elif distance((ix, iy), (mx, my)) < CLICK_THRESHOLD:
                    gesture = "Right Click"
                elif distance((ix, iy), (mx, my)) < 0.02:
                    gesture = "Double Click"
                else:
                    gesture = "Move Cursor"
        stable_gesture = self.get_stable_gesture(gesture)
        self.gesture_text = stable_gesture
        new_time = time.time()
        self.fps = int(1 / (new_time - self.last_time))
        self.last_time = new_time
        color_map = {
            "Left Click": (0, 255, 0),
            "Right Click": (0, 0, 255),
            "Double Click": (255, 0, 0),
            "Move Cursor": (0, 255, 255),
            "None": (200, 200, 200),
        }
        color = color_map.get(stable_gesture, (255, 255, 255))
        cv2.circle(frame, (int(self.cursor_pos[0] * w / screen_w), int(self.cursor_pos[1] * h / screen_h)), 15, color, -1)
        cv2.putText(frame, f"{self.gesture_text}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
        cv2.putText(frame, f"FPS: {self.fps}", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        qimg = QImage(frame.data, w, h, frame.shape[1] * frame.shape[2], QImage.Format_BGR888)
        self.label.setPixmap(QPixmap.fromImage(qimg))

app = QApplication(sys.argv)
window = CameraWidget()
window.show()
sys.exit(app.exec_())
