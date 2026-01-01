from __future__ import annotations

import collections
from typing import Deque, Iterable, Optional, Sequence

import numpy as np


class ExponentialSmoother:
    """Applies exponential moving average smoothing to scalar or vector data."""

    def __init__(self, alpha: float) -> None:
        if not 0 < alpha <= 1:
            raise ValueError("alpha must be in (0, 1]")
        self.alpha = alpha
        self._value: Optional[np.ndarray] = None

    def reset(self) -> None:
        self._value = None

    def update(self, sample: Sequence[float]) -> np.ndarray:
        sample_vec = np.asarray(sample, dtype=np.float32)
        if self._value is None:
            self._value = sample_vec
        else:
            self._value = self.alpha * sample_vec + (1 - self.alpha) * self._value
        return self._value

    @property
    def value(self) -> Optional[np.ndarray]:
        return self._value


class TimeSeriesBuffer:
    """Maintains a bounded time-ordered collection of (timestamp, value) samples."""

    def __init__(self, max_age: float) -> None:
        self.max_age = max_age
        self._samples: Deque[tuple[float, float]] = collections.deque()

    def append(self, timestamp: float, value: float) -> None:
        self._samples.append((timestamp, value))
        self._evict_older_than(timestamp - self.max_age)

    def values(self) -> Iterable[tuple[float, float]]:
        return tuple(self._samples)

    def is_empty(self) -> bool:
        return not self._samples

    def span(self) -> float:
        if self.is_empty():
            return 0.0
        return self._samples[-1][0] - self._samples[0][0]

    def _evict_older_than(self, threshold: float) -> None:
        while self._samples and self._samples[0][0] < threshold:
            self._samples.popleft()


class RollingAverage:
    """Computes an average over a fixed-size queue of numpy vectors."""

    def __init__(self, size: int) -> None:
        if size <= 0:
            raise ValueError("size must be positive")
        self.size = size
        self._queue: Deque[np.ndarray] = collections.deque(maxlen=size)

    def append(self, sample: Sequence[float]) -> np.ndarray:
        vec = np.asarray(sample, dtype=np.float32)
        self._queue.append(vec)
        return self.value

    @property
    def value(self) -> np.ndarray:
        if not self._queue:
            return np.zeros(2, dtype=np.float32)
        stack = np.stack(self._queue, axis=0)
        return stack.mean(axis=0)
