# Hand Gesture Visualizer (Wayland)

[![Build](https://img.shields.io/badge/build-passing-brightgreen)]()
[![License](https://img.shields.io/badge/license-MIT-blue)]()
[![Platform](https://img.shields.io/badge/platform-Python%203.8%2B-blue)]()

A **real-time hand gesture tracking app** for Linux Wayland using a webcam.  
It shows a **virtual cursor** and **gesture labels** but does **not send real mouse input**.  
Great for **research**, **training models**, and **prototyping gesture-based UIs**.

---

## ✨ Features

- Virtual cursor follows the **index fingertip**  
- Gesture recognition:
  - **Left Click (visual)** → index finger near thumb  
  - **Right Click (visual)** → index finger near middle finger  
  - **Double Click (visual)** → multiple fingers close  
  - **Move Cursor** → free movement of index finger  
- On-screen feedback:
  - Colored circle = cursor position  
  - Text = detected gesture + FPS counter  
- Works in **real time** with PyQt5 + OpenCV  
- Optimized for **Wayland desktops on Linux**  

---

## 📦 Requirements

- Python **3.8+**  
- [OpenCV](https://pypi.org/project/opencv-python/)  
- [Mediapipe](https://pypi.org/project/mediapipe/)  
- [PyQt5](https://pypi.org/project/PyQt5/)  
- Linux with **Wayland** session  
- Any **USB or built-in webcam**  

Install dependencies:

```bash
pip install opencv-python mediapipe PyQt5
````

---

## 🚀 Usage

* **Move Cursor** → move index finger freely
* **Left Click (visual)** → bring index finger close to thumb
* **Right Click (visual)** → bring index finger close to middle finger
* **Double Click (visual)** → touch index and middle finger

The app opens a window with the **camera feed**, showing gestures and the **virtual cursor**.

---

## 📝 Notes

* Only **visual feedback** is provided — no real mouse actions.
* Works best with **bright lighting** and **clear hand visibility**.
* Made for **learning, experimentation, and demos**.


