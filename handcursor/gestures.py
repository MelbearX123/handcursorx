"""Gestures: stateless pose predicates.

Responsibility: answer "is this pose happening RIGHT NOW?" as pure functions of
the landmarks. No state, no side effects, no pyautogui -- that lives in
controller.py. This split is what makes debounce bugs easy to find.

Every predicate is a distance/angle relationship between landmarks. Normalize
all distances by a reference length (e.g. wrist(0) -> middle knuckle(9)) so
thresholds are scale-invariant: a pinch reads the same whether the hand is
near or far from the camera.

Predicates to implement (thresholds in config):
    is_pinch(landmarks)        thumb tip(4)  <-> index tip(8)  distance small
    is_right_pinch(landmarks)  thumb tip(4)  <-> middle tip(12) distance small
    is_fist(landmarks)         all tips close to wrist(0)
    is_two_fingers(landmarks)  index + middle extended (for scroll)

Later, classifier.py can provide these same labels from a trained model; the
controller shouldn't care whether a label came from an `if` or a model.
"""


def hand_scale(landmarks):
    """Reference length (wrist -> middle knuckle) for normalizing distances."""
    raise NotImplementedError


def is_pinch(landmarks):
    raise NotImplementedError


def is_right_pinch(landmarks):
    raise NotImplementedError


def is_fist(landmarks):
    raise NotImplementedError
