# Hand Gesture Visualizer (Wayland)

A real-time hand gesture visualization tool for Linux (Wayland) using a webcam.  
This application **does not perform actual mouse clicks**—it visually indicates detected gestures and cursor position.  
Ideal for testing hand-tracking, training gesture recognition, or developing gesture-based interfaces.

---

## Features

- Tracks the **index finger** as a visual cursor.
- Detects common gestures:
  - **Left Click (visual)**
  - **Right Click (visual)**
  - **Double Click (visual)**
- Displays a **green circle** to indicate cursor position.
- Shows a **text label** describing the recognized gesture.
- Real-time display using **PyQt5** and **OpenCV**.
- Fully compatible with **Wayland** sessions.

---

## Requirements

- Python 3.8+
- OpenCV (`opencv-python`)
- Mediapipe (`mediapipe`)
- PyQt5 (`PyQt5`)
- Linux with Wayland
- A working webcam

Install dependencies with:

```bash
pip install opencv-python mediapipe PyQt5
````

---
## Usage

* **Move Cursor**: Move your index finger to control the on-screen cursor.
* **Left Click (visual)**: Index finger near the thumb.
* **Right Click (visual)**: Index finger near the middle finger.
* **Double Click (visual)**: All fingers together.
* The current gesture is displayed as text on the screen, along with a visual cursor.

---

## Notes

* This tool is purely visual; no actual mouse events are triggered.
* It is intended for learning, demonstration, or gesture recognition testing.
* Works best under good lighting conditions with a clear view of the hand.
