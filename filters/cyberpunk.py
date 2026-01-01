from __future__ import annotations

import cv2
import numpy as np

from .base import FilterBase


class CyberpunkFilter(FilterBase):
    """Neon-inspired purple/blue glow with edge accents."""

    def __init__(self, config) -> None:
        super().__init__("Cyberpunk Neon", config)

    def apply(self, frame: np.ndarray) -> np.ndarray:
        float_frame = self._to_float(frame)
        contrasted = self._contrast_curve(float_frame, contrast=1.3)
        tinted = self._apply_color_tint(contrasted, (0.25, 0.05, 0.4), 0.35)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 80, 160)
        edges = cv2.GaussianBlur(edges, (0, 0), sigmaX=1.5)
        neon = cv2.applyColorMap(edges, cv2.COLORMAP_HOT)
        neon = cv2.cvtColor(neon, cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0
        neon = self._apply_color_tint(neon, (0.0, 0.3, 0.9), 0.6)

        glow = cv2.GaussianBlur(neon, (0, 0), sigmaX=2)
        mixed = np.clip(tinted + glow * 0.35, 0.0, 1.0)
        grainy = self._film_grain(mixed, intensity=self.config.grain_intensity * 0.6)
        return self._to_uint8(grainy)
