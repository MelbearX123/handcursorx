"""handcursorx application package.

Modules:
    tracker    - MediaPipe wrapper: frame -> 21 landmarks
    position   - landmark 8 (index tip) -> smoothed, dead-zoned screen coords
    gestures   - stateless pose predicates (is_pinch, is_fist, ...)
    controller - state machine: gestures -> pyautogui actions (debounce/cooldown)
    overlay    - debug drawing of landmarks + current state
"""
