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

SCREEN_W, SCREEN_H = 1920, 1080
CLICK_THRESHOLD, DOUBLE_CLICK_THRESHOLD = 0.04, 0.02

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 960)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

def distance(p1, p2):
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

class CameraWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hand Gesture Visualizer (Wayland)")
        self.label = QLabel(alignment=0x84)
        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        self.gesture_history, self.cursor_pos = deque(maxlen=5), (0, 0)
        self.gesture_text, self.last_time, self.fps = "", time.time(), 0
        self.timer = QTimer(self, timeout=self.update_frame)
        self.timer.start(30)

    def get_stable_gesture(self, gesture):
        self.gesture_history.append(gesture)
        return max(set(self.gesture_history), key=self.gesture_history.count)

    def detect_gesture(self, landmarks):
        ix, iy = landmarks[8].x, landmarks[8].y
        tx, ty = landmarks[4].x, landmarks[4].y
        mx, my = landmarks[12].x, landmarks[12].y
        self.cursor_pos = (int(ix * SCREEN_W), int(iy * SCREEN_H))
        if distance((ix, iy), (tx, ty)) < CLICK_THRESHOLD:
            return "Left Click"
        if distance((ix, iy), (mx, my)) < DOUBLE_CLICK_THRESHOLD:
            return "Double Click"
        if distance((ix, iy), (mx, my)) < CLICK_THRESHOLD:
            return "Right Click"
        return "Move Cursor"

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
            for lm in result.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, lm, mp_hands.HAND_CONNECTIONS)
                gesture = self.detect_gesture(lm.landmark)
        stable_gesture = self.get_stable_gesture(gesture)
        self.gesture_text = stable_gesture
        now = time.time()
        self.fps = int(1 / (now - self.last_time))
        self.last_time = now
        color_map = {
            "Left Click": (0, 255, 0),
            "Right Click": (0, 0, 255),
            "Double Click": (255, 0, 0),
            "Move Cursor": (0, 255, 255),
            "None": (200, 200, 200),
        }
        color = color_map.get(stable_gesture, (255, 255, 255))
        cv2.circle(frame, (int(self.cursor_pos[0] * w / SCREEN_W), int(self.cursor_pos[1] * h / SCREEN_H)), 15, color, -1)
        cv2.putText(frame, self.gesture_text, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
        cv2.putText(frame, f"FPS: {self.fps}", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        qimg = QImage(frame.data, w, h, frame.strides[0], QImage.Format_BGR888)
        self.label.setPixmap(QPixmap.fromImage(qimg))

app = QApplication(sys.argv)
window = CameraWidget()
window.show()
sys.exit(app.exec_())
