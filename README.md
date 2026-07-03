s# handcursorx

Control your cursor with hand gestures via webcam, using MediaPipe hand
landmarks (not a custom-trained detector — see `archive_yolo/` for the old
YOLO approach).

## How it works

```
webcam frame -> MediaPipe Hands -> 21 landmarks
  ├─ position engine -> smoothed cursor coords -> pyautogui.moveTo
  └─ gesture engine  -> discrete actions        -> pyautogui click/scroll
```

## Layout

```
config.py            all tuning constants (start here)
main.py              entry point: capture loop + wiring only
handcursor/
  tracker.py         MediaPipe wrapper: frame -> 21 landmarks
  position.py        index tip -> smoothed, dead-zoned screen coords
  gestures.py        stateless pose predicates (is_pinch, is_fist, ...)
  controller.py      state machine: gestures -> actions (debounce/cooldown)
  overlay.py         debug drawing
archive_yolo/        the old YOLO detection work (kept for reference)
```

## Setup

```
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
python main.py
```

## Gestures (planned)

| Gesture               | Action        |
|-----------------------|---------------|
| Index fingertip       | Move cursor   |
| Thumb + index pinch   | Left click    |
| Thumb + middle pinch  | Right click   |
| Two fingers up/down   | Scroll        |
| Fist                  | Pause / reclaim mouse |

## Build order

1. Capture + flip + draw landmarks — confirm 21 dots track your hand.
2. Cursor follows index tip, no smoothing — confirm it moves.
3. Add smoothing + dead-zone — tune until it feels good.
4. Add pinch-to-click with debounce.
5. Add remaining gestures one at a time.
6. Add the pause gesture so you can reclaim your mouse.
