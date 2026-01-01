from __future__ import annotations

import cv2

from utils.config import OverlayConfig


class Overlay:
    """Draws minimalist HUD elements such as filter name and FPS."""

    def __init__(self, config: OverlayConfig) -> None:
        self.config = config
        self._font = cv2.FONT_HERSHEY_DUPLEX

    def draw(self, frame, filter_name: str, fps: float) -> None:
        text = f"{filter_name}  ·  {fps:05.1f} FPS"
        margin = self.config.margin
        shadow_pos = (margin + 2, margin + 2)
        text_pos = (margin, margin)
        cv2.putText(
            frame,
            text,
            shadow_pos,
            self._font,
            self.config.font_scale,
            self.config.shadow_color,
            self.config.font_thickness + 2,
            lineType=cv2.LINE_AA,
        )
        cv2.putText(
            frame,
            text,
            text_pos,
            self._font,
            self.config.font_scale,
            self.config.text_color,
            self.config.font_thickness,
            lineType=cv2.LINE_AA,
        )
