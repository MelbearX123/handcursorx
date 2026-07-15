import cv2
import os

video_path = "./hand_Videos/combined_video.mp4"
output_folder = "frames"
frame_interval = 1

os.makedirs(output_folder, exist_ok=True)


cap = cv2.VideoCapture(video_path)

if not cap.isOpened:
    print("Could not open video")
    exit()

frame_count = 0
saved_count = 0

while True:
    ret, frame = cap.read()
    # Frame was not succesfully read, hopefully video end
    if not ret:
        break

    if frame_count % frame_interval == 0:
        # Joins frame and names it the frame number with 5 0s
        filename = os.path.join(output_folder, f"frame_{saved_count:05d}.jpg")
        cv2.imwrite(filename, frame)
        saved_count += 1

    frame_count += 1

cap.release()  # Release capture
