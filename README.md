
# Snap Gesture Cam

A Snapchat-inspired, gesture-controlled cinematic webcam application built with Python, OpenCV, and MediaPipe Hands. Swipe left or right in mid-air to cycle through polished film looks in real time.

---
**Creator/Dev:** [tubakhxn](https://github.com/tubakhxn)
---

## Features
- Real-time threaded webcam capture (mirrored view for natural interaction)
- MediaPipe-powered hand tracking with smoothed wrist motion and swipe gesture detection
- Five cinematic color pipelines with multi-stage processing:
  1. **Cinematic B&W** – punchy monochrome with film grain
  2. **New York Look** – cool metropolis tones and sharp contrast
  3. **Vintage Sepia** – sepia wash, bloom, and vignette
  4. **Cyberpunk Neon** – purple/blue neon glow with edge accents
  5. **Warm Film** – soft warm palette with subtle bloom
- Eased cross-fades between filters for cinematic transitions
- Minimal HUD showing active filter and live FPS


## Installation
1. Ensure Python 3.10+ is installed.
2. (Recommended) Fork this repository to your own GitHub account.
3. Clone your fork locally:
  ```bash
  git clone https://github.com/YOUR-USERNAME/snap-gesture-cam.git
  cd snap-gesture-cam
  ```
4. Create and activate a virtual environment.
5. Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```

## Usage
Run the app directly:
```bash
python main.py
```

Controls:
- **Swipe right** with your hand → next filter
- **Swipe left** → previous filter
- **Press `q`** → exit the app

Tips:
- Use a well-lit environment so MediaPipe can track your hand reliably.
- Keep your swipe roughly horizontal and within the frame.
- Allow a short pause between swipes for the cooldown to reset.

## Project Structure
```
main.py
camera/
  webcam.py
filters/
  base.py
  black_white.py
  new_york.py
  vintage.py
  cyberpunk.py
  warm_film.py
gestures/
  hand_tracker.py
  swipe_detector.py
ui/
  overlay.py
utils/
  config.py
  fps.py
  smoothing.py
README.md
requirements.txt
```

## Troubleshooting
- **No camera feed**: ensure no other applications are using the webcam and the correct device index is set in `utils/config.py`.
- **Low FPS**: reduce the camera resolution or close other CPU-intensive processes.
- **Gestures not recognized**: adjust lighting, keep your hand near the center, or tweak swipe sensitivity in `GestureConfig`.
