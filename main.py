"""Entry point for handcursorx.

Wiring only: capture a frame, flip it, run the tracker, draw the overlay, show
it. Keep this thin -- real logic belongs in modules under handcursor/. (The
position engine and gesture controller get wired in here as they're built.)
"""

import cv2
from config import QUIT_KEY, FLIP_HORIZONTAL, CAMERA_INDEX, SHOW_OVERLAY
from handcursor.overlay import draw_overlay
from handcursor.gestures import gesture_check, Gesture
from handcursor.tracker import HandTracker
from handcursor.position import PositionEngine
from handcursor.controller import GestureController
from handcursor.scroll import ScrollEngine


def main():
    cap = cv2.VideoCapture(CAMERA_INDEX)
    if not cap.isOpened():
        print("Webcam could not be opened.")
        return

    tracker = HandTracker()
    position = PositionEngine()
    controller = GestureController()
    scroll = ScrollEngine()

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Failed to receive frame")
            return

        if FLIP_HORIZONTAL:
            frame = cv2.flip(frame, 1)

        landmarks = tracker.process(frame=frame)
        gesture = gesture_check(landmarks) if landmarks else Gesture.NONE

        if landmarks and SHOW_OVERLAY:
            draw_overlay(frame, landmarks, gesture.name)

        if landmarks and gesture == Gesture.POINTING:
            position.update(landmarks=landmarks)

        controller.update(gesture)
        scroll.update(gesture, landmarks)

        cv2.imshow("Handcursor", frame)
        if cv2.waitKey(1) & 0xFF == QUIT_KEY:
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
