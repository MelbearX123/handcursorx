import cv2
import os

#GPT script
video_path = "src/videos/hand_gestures.mp4"
output_folder = "frames"
frame_interval = 1

os.makedirs(output_folder, exist_ok=True)

cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

frame_count = 0
saved_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break  # No more frames
    
    if frame_count % frame_interval == 0:
        filename = os.path.join(output_folder, f"frame_{saved_count:05d}.jpg")
        cv2.imwrite(filename, frame)
        saved_count += 1
    
    frame_count += 1

cap.release()
print(f"✅ Done! Saved {saved_count} frames to '{output_folder}'")