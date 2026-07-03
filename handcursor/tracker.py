"""Tracker: wraps MediaPipe Hands.

Responsibility: take a raw BGR frame and return the 21 hand landmarks for the
first detected hand (or None if no hand is present). Nothing in here should
know about cursors or gestures -- it only produces landmarks.

Landmark index reference (the ones the rest of the app cares about):
    0  = wrist            (stable anchor / palm reference)
    4  = thumb tip
    8  = index fingertip  (the cursor pointer)
    12 = middle tip
    16 = ring tip
    20 = pinky tip
    5, 9, 13, 17 = knuckles (MCP joints) below each finger

Landmarks come back normalized (0.0-1.0) relative to the frame -- keep them
that way; downstream modules rely on scale-invariance.

Design notes:
    - Configure with MAX_NUM_HANDS, MIN_DETECTION_CONFIDENCE,
      MIN_TRACKING_CONFIDENCE from config.
    - Run in video/streaming mode for speed.
"""


class HandTracker:
    def __init__(self):
        raise NotImplementedError

    def process(self, frame):
        """Return the 21 landmarks for the first hand, or None."""
        raise NotImplementedError
