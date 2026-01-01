from __future__ import annotations

import abc
from functools import lru_cache
from typing import Tuple

import cv2
import numpy as np

from utils.config import FilterConfig


class FilterBase(abc.ABC):
    """Base class for cinematic filters with shared helpers."""

    def __init__(self, name: str, config: FilterConfig) -> None:
        self.name = name
        self.config = config

    @abc.abstractmethod
    def apply(self, frame: np.ndarray) -> np.ndarray:
        raise NotImplementedError

    # ----- Helper operations -------------------------------------------------
    def _to_float(self, frame: np.ndarray) -> np.ndarray:
        return frame.astype(np.float32) / 255.0

    def _to_uint8(self, frame: np.ndarray) -> np.ndarray:
        return np.clip(frame * 255.0, 0, 255).astype(np.uint8)

    def _film_grain(self, frame: np.ndarray, intensity: float | None = None) -> np.ndarray:
        intensity = self.config.grain_intensity if intensity is None else intensity
        if intensity <= 0:
            return frame
        noise = np.random.normal(0.0, intensity, frame.shape).astype(np.float32)
        noisy = np.clip(frame + noise, 0.0, 1.0)
        return noisy

    def _vignette(self, frame: np.ndarray, strength: float | None = None) -> np.ndarray:
        strength = self.config.vignette_strength if strength is None else strength
        if strength <= 0:
            return frame
        rows, cols = frame.shape[:2]
        kernel_x = cv2.getGaussianKernel(cols, cols * strength)
        kernel_y = cv2.getGaussianKernel(rows, rows * strength)
        kernel = kernel_y * kernel_x.T
        mask = kernel / kernel.max()
        vignetted = frame * mask[..., np.newaxis]
        return vignetted

    def _apply_color_tint(self, frame: np.ndarray, color: Tuple[float, float, float], strength: float) -> np.ndarray:
        tint = np.array(color, dtype=np.float32)
        tinted = frame * (1 - strength) + tint * strength
        return np.clip(tinted, 0.0, 1.0)

    def _contrast_curve(self, frame: np.ndarray, contrast: float, pivot: float = 0.5) -> np.ndarray:
        return np.clip((frame - pivot) * contrast + pivot, 0.0, 1.0)

    def _soft_light_blend(self, base: np.ndarray, blend: np.ndarray) -> np.ndarray:
        return np.clip((1 - 2 * blend) * base ** 2 + 2 * blend * base, 0.0, 1.0)
