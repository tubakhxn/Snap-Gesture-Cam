from __future__ import annotations

import cv2
import numpy as np

from .base import FilterBase


class WarmFilmFilter(FilterBase):
    """Soft, warm cinematic palette with subtle bloom."""

    def __init__(self, config) -> None:
        super().__init__("Warm Film", config)

    def apply(self, frame: np.ndarray) -> np.ndarray:
        float_frame = self._to_float(frame)
        blur = cv2.GaussianBlur(float_frame, (0, 0), sigmaX=2.2)
        bloom = np.clip(float_frame + blur * 0.4, 0.0, 1.0)
        toned = self._apply_color_tint(bloom, (0.35, 0.24, 0.12), 0.3)
        lifted = np.clip(toned + 0.02, 0.0, 1.0)
        grainy = self._film_grain(lifted, intensity=self.config.grain_intensity * 0.7)
        return self._to_uint8(grainy)
