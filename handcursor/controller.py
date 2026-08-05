"""Controller: gestures -> actions.

Holds the stateful logic gestures.py avoids: debounce (a gesture must hold for
DEBOUNCE_FRAMES before firing) and cooldown (COOLDOWN_MS between actions), so a
held pinch clicks once, not every frame.
"""

import time

from mediapipe.tasks.python.components.containers.landmark import NormalizedLandmark
from handcursor.gestures import gesture_check, Gesture
from config import DEBOUNCE_FRAMES, COOLDOWN_MS
import pyautogui as pag


class GestureController:
    def __init__(self):
        self._state = None
        self._lastActionMs = None
        self._framesPerAction = 0
        self._pending = None

    def update(self, landmarks: list[NormalizedLandmark]) -> None:
        """Evaluate the gesture, debounce it, and fire a click once per hold."""
        current_gesture = gesture_check(landmarks=landmarks)

        # Reset the frame counter
        if current_gesture != self._pending:
            self._pending = current_gesture
            self._framesPerAction = 0

        # POINTING (cursor) and NONE (idle) handled elsewhere or not at all.
        if current_gesture is Gesture.NONE or current_gesture is Gesture.POINTING:
            return

        self._framesPerAction += 1

        if self._framesPerAction != DEBOUNCE_FRAMES:
            return

        # Cooldown
        now_ms = time.monotonic() * 1000
        if self._lastActionMs is not None and now_ms - self._lastActionMs < COOLDOWN_MS:
            return

        match current_gesture:
            case Gesture.PINCH:
                pag.leftClick()
            case Gesture.RIGHT_PINCH:
                pag.rightClick()

        self._lastActionMs = now_ms
