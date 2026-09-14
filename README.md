# handcursorx

Control your mouse with hand gestures over a webcam — move the cursor, click,
and scroll with your hand. Built on **MediaPipe** hand landmarks (not a
custom-trained detector — see `archive_yolo/` for the earlier YOLO approach).

## Controls

| Gesture | Action |
|---|---|
| Index finger pointing | Move the cursor |
| Thumb + index pinch | Left click |
| Thumb + middle pinch | Right click |
| Open palm, move hand | Scroll (glides, with momentum/inertia) |
| Fist | Stop scrolling (hard brake, kills inertia) |
| `Esc` | Quit (with the preview window focused) |

Gestures are mutually exclusive — each frame the hand is classified as exactly
one gesture, so a pinch never also moves the cursor and a fist always wins.

## How it works

```
webcam frame
  -> tracker      MediaPipe HandLandmarker -> 21 normalized landmarks
  -> gesture_check landmarks -> one Gesture (POINTING / PINCH / RIGHT_PINCH /
                                             OPEN_PALM / FIST / NONE)
  -> position     POINTING     -> smoothed cursor move   (pyautogui.moveTo)
  -> controller   PINCH/R_PINCH-> debounced click        (pyautogui.click)
  -> scroll       OPEN_PALM    -> momentum scroll        (pyautogui.scroll)
  -> overlay      draws landmarks + current gesture onto the preview
```

## Layout

```
config.py              all tuning constants (start here)
main.py                entry point: capture loop + wiring only
handcursor/
  tracker.py           MediaPipe wrapper: frame -> 21 landmarks
  gestures.py          stateless pose detection; gesture_check -> Gesture enum
  position.py          index fingertip -> smoothed cursor movement
  controller.py        clicks: gesture -> action with debounce + cooldown
  scroll.py            open-palm hand motion -> continuous scroll w/ momentum
  overlay.py           debug HUD: landmark skeleton + gesture text
models/                hand_landmarker.task (downloaded, gitignored)
archive_yolo/          the old YOLO detection work (kept for reference)
```

Two design lines run through it: `gestures.py` is **stateless** (pure per-frame
pose checks), while `position.py` / `controller.py` / `scroll.py` are
**stateful** (smoothing, debounce, and scroll momentum need memory across
frames).

## Setup

```
python -m venv .venv
.venv\Scripts\activate       # Windows
pip install -r requirements.txt
python main.py
```

### Model

The MediaPipe hand-landmark model isn't committed (it's ~8 MB and gitignored).
Download it once into `models/`:

```
curl -L -o models/hand_landmarker.task ^
  https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/latest/hand_landmarker.task
```

Source: [MediaPipe HandLandmarker models](https://ai.google.dev/edge/mediapipe/solutions/vision/hand_landmarker#models)

## Tuning

Everything tunable lives in `config.py`. The knobs you'll reach for most:

| Constant | Controls |
|---|---|
| `SMOOTHING_ALPHA` | Cursor smoothing — lower = smoother/laggier, higher = snappier |
| `X_FACTOR` / `Y_FACTOR` | Cursor travel amplification (reach screen edges) |
| `PINCH_THRESHOLD` | How close fingers must be to register a pinch |
| `DEBOUNCE_FRAMES` / `COOLDOWN_MS` | Click debounce + repeat lockout |
| `SCROLL_GAIN` | Overall scroll strength |
| `SCROLL_SMOOTHING` | Scroll glide (lower = floatier) |
| `SCROLL_FRICTION` | Momentum coast length (higher = coasts further) |

## Previous approach: custom-trained YOLO (archived)

Before MediaPipe, this project tried to recognize gestures with a **custom
object detector** trained from scratch. That work lives in `archive_yolo/`:

- **Custom data collection.** Recorded my own webcam footage of each gesture
  (`concatenate.py` merges the clips, `frames.py` splits them into stills).
- **Hand-labelled 8000+ frames in [CVAT](https://www.cvat.ai/).** Every frame
  got a bounding box + gesture class, drawn by hand. This was the bulk of the
  effort — annotation, not code.
- **Trained a YOLOv8 detector** on the annotated dataset, **CUDA-accelerated**
  on a local GPU (`runs/` holds the training outputs and weights).

**Why it was abandoned.** Detecting a whole-hand bounding box *per gesture* is
the wrong tool for cursor control: it throws away the structure of the hand, so
the model has to relearn "what a hand looks like" and "what pose it's in" from
scratch — needing huge, varied, hand-labelled data to generalize at all, and
still producing a jittery box-center for the cursor. MediaPipe's
`HandLandmarker` ships a pretrained model that returns 21 structured landmarks
per frame, so the cursor rides a precise fingertip and gestures fall out of
simple landmark geometry (distances/positions) — **no annotation, no training,
and a far better result.** The lesson: reach for a pretrained model before
building a bespoke pipeline. The archived work is kept as a record of that
detour.

## Notes

- `pyautogui`'s corner failsafe is disabled so the cursor can reach screen
  edges — quit with `Esc` (the preview window must be focused).
- Scroll direction is currently inverted (hand up scrolls down); flip the sign
  in `scroll.py` to change it.
