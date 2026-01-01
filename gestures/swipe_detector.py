from __future__ import annotations

import time
from typing import Optional

from utils.config import GestureConfig
from utils.smoothing import ExponentialSmoother, TimeSeriesBuffer

from .hand_tracker import HandObservation


class SwipeDetector:
    """Detects left/right swipe gestures from wrist motion."""

    def __init__(self, config: GestureConfig, frame_width: int) -> None:
        self.config = config
        self.frame_width = frame_width
        self._smoother = ExponentialSmoother(config.smoothing_alpha)
        self._history = TimeSeriesBuffer(config.history_window)
        self._cooldown_until = 0.0

    def update(self, hands: list[HandObservation]) -> Optional[str]:
        now = time.perf_counter()
        if not hands:
            self._smoother.reset()
            return None

        wrist_x = hands[0].wrist[0] / max(self.frame_width, 1)
        smoothed = float(self._smoother.update([wrist_x])[0])
        self._history.append(now, smoothed)

        if now < self._cooldown_until:
            return None

        samples = list(self._history.values())
        if len(samples) < 2:
            return None

        start_time, start_pos = samples[0]
        end_time, end_pos = samples[-1]
        duration = max(end_time - start_time, 1e-3)
        delta = end_pos - start_pos
        velocity = abs(delta) / duration

        if abs(delta) < self.config.swipe_distance_normalized:
            return None
        if velocity < self.config.swipe_velocity_normalized:
            return None

        direction = "right" if delta > 0 else "left"
        self._cooldown_until = now + self.config.swipe_cooldown
        self._history = TimeSeriesBuffer(self.config.history_window)
        self._smoother.reset()
        return direction

    def resize(self, frame_width: int) -> None:
        self.frame_width = frame_width
