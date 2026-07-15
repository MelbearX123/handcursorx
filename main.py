"""Entry point for handcursorx.

Responsibility: wiring only. Read a frame, pass it through the tracker,
feed landmarks to the position engine and the controller, draw the overlay,
repeat. Keep this file thin — if real logic shows up here, it belongs in a
module under handcursor/.

Loop sketch:
    tracker = HandTracker()
    position = PositionEngine()
    controller = GestureController()

    while True:
        frame = read_and_flip(cap)
        landmarks = tracker.process(frame)
        if landmarks:
            position.update(landmarks)      # moves the cursor
            controller.update(landmarks)    # fires clicks / scrolls
        if SHOW_OVERLAY:
            draw_overlay(frame, landmarks, controller.state)
        if quit_pressed():
            break
"""

import cv2


def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Webcam could not be opened.")
        return

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Failed to receive frame")
            return

        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
