import sys
import cv2
import mediapipe as mp
import math
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer
screen_w, screen_h = 1920, 1080

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 960)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

CLICK_THRESHOLD = 0.04

def distance(p1, p2):
    return math.hypot(p2[0]-p1[0], p2[1]-p1[1])

class CameraWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hand Gesture Visualizer (Wayland)")
        self.label = QLabel()
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)
        self.gesture_text = ""
        self.cursor_pos = (0,0)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def update_frame(self):
        ret, frame = cap.read()
        if not ret:
            return

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb)

        h, w, _ = frame.shape
        self.gesture_text = ""

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                ix = hand_landmarks.landmark[8].x
                iy = hand_landmarks.landmark[8].y
                self.cursor_pos = (int(ix*screen_w), int(iy*screen_h))

                tx = hand_landmarks.landmark[4].x
                ty = hand_landmarks.landmark[4].y
                mx = hand_landmarks.landmark[12].x
                my = hand_landmarks.landmark[12].y
                if distance((ix, iy), (tx, ty)) < CLICK_THRESHOLD:
                    self.gesture_text = "Left Click (visual)"
                elif distance((ix, iy), (mx, my)) < CLICK_THRESHOLD:
                    self.gesture_text = "Right Click (visual)"
                else:
                    finger_dist = distance((ix, iy), (mx, my))
                    if finger_dist < 0.02:
                        self.gesture_text = "Double Click (visual)"
                    else:
                        self.gesture_text = "Move Cursor"
        cv2.circle(frame, (int(self.cursor_pos[0]*w/screen_w), int(self.cursor_pos[1]*h/screen_h)), 15, (0,255,0), -1)
        cv2.putText(frame, self.gesture_text, (10,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
        bytes_per_line = frame.shape[1] * frame.shape[2]
        qimg = QImage(frame.data, w, h, bytes_per_line, QImage.Format_BGR888)
        self.label.setPixmap(QPixmap.fromImage(qimg))
import os
os.environ['QT_QPA_PLATFORM'] = 'wayland'

app = QApplication(sys.argv)
window = CameraWidget()
window.show()
sys.exit(app.exec_())
