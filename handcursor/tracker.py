"""Tracker: wraps MediaPipe HandLandmarker.

Takes a raw BGR frame and returns the first detected hand's 21 landmarks
(or None). Landmarks are normalized (0.0-1.0) relative to the frame -- keep
them that way; downstream modules rely on scale-invariance.

Landmark index reference:
    0  = wrist            8  = index fingertip (cursor pointer)
    4  = thumb tip        12/16/20 = middle/ring/pinky tips
    5, 9, 13, 17 = knuckles (MCP joints) below each finger
"""

import time
from pathlib import Path

import cv2
from cv2.typing import MatLike
from config import MAX_NUM_HANDS, MIN_DETECTION_CONFIDENCE, MIN_TRACKING_CONFIDENCE
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# Absolute path to the model
_MODEL_PATH = Path(__file__).resolve().parent.parent / "models" / "hand_landmarker.task"


class HandTracker:
    def __init__(self):
        self._base_options = python.BaseOptions(model_asset_path=str(_MODEL_PATH))
        self._options = vision.HandLandmarkerOptions(
            base_options=self._base_options,
            running_mode=vision.RunningMode.VIDEO,
            num_hands=MAX_NUM_HANDS,
            min_hand_detection_confidence=MIN_DETECTION_CONFIDENCE,
            min_tracking_confidence=MIN_TRACKING_CONFIDENCE,
        )
        self._detector = vision.HandLandmarker.create_from_options(self._options)
        self._last_timestamp_ms = -1

    def process(self, frame: MatLike):
        """Return the 21 landmarks for the first hand, or None."""

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_frame = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        # VIDEO mode requires a strictly increasing timestamp (ms)
        timestamp_ms = max(
            self._last_timestamp_ms + 1, time.monotonic_ns() // 1_000_000
        )
        self._last_timestamp_ms = timestamp_ms
        detection_result = self._detector.detect_for_video(mp_frame, timestamp_ms)

        landmarks = detection_result.hand_landmarks
        if not landmarks:
            return None
        # 21 landmarks
        return landmarks[0]
