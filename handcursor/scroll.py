"""Scroll engine: open-palm hand movement -> continuous scroll.
"""

import pyautogui as pag
from mediapipe.tasks.python.components.containers.landmark import NormalizedLandmark
from handcursor.gestures import Gesture
from config import SCROLL_GAIN, SCROLL_SMOOTHING, SCROLL_FRICTION


class ScrollEngine:
    def __init__(self):
        self._prev_y = None
        self._velocity = 0.0

    def update(
        self, gesture: Gesture, landmarks: list[NormalizedLandmark] | None
    ) -> None:
        """Scroll proportional to wrist speed; coast with momentum after release."""
        # fist kills all scrolling
        if gesture is Gesture.FIST:
            self._velocity = 0.0
            self._prev_y = None
            return

        if gesture is not Gesture.OPEN_PALM or landmarks is None:
            self._prev_y = None 
            self._velocity *= SCROLL_FRICTION
            amount = int(self._velocity * SCROLL_GAIN)
            if amount == 0:
                self._velocity = 0.0 
            else:
                pag.scroll(amount)
            return

        wrist_y = landmarks[0].y
        if wrist_y is None:
            return

        if self._prev_y is None:
            self._prev_y = wrist_y
            return

        dy = wrist_y - self._prev_y
        self._prev_y = wrist_y

        self._velocity = SCROLL_SMOOTHING * dy + (1 - SCROLL_SMOOTHING) * self._velocity
        pag.scroll(int(self._velocity * SCROLL_GAIN))
