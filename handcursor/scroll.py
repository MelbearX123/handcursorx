"""Scroll engine: open-palm hand movement -> continuous scroll.

Stateful sibling of position.py. While armed (open palm), scrolls every frame by
an amount proportional to how fast the wrist is moving vertically -- slow
movement nudges, fast movement flies (direct-manipulation, iPad-style), instead
of firing one discrete burst per detected swipe. Velocity is EMA-smoothed so it
glides rather than jitters, and on release the velocity decays by SCROLL_FRICTION
so a flick coasts to a stop (momentum). Stateful (needs the previous frame), so
it lives here rather than in the stateless gestures.py.
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
        # Released (not open palm / no hand): coast on the leftover velocity,
        # decaying it each frame until it's too small to move a line. This is the
        # inertia -- a fast flick keeps scrolling after you lower your hand.
        if gesture is not Gesture.OPEN_PALM or landmarks is None:
            self._prev_y = None  # re-arming later seeds fresh (no jump)
            self._velocity *= SCROLL_FRICTION
            amount = int(-self._velocity * SCROLL_GAIN)
            if amount == 0:
                self._velocity = 0.0  # coast has died out
            else:
                pag.scroll(amount)
            return

        wrist_y = landmarks[0].y
        if wrist_y is None:
            return

        if self._prev_y is None:
            self._prev_y = wrist_y
            return

        dy = wrist_y - self._prev_y  # per-frame movement; bigger = faster hand
        self._prev_y = wrist_y

        # EMA-smooth the velocity so scrolling glides instead of jittering.
        self._velocity = SCROLL_SMOOTHING * dy + (1 - SCROLL_SMOOTHING) * self._velocity
        pag.scroll(int(-self._velocity * SCROLL_GAIN))
