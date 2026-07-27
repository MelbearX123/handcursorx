"""Position engine: index fingertip -> screen coordinates.

Responsibility: turn landmark 8 (normalized 0.0-1.0) into a smoothed cursor
position and move the cursor there. Runs EVERY frame a hand is present.

"""

import pyautogui as pag
from mediapipe.tasks.python.components.containers.landmark import NormalizedLandmark
from config import X_FACTOR, Y_FACTOR, SMOOTHING_ALPHA

pag.PAUSE = 0
pag.FAILSAFE = False


class PositionEngine:
    def __init__(self):
        self._screen_size = pag.size()
        self._width = self._screen_size[0]
        self._height = self._screen_size[1]
        self._prev_x = None
        self._prev_y = None

    def update(self, landmarks: list[NormalizedLandmark]) -> None:
        index = landmarks[8]
        if index.x is None or index.y is None:
            return
        screen_x = index.x * self._width * X_FACTOR
        screen_y = index.y * self._height * Y_FACTOR
        if self._prev_x is None or self._prev_y is None:
            smooth_x, smooth_y = screen_x, screen_y
        else:
            smooth_x = SMOOTHING_ALPHA * screen_x + (1 - SMOOTHING_ALPHA) * self._prev_x
            smooth_y = SMOOTHING_ALPHA * screen_y + (1 - SMOOTHING_ALPHA) * self._prev_y

        self._prev_x = smooth_x
        self._prev_y = smooth_y

        pag.moveTo(smooth_x, smooth_y)
