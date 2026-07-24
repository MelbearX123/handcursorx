"""Position engine: index fingertip -> screen coordinates.

Responsibility: turn landmark 8 (normalized 0.0-1.0) into a smoothed cursor
position and move the cursor there. Runs EVERY frame a hand is present.

Two things that make it feel good instead of broken:
    1. Dead-zone / active region (config.DEAD_ZONE): map only the center of the
       camera view to the full screen, so screen corners are reachable without
       the hand leaving the frame.
    2. Exponential moving average (config.SMOOTHING_ALPHA):
           smooth = alpha * new + (1 - alpha) * prev
       Kills the few-pixel per-frame jitter. This is the single biggest
       quality lever -- tune alpha live.

Note: pyautogui raises on the corner failsafe; decide whether to disable it
(and keep a keyboard quit key if you do).
"""

import pyautogui as pag
from mediapipe.tasks.python.components.containers.landmark import NormalizedLandmark

pag.PAUSE = 0
pag.FAILSAFE = False


class PositionEngine:
    def __init__(self):
        self._screen_size = pag.size()
        self._width = self._screen_size[0]
        self._height = self._screen_size[1]

    def update(self, landmarks: list[NormalizedLandmark]) -> None:
        index = landmarks[8]
        if index.x is None or index.y is None:
            return
        screen_x = index.x * self._width
        screen_y = index.y * self._height
        pag.moveTo(screen_x, screen_y)
