from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

import cv2
import mediapipe as mp

from utils.config import GestureConfig


@dataclass
class HandObservation:
    """Represents a single detected hand with pixel coordinates."""

    landmarks: List[tuple[float, float]]
    handedness: str

    @property
    def wrist(self) -> tuple[float, float]:
        return self.landmarks[0]


class HandTracker:
    """Wrapper around MediaPipe Hands with convenient outputs."""

    def __init__(self, config: GestureConfig) -> None:
        self.config = config
        self._mp_hands = mp.solutions.hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            model_complexity=1,
            min_detection_confidence=config.detection_confidence,
            min_tracking_confidence=config.tracking_confidence,
        )

    def process(self, frame) -> List[HandObservation]:
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rgb.flags.writeable = False
        results = self._mp_hands.process(rgb)
        if not results.multi_hand_landmarks:
            return []

        h, w, _ = frame.shape
        observations: List[HandObservation] = []
        for hand_landmarks, classification in zip(
            results.multi_hand_landmarks,
            results.multi_handedness,
        ):
            coords: List[tuple[float, float]] = []
            for lm in hand_landmarks.landmark:
                coords.append((lm.x * w, lm.y * h))
            observations.append(
                HandObservation(
                    landmarks=coords,
                    handedness=classification.classification[0].label,
                )
            )
        return observations

    def close(self) -> None:
        self._mp_hands.close()
