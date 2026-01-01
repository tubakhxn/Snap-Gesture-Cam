from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class CameraConfig:
    width: int = 1280
    height: int = 720
    target_fps: int = 30
    device_index: int = 0
    frame_buffer_size: int = 2


@dataclass(frozen=True)
class GestureConfig:
    smoothing_alpha: float = 0.25
    swipe_distance_normalized: float = 0.25  # fraction of frame width
    swipe_velocity_normalized: float = 0.55  # width per second
    swipe_cooldown: float = 0.9  # seconds
    history_window: float = 0.6  # seconds
    detection_confidence: float = 0.7
    tracking_confidence: float = 0.6


@dataclass(frozen=True)
class TransitionConfig:
    duration: float = 0.45  # seconds
    easing_power: float = 2.5
    frame_blend_bias: float = 0.15


@dataclass(frozen=True)
class FilterConfig:
    grain_intensity: float = 0.08
    vignette_strength: float = 0.35


@dataclass(frozen=True)
class OverlayConfig:
    font_scale: float = 0.8
    font_thickness: int = 2
    margin: int = 24
    text_color: Tuple[int, int, int] = (245, 245, 245)
    shadow_color: Tuple[int, int, int] = (10, 10, 10)


@dataclass(frozen=True)
class AppConfig:
    camera: CameraConfig = CameraConfig()
    gesture: GestureConfig = GestureConfig()
    transition: TransitionConfig = TransitionConfig()
    filters: FilterConfig = FilterConfig()
    overlay: OverlayConfig = OverlayConfig()


def get_config() -> AppConfig:
    """Return the default immutable app configuration."""

    return AppConfig()
