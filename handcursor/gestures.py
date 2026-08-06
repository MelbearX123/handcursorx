"""Gestures: stateless pose detection.

Pure functions of the landmarks. Distances are normalized by hand size so
thresholds are scale-invariant (a pinch reads the same near or far).

Public interface: gesture_check(landmarks) -> Gesture, the single active
gesture; the is_* predicates are the building blocks it composes.
"""

import math
from enum import Enum, auto

from mediapipe.tasks.python.components.containers.landmark import NormalizedLandmark
from config import PINCH_THRESHOLD


class Gesture(Enum):
    """The single hand gesture active in a frame."""

    NONE = auto()
    POINTING = auto()  # index only -> move cursor
    PINCH = auto()  # thumb + index -> left click
    RIGHT_PINCH = auto()  # thumb + middle -> right click
    OPEN_PALM = auto()  # open palm -> scroll enabled


def _distance(a: NormalizedLandmark, b: NormalizedLandmark) -> float:
    """Euclidean distance between two landmarks in normalized (x, y) space."""
    assert a.x is not None and a.y is not None
    assert b.x is not None and b.y is not None
    return math.hypot(a.x - b.x, a.y - b.y)


def hand_scale(landmarks: list[NormalizedLandmark]) -> float:
    """Apparent hand size: wrist(0) -> middle knuckle(9) distance."""
    return _distance(landmarks[0], landmarks[9])


def is_pinch(landmarks: list[NormalizedLandmark]) -> bool:
    """Thumb tip(4) touching index tip(8), measured as a fraction of hand size."""
    return (
        _distance(landmarks[4], landmarks[8]) / hand_scale(landmarks) < PINCH_THRESHOLD
    )


def is_right_pinch(landmarks: list[NormalizedLandmark]) -> bool:
    """Thumb tip(4) touching middle finger tip(12), measured as a fraction of hand size."""
    return (
        _distance(landmarks[4], landmarks[12]) / hand_scale(landmarks) < PINCH_THRESHOLD
    )


def is_fist(landmarks: list[NormalizedLandmark]) -> bool:
    """Distance from tips to wrist is shorter than distance from MCP to wrist"""
    raise NotImplementedError


def is_open_palm(landmarks: list[NormalizedLandmark]) -> bool:
    """All four fingers extended: each tip is farther from the wrist than its MCP """
    wrist = landmarks[0]
    finger_tips = [8, 12, 16, 20]
    finger_mcps = [5, 9, 13, 17]
    for tip, mcp in zip(finger_tips, finger_mcps):
        if _distance(landmarks[tip], wrist) <= _distance(landmarks[mcp], wrist):
            return False
    return True


def is_pointing(landmarks: list[NormalizedLandmark]) -> bool:
    """Checks if index tip(8) is higher than pip(6)."""
    tip = landmarks[8]
    pip = landmarks[6]
    if tip.y is None or pip.y is None:
        return False
    return tip.y < pip.y


def gesture_check(landmarks: list[NormalizedLandmark]) -> Gesture:
    """Return the single active gesture this frame.

    Order encodes priority: pinches are checked before pointing, because a
    thumb-index pinch also satisfies "index extended" so
    the cursor holds still while you click.
    """
    if is_pinch(landmarks):
        return Gesture.PINCH
    if is_right_pinch(landmarks):
        return Gesture.RIGHT_PINCH
    if is_pointing(landmarks):
        return Gesture.POINTING
    return Gesture.NONE
