"""Controller: gestures -> actions, with a state machine.

Responsibility: own all the STATEFUL logic that gestures.py deliberately
avoids. Reads the stateless predicates each frame and decides when to actually
fire a pyautogui action.

Two rules that keep it from misfiring:
    - Debounce: a predicate must be true for config.DEBOUNCE_FRAMES consecutive
      frames before the action fires (kills single-frame false positives).
    - Cooldown: enforce config.COOLDOWN_MS before the SAME action can fire
      again (kills accidental double-clicks).

Fire once per gesture, not once per frame. Expose `state` (current gesture /
cooldown info) so overlay.py can display what's happening while you tune.

Mapping (transfers directly from the old archive_yolo/main_yolo.py):
    pinch        -> pag.leftClick
    right pinch  -> pag.rightClick
    two fingers  -> pag.scroll
    fist         -> pause tracking / reclaim the mouse
"""


class GestureController:
    def __init__(self):
        self.state = None
        raise NotImplementedError

    def update(self, landmarks):
        """Evaluate predicates, apply debounce/cooldown, fire actions."""
        raise NotImplementedError
