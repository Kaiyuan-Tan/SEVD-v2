import cv2
import numpy as np

# Frame rate and output video settings
frame_rate = 30
video_filename = "combined_output_video.avi"

# Open video files
videos = [cv2.VideoCapture(f"{i}.avi") for i in range(1, 8)]  # 1.avi to 7.avi

# Get the width and height of the first video (assume all are same size)
w, h = int(videos[0].get(cv2.CAP_PROP_FRAME_WIDTH)), int(videos[0].get(cv2.CAP_PROP_FRAME_HEIGHT))

# Define output video resolution (3x3 grid)
output_width = w * 3
output_height = h * 3

# Video writer
fourcc = cv2.VideoWriter_fourcc(*'XVID')
video_writer = cv2.VideoWriter(video_filename, fourcc, frame_rate, (output_width, output_height))


i = 0
while True:
    i += 1
    frames = []
    rets = []

    # Read frames from all 7 videos
    for vid in videos:
        ret, frame = vid.read()
        rets.append(ret)
        if not ret:
            frame = np.zeros((h, w, 3), dtype=np.uint8)  # Black frame if video ends
        frames.append(frame)

    # Stop when all videos are finished
    if not any(rets):
        break

    # Arrange videos in 3x3 grid with the center video fixed
    top_row = np.hstack((frames[1], frames[0], frames[2])) 
    middle_row = np.hstack((np.zeros((h, w, 3), dtype=np.uint8), frames[6], np.zeros((h, w, 3), dtype=np.uint8)))  # Middle: [4] [center] [5]
    bottom_row = np.hstack((frames[4], frames[5], frames[3])) 

    # Combine all rows vertically
    combined_frame = np.vstack((top_row, middle_row, bottom_row))

    # Write the frame to output video
    video_writer.write(combined_frame)

    # Exit condition
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release resources
for vid in videos:
    vid.release()
video_writer.release()

print("DONE")
cv2.destroyAllWindows()
