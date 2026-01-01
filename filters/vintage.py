from __future__ import annotations

import cv2
import numpy as np

from .base import FilterBase


class VintageFilter(FilterBase):
    """Warm sepia tone with subtle bloom and vignette."""

    def __init__(self, config) -> None:
        super().__init__("Vintage Sepia", config)
        self._sepia_matrix = np.array(
            [
                [0.272, 0.534, 0.131],
                [0.349, 0.686, 0.168],
                [0.393, 0.769, 0.189],
            ],
            dtype=np.float32,
        )

    def apply(self, frame: np.ndarray) -> np.ndarray:
        float_frame = self._to_float(frame)
        sepia = float_frame @ self._sepia_matrix.T
        sepia = np.clip(sepia, 0.0, 1.0)

        bloom = cv2.GaussianBlur(sepia, (0, 0), sigmaX=3)
        blended = self._soft_light_blend(sepia, bloom)
        toned = self._apply_color_tint(blended, (0.3, 0.22, 0.1), 0.2)
        vignetted = self._vignette(toned, strength=self.config.vignette_strength * 1.2)
        grainy = self._film_grain(vignetted, intensity=self.config.grain_intensity)
        return self._to_uint8(grainy)
