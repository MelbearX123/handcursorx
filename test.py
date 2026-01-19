import cv2
import os

#GPT Generated Script
input_folder = "Hand_Videos"
output_video = "merged.mp4"

video_files = sorted([
    f for f in os.listdir(input_folder)
    if f.lower().endswith((".mp4", ".avi", ".mov", ".mkv"))
])

if not video_files:
    print("No videos found.")
    exit()

# ---- Reference video (first one) ----
ref_path = os.path.join(input_folder, video_files[0])
ref_cap = cv2.VideoCapture(ref_path)

target_fps = ref_cap.get(cv2.CAP_PROP_FPS)
target_w = int(ref_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
target_h = int(ref_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

ref_cap.release()

print(f"Target FPS: {target_fps}")
print(f"Target Resolution: {target_w}x{target_h}")

# ---- Video writer ----
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = cv2.VideoWriter(output_video, fourcc, target_fps, (target_w, target_h))

# ---- Process videos ----
for video_name in video_files:
    path = os.path.join(input_folder, video_name)
    print(f"Processing {video_name}")

    cap = cv2.VideoCapture(path)

    src_fps = cap.get(cv2.CAP_PROP_FPS)
    fps_ratio = src_fps / target_fps if target_fps > 0 else 1

    frame_index = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Resize frame
        frame = cv2.resize(frame, (target_w, target_h))

        # FPS normalization
        # Decide whether to write this frame
        if fps_ratio >= 1:
            # Source FPS higher → skip frames
            if frame_index % round(fps_ratio) == 0:
                out.write(frame)
        else:
            # Source FPS lower → duplicate frames
            duplicates = round(1 / fps_ratio)
            for _ in range(duplicates):
                out.write(frame)

        frame_index += 1

    cap.release()

out.release()
print(f"Finished! Output saved as '{output_video}'")