import cv2
import os

# GPT Generated Script
input_folder = "Hand_Videos"  # input folder variable
output_video = "merged.mp4"  # output folder name

video_files = sorted(
    [
        f
        for f in os.listdir(input_folder)
        if f.lower().endswith((".mp4", ".avi", ".mov", ".mkv"))
    ]
)  # list of video files

if not video_files:
    print("No videos found.")
    exit()

# ---- Reference video (first one) ----
ref_path = os.path.join(
    input_folder, video_files[0]
)  # Grab the path of the first video file
ref_cap = cv2.VideoCapture(ref_path)  # Capture the first video

target_fps = ref_cap.get(
    cv2.CAP_PROP_FPS
)  # Take the fps of the first video and use it as reference
target_w = int(
    ref_cap.get(cv2.CAP_PROP_FRAME_WIDTH)
)  # Take the width of the first video and use it as reference
target_h = int(
    ref_cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
)  # Take the height of the first video and use it as reference

ref_cap.release()  # Release the capture

print(f"Target FPS: {target_fps}")
print(f"Target Resolution: {target_w}x{target_h}")

# ---- Video writer ----
fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # Four character concatenation
out = cv2.VideoWriter(
    output_video, fourcc, target_fps, (target_w, target_h)
)  # Write the new video

# ---- Process videos ----
for video_name in video_files:  # Iterate throught each video to be concatenated
    path = os.path.join(input_folder, video_name)  # get the path
    print(f"Processing {video_name}")

    cap = cv2.VideoCapture(path)  # capture the video

    src_fps = cap.get(cv2.CAP_PROP_FPS)  # get the fps
    fps_ratio = src_fps / target_fps if target_fps > 0 else 1

    frame_index = 0

    while True:
        ret, frame = cap.read()  # read the frame
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
