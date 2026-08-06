"""Scroll engine: open-palm vertical swipe -> scroll.

Stateful sibling of position.py -- while armed (open palm), tracks the wrist's
recent y in a rolling window and fires pag.scroll when the vertical displacement
across it exceeds SWIPE_THRESHOLD. Needs history (hence stateful), so it lives
here rather than in the stateless gestures.py.
"""

import time
from collections import deque

import pyautogui as pag
from mediapipe.tasks.python.components.containers.landmark import NormalizedLandmark
from handcursor.gestures import Gesture
from config import (
    SWIPE_WINDOW,
    SWIPE_THRESHOLD,
    SCROLL_AMOUNT,
    SCROLL_COOLDOWN_MS,
    SWIPE_THRESHOLD,
)


class ScrollEngine:
    def __init__(self):
        self._history = deque(maxlen=SWIPE_WINDOW)
        self._lastScrollMs = None

    def update(
        self, gesture: Gesture, landmarks: list[NormalizedLandmark] | None
    ) -> None:
        """Track wrist motion while armed; fire pag.scroll on a vertical swipe."""
        if gesture is not Gesture.OPEN_PALM or landmarks is None:
            self._history.clear()
            return

        wrist_y = landmarks[0].y
        if wrist_y is None:
            return
        self._history.append(wrist_y)

        if len(self._history) < SWIPE_WINDOW:
            return

        displacement = self._history[-1] - self._history[0]
        if abs(displacement) < SWIPE_THRESHOLD:
            return

        now_ms = time.monotonic() * 1000
        if (
            self._lastScrollMs is not None
            and now_ms - self._lastScrollMs < SCROLL_COOLDOWN_MS
        ):
            return

        pag.scroll(SCROLL_AMOUNT if displacement < 0 else -SCROLL_AMOUNT)

        self._lastScrollMs = now_ms
        self._history.clear()
