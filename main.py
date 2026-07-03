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


def main():
    raise NotImplementedError("Wire up the loop described in this module's docstring.")


if __name__ == "__main__":
    main()
