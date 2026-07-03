"""Overlay: debug drawing.

Responsibility: draw the 21 landmarks and the current controller state onto the
frame so you can see what the model sees while tuning. Kept separate so debug
visuals never tangle with real control logic -- disable via config.SHOW_OVERLAY
without touching anything else.

Draw:
    - landmark points / hand skeleton
    - the active gesture and cooldown status (from controller.state)
    - optionally the dead-zone rectangle, so you can see the active region
"""


def draw_overlay(frame, landmarks, state):
    """Annotate the frame in place (or return the annotated copy)."""
    raise NotImplementedError
