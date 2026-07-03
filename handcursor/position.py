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


class PositionEngine:
    def __init__(self):
        raise NotImplementedError

    def update(self, landmarks):
        """Map index tip -> screen, smooth, and move the cursor."""
        raise NotImplementedError
