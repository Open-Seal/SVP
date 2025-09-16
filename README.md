# Hand Gesture Visualizer (Wayland)

[![Build](https://img.shields.io/badge/build-passing-brightgreen)]()
[![License](https://img.shields.io/badge/license-MIT-blue)]()
[![Platform](https://img.shields.io/badge/platform-Python%203.8%2B-blue)]()



A real-time **hand gesture visualization tool** for Linux Wayland using a webcam.  
This app **does not trigger real mouse events** — it only shows detected gestures and a visual cursor.  
Useful for **gesture tracking experiments**, **recognition training**, and **prototype gesture-based interfaces**.

---

## Features

- Tracks the **index fingertip** as a virtual cursor.  
- Recognizes gestures:
  - **Left Click (visual)** → index finger near thumb  
  - **Right Click (visual)** → index finger near middle finger  
  - **Double Click (visual)** → fingers close together  
  - **Move Cursor** → free index finger movement  
- Visual feedback:
  - Colored circle showing cursor position  
  - Text label with the detected gesture  
- Runs in **real time** with PyQt5 + OpenCV  
- Designed for **Wayland sessions on Linux**  

---

## Requirements

- Python **3.8+**  
- [OpenCV](https://pypi.org/project/opencv-python/)  
- [Mediapipe](https://pypi.org/project/mediapipe/)  
- [PyQt5](https://pypi.org/project/PyQt5/)  
- Linux with **Wayland**  
- A working **webcam**  

Install dependencies:

```bash
pip install opencv-python mediapipe PyQt5
````

---

## Usage

* **Move Cursor** → move index finger freely
* **Left Click (visual)** → bring index finger close to thumb
* **Right Click (visual)** → bring index finger close to middle finger
* **Double Click (visual)** → fingers close together

The app shows the detected gesture and a visual cursor in the camera window.

---

## Notes

* No real mouse control is performed — this is a **visualization only**.
* Best results with **good lighting** and a clear view of the hand.
* Intended for **learning, demos, and testing gesture recognition**.

