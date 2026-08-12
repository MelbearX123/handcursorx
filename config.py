"""Central tuning surface for handcursorx.

Every magic number lives here so tuning never means hunting through modules.
All other modules import their constants from this file.
"""

# --- Camera ---
CAMERA_INDEX = 0
FLIP_HORIZONTAL = True
# --- MediaPipe ---
MAX_NUM_HANDS = 1
MIN_DETECTION_CONFIDENCE = 0.7
MIN_TRACKING_CONFIDENCE = 0.5

# --- Position engine ---
SMOOTHING_ALPHA = 0.4
DEAD_ZONE = 0.2 
X_FACTOR = 1.5
Y_FACTOR = 1.5

# --- Gesture engine ---
PINCH_THRESHOLD = 0.2
FIST_THRESHOLD = 0.15
DEBOUNCE_FRAMES = 3  
COOLDOWN_MS = 300

# --- Scroll engine ---
SCROLL_GAIN = 500
SCROLL_SMOOTHING = 0.5
SCROLL_FRICTION = 0.9

# --- Debug ---
SHOW_OVERLAY = True
QUIT_KEY = 27  # Escape key