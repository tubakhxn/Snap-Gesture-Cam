from __future__ import annotations

import cv2
import numpy as np

from .base import FilterBase


class NewYorkFilter(FilterBase):
    """Cool, high-contrast street aesthetic."""

    def __init__(self, config) -> None:
        super().__init__("New York Look", config)

    def apply(self, frame: np.ndarray) -> np.ndarray:
        lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB).astype(np.float32)
        lab[..., 0] = np.clip(lab[..., 0] * 1.08 + 5, 0, 255)
        lab[..., 1] = np.clip(lab[..., 1] * 0.9 - 3, 0, 255)
        lab[..., 2] = np.clip(lab[..., 2] * 0.8 - 12, 0, 255)
        cool = cv2.cvtColor(lab.astype(np.uint8), cv2.COLOR_LAB2BGR)
        float_frame = self._to_float(cool)

        blur = cv2.GaussianBlur(float_frame, (0, 0), sigmaX=1.2)
        detail = float_frame - blur
        punchy = np.clip(float_frame + detail * 1.8, 0.0, 1.0)
        toned = self._apply_color_tint(punchy, (0.05, 0.18, 0.35), 0.25)
        toned = self._contrast_curve(toned, contrast=1.1)
        grainy = self._film_grain(toned, intensity=self.config.grain_intensity * 0.8)
        return self._to_uint8(grainy)
