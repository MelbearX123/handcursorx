"""Overlay: debug drawing.

Draws the detected hand's 21 landmarks + skeleton onto the frame so you can see
what the tracker sees. Kept separate from control logic; toggle via
config.SHOW_OVERLAY. (Gesture-state HUD and dead-zone box come later, with the
controller and position engine.)
"""

import cv2
from cv2.typing import MatLike
from mediapipe.tasks.python.components.containers.landmark import NormalizedLandmark

_HAND_CONNECTIONS = (
    (0, 1), (0, 5), (5, 9), (9, 13), (13, 17), (0, 17),  # palm
    (1, 2), (2, 3), (3, 4),                              # thumb
    (5, 6), (6, 7), (7, 8),                              # index
    (9, 10), (10, 11), (11, 12),                         # middle
    (13, 14), (14, 15), (15, 16),                        # ring
    (17, 18), (18, 19), (19, 20),                        # pinky
)


def draw_overlay(
    frame: MatLike,
    landmarks: list[NormalizedLandmark] | None,
    state: str | None,
) -> MatLike:
    """Draw the hand's landmarks + skeleton onto the frame (in place)."""
    if landmarks is None:
        return frame
    h, w = frame.shape[:2]
    points = [(int(lm.x * w), int(lm.y * h)) for lm in landmarks]
    for start, end in _HAND_CONNECTIONS:
        cv2.line(frame, points[start], points[end], color=(255, 255, 255), thickness=2)
    for point in points:
        cv2.circle(frame, point, radius=4, color=(0, 255, 0), thickness=-1)
    return frame
