"""Central tuning surface for handcursorx.

Every magic number lives here so tuning never means hunting through modules.
All other modules import their constants from this file.
"""

# --- Camera ---
CAMERA_INDEX = 0
FLIP_HORIZONTAL = True  # mirror the frame so hand-right == cursor-right

# --- MediaPipe ---
MAX_NUM_HANDS = 1
MIN_DETECTION_CONFIDENCE = 0.7
MIN_TRACKING_CONFIDENCE = 0.5

# --- Position engine ---
SMOOTHING_ALPHA = 0.4  # EMA factor; higher = snappier, lower = smoother
DEAD_ZONE = 0.2  # fraction of frame cropped on each edge before mapping
# (0.2 => center 60% of the view maps to full screen)
X_FACTOR = 1.5
Y_FACTOR = 1.5

# --- Gesture engine ---
PINCH_THRESHOLD = 0.08  # normalized tip-to-tip distance to count as a pinch
FIST_THRESHOLD = 0.15  # normalized tip-to-wrist distance to count as closed
DEBOUNCE_FRAMES = 3  # consecutive true frames required before a gesture fires
COOLDOWN_MS = 300  # min time before the same action can fire again

# --- Debug ---
SHOW_OVERLAY = True
QUIT_KEY = "f"
