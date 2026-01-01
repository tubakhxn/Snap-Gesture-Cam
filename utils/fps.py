from __future__ import annotations

import time
from collections import deque
from typing import Deque


class FPSTracker:
    """Tracks instantaneous and smoothed FPS using a timestamp queue."""

    def __init__(self, window: int = 60) -> None:
        self.window = window
        self._samples: Deque[float] = deque(maxlen=window)
        self._last_time = time.perf_counter()

    def tick(self) -> float:
        now = time.perf_counter()
        delta = now - self._last_time
        self._last_time = now
        if delta > 0:
            self._samples.append(1.0 / delta)
        return self.fps

    @property
    def fps(self) -> float:
        if not self._samples:
            return 0.0
        return sum(self._samples) / len(self._samples)
