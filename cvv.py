import cv2
import mediapipe as mp
import pyautogui
import math
screen_w, screen_h = pyautogui.size()

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 960)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

def distance(p1, p2):
    return math.hypot(p2[0]-p1[0], p2[1]-p1[1])

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            h, w, _ = frame.shape

            ix = int(hand_landmarks.landmark[8].x * w)
            iy = int(hand_landmarks.landmark[8].y * h)

            tx = int(hand_landmarks.landmark[4].x * w)
            ty = int(hand_landmarks.landmark[4].y * h)

            mx = int(hand_landmarks.landmark[12].x * w)
            my = int(hand_landmarks.landmark[12].y * h)

            cv2.circle(frame, (ix, iy), 10, (0, 255, 0), -1)

            screen_x = int(hand_landmarks.landmark[8].x * screen_w)
            screen_y = int(hand_landmarks.landmark[8].y * screen_h)
            pyautogui.moveTo(screen_x, screen_y)

            if distance((ix, iy), (tx, ty)) < 40:
                cv2.putText(frame, "Click", (ix, iy - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
                pyautogui.click()

            if distance((ix, iy), (mx, my)) < 40:
                cv2.putText(frame, "Right Click", (ix, iy - 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)
                pyautogui.click(button='right')

    cv2.imshow("Hand Mouse Control", frame)
    if cv2.waitKey(1) & 0xFF == 27: 
        break

cap.release()
cv2.destroyAllWindows()

