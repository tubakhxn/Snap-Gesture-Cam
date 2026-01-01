from __future__ import annotations

import time
from typing import List

import cv2

from camera.webcam import ThreadedCamera
from filters.black_white import BlackWhiteFilter
from filters.cyberpunk import CyberpunkFilter
from filters.new_york import NewYorkFilter
from filters.vintage import VintageFilter
from filters.warm_film import WarmFilmFilter
from gestures.hand_tracker import HandTracker
from gestures.swipe_detector import SwipeDetector
from ui.overlay import Overlay
from utils.config import AppConfig, get_config
from utils.fps import FPSTracker


def ease(value: float, power: float) -> float:
    value = min(max(value, 0.0), 1.0)
    if value in (0.0, 1.0):
        return value
    numerator = value**power
    denominator = numerator + (1 - value) ** power
    return numerator / denominator if denominator else value


def build_filters(cfg: AppConfig) -> List:
    return [
        BlackWhiteFilter(cfg.filters),
        NewYorkFilter(cfg.filters),
        VintageFilter(cfg.filters),
        CyberpunkFilter(cfg.filters),
        WarmFilmFilter(cfg.filters),
    ]


def main() -> None:
    cfg = get_config()
    filters = build_filters(cfg)
    overlay = Overlay(cfg.overlay)
    fps_tracker = FPSTracker()

    with ThreadedCamera(cfg.camera) as camera:
        hand_tracker = HandTracker(cfg.gesture)
        swipe_detector = SwipeDetector(cfg.gesture, cfg.camera.width)

        current_idx = 0
        target_idx = 0
        transition_start: float | None = None

        try:
            while True:
                frame = camera.read()
                if frame is None:
                    time.sleep(0.005)
                    continue

                height, width = frame.shape[:2]
                if width != swipe_detector.frame_width:
                    swipe_detector.resize(width)

                hands = hand_tracker.process(frame)
                swipe_direction = swipe_detector.update(hands)
                if swipe_direction == "right":
                    target_idx = (current_idx + 1) % len(filters)
                    transition_start = time.perf_counter()
                elif swipe_direction == "left":
                    target_idx = (current_idx - 1) % len(filters)
                    transition_start = time.perf_counter()

                if transition_start is not None:
                    elapsed = time.perf_counter() - transition_start
                    progress = elapsed / cfg.transition.duration
                    if progress >= 1.0:
                        current_idx = target_idx
                        transition_start = None
                        filtered = filters[current_idx].apply(frame)
                        display_name = filters[current_idx].name
                    else:
                        pct = ease(progress, cfg.transition.easing_power)
                        base = filters[current_idx].apply(frame)
                        target = filters[target_idx].apply(frame)
                        filtered = cv2.addWeighted(target, pct, base, 1 - pct, 0)
                        display_name = filters[target_idx].name
                else:
                    filtered = filters[current_idx].apply(frame)
                    display_name = filters[current_idx].name

                fps = fps_tracker.tick()
                overlay.draw(filtered, display_name, fps)
                cv2.imshow("Snap Gesture Cam", filtered)

                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
        finally:
            hand_tracker.close()
            cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
