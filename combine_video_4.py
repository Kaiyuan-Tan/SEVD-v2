import cv2
import numpy as np

# Frame rate and output video settings
frame_rate = 25
video_filename = "combined_output_video.avi"

# Paths to video folders
rgb_path = "rgb"
semantic_path = "semantic"
depth_path = "depth"
optical_path = "optical"
instance_path = "instance"

# Get the video filenames for each folder
rgb_files = [f"{rgb_path}/{i}.avi" for i in range(7)]      # rgb/0.avi to rgb/6.avi
semantic_files = [f"{semantic_path}/{i}.avi" for i in range(7)]  # semantic/0.avi to semantic/6.avi
depth_files = [f"{depth_path}/{i}.avi" for i in range(7)]      # depth/0.avi to depth/6.avi
optical_files = [f"{optical_path}/{i}.avi" for i in range(7)]  # optical/0.avi to optical/6.avi
instance_files = [f"{instance_path}/{i}.avi" for i in range(7)]  # instance/0.avi to instance/6.avi

# Combine all 35 video files (7 videos from each folder)
video_files = rgb_files + semantic_files + depth_files + optical_files + instance_files

# Open video files
caps = [cv2.VideoCapture(f) for f in video_files]

# Get the width and height of the first video (assume all are same size)
w = 1280
h = 720

# Define output video resolution (5x7 grid)
output_width = int(w * 7 * 0.5)  # 7 videos horizontally, adjusted by 0.5
output_height = int(h * 5 * 0.5)  # 5 videos vertically, adjusted by 0.5

# Video writer
fourcc = cv2.VideoWriter_fourcc(*'XVID')
video_writer = cv2.VideoWriter(video_filename, fourcc, frame_rate, (output_width, output_height))

while True:
    frames = []
    rets = []

    # Read frames from all 35 videos
    for vid in caps:
        ret, frame = vid.read()
        rets.append(ret)
        if not ret:
            frame = np.zeros((h, w, 3), dtype=np.uint8)  # Black frame if video ends
        frames.append(frame)

    # Stop when all videos are finished
    if not any(rets):
        break

    # Arrange videos in a 5x7 grid (5 rows, 7 columns)
    rows = []
    for i in range(5):
        # row_frames = frames[i*7:(i+1)*7]  # Extract 7 frames for the row
        row_frames = [
            frames[1 + 7 * i], frames[0 + 7 * i], frames[2 + 7 * i],
            frames[4 + 7 * i], frames[5 + 7 * i], frames[3 + 7 * i], frames[6 + 7 * i]
        ]        
        row = np.hstack(row_frames)  # Horizontally stack the frames in the row
        rows.append(row)  # Add the row to the list

    # Stack all rows vertically to form the 5x7 grid
    combined_frame = np.vstack(rows)

    # Resize the combined frame if necessary to match output resolution
    combined_frame = cv2.resize(combined_frame, (output_width, output_height))

    # Write the frame to the output video
    video_writer.write(combined_frame)

    # Exit condition (wait 10ms for 'q' key)
    if cv2.waitKey(10) & 0xFF == ord("q"):
        break

# Release resources
for vid in caps:
    vid.release()
video_writer.release()

print("DONE")
cv2.destroyAllWindows()
