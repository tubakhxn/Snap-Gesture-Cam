from __future__ import annotations

import cv2
import numpy as np

from .base import FilterBase


class BlackWhiteFilter(FilterBase):
    """High-contrast monochrome look with film grain."""

    def __init__(self, config) -> None:
        super().__init__("Cinematic B&W", config)
        self._clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))

    def apply(self, frame: np.ndarray) -> np.ndarray:
        float_frame = self._to_float(frame)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = self._clahe.apply(gray)
        gray = gray.astype(np.float32) / 255.0
        mono = np.dstack([gray, gray, gray])

        high_freq = float_frame - cv2.GaussianBlur(float_frame, (0, 0), sigmaX=2)
        crisp = np.clip(mono + high_freq * 0.35, 0.0, 1.0)
        with_grain = self._film_grain(crisp, intensity=self.config.grain_intensity * 1.3)
        vignetted = self._vignette(with_grain, strength=self.config.vignette_strength * 0.8)
        return self._to_uint8(vignetted)
