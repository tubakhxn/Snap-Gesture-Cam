from __future__ import annotations

import threading
import time
from typing import Optional

import cv2

from utils.config import CameraConfig


class ThreadedCamera:
    """Continuously captures frames on a background thread for low-latency reads."""

    def __init__(self, config: CameraConfig) -> None:
        self.config = config
        self._capture = cv2.VideoCapture(config.device_index, cv2.CAP_DSHOW)
        self._capture.set(cv2.CAP_PROP_FRAME_WIDTH, config.width)
        self._capture.set(cv2.CAP_PROP_FRAME_HEIGHT, config.height)
        self._capture.set(cv2.CAP_PROP_FPS, config.target_fps)

        self._lock = threading.Lock()
        self._frame: Optional[cv2.Mat] = None
        self._running = False
        self._thread: Optional[threading.Thread] = None

    def start(self) -> None:
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._reader_loop, daemon=True)
        self._thread.start()

    def _reader_loop(self) -> None:
        while self._running:
            ret, frame = self._capture.read()
            if not ret:
                time.sleep(0.01)
                continue
            frame = cv2.flip(frame, 1)
            with self._lock:
                self._frame = frame

    def read(self) -> Optional[cv2.Mat]:
        with self._lock:
            if self._frame is None:
                return None
            return self._frame.copy()

    def stop(self) -> None:
        self._running = False
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=1.0)
        self._thread = None
        self._frame = None
        self._capture.release()

    def __enter__(self) -> "ThreadedCamera":
        self.start()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.stop()
