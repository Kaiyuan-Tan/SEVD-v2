import cv2
import numpy as np

# Frame rate and output video settings
frame_rate = 30
video_filename = "combined_output_video.avi"

# Paths to video folders
video_paths = [f"videos/{i}.avi" for i in range(14)]  # Assuming videos are named 0.avi to 34.avi

# Open video files
videos = [cv2.VideoCapture(path) for path in video_paths]

# Get the width and height of the first video (assume all are the same size)
w, h = 1280, 720  # Set default resolution (modify if needed)

# Define output video resolution (7x5 grid)
scaled_w, scaled_h = int(w * 0.5), int(h * 0.5)  # Resize each video to 50%
output_width, output_height = scaled_w * 7, scaled_h * 2  # 7 videos per row, 5 rows

# Video writer
fourcc = cv2.VideoWriter_fourcc(*'XVID')
video_writer = cv2.VideoWriter(video_filename, fourcc, frame_rate, (output_width, output_height))

while True:
    frames = []
    rets = []

    # Read frames from all 35 videos
    for vid in videos:
        ret, frame = vid.read()
        rets.append(ret)
        if not ret:
            frame = np.zeros((scaled_h, scaled_w, 3), dtype=np.uint8)  # Black frame if video ends
        else:
            frame = cv2.resize(frame, (scaled_w, scaled_h))  # Resize to fit grid
        frames.append(frame)

    # Stop when all videos are finished
    if not any(rets):
        break

    # Arrange videos in 7x5 grid dynamically
    grid_rows = []
    for i in range(2):  # 5 rows
        row_frames = frames[i * 7 : (i + 1) * 7]  # Get 7 videos per row
        row = np.hstack(row_frames)  # Stack horizontally
        grid_rows.append(row)

    # Stack all rows vertically
    combined_frame = np.vstack(grid_rows)

    # Write the frame to output video
    video_writer.write(combined_frame)

    # Exit condition
    if cv2.waitKey(10) & 0xFF == ord("q"):
        break

# Release resources
for vid in videos:
    vid.release()
video_writer.release()

print("DONE")
cv2.destroyAllWindows()
