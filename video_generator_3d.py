import cv2
import os
import show_bbox_api
def main():
    if not os.path.exists("videos"):
        os.makedirs("videos")
    for index in range(7):

        # Path to the directory containing images
        image_folder = f'output/sensor.camera.optical_flow/{index}'
        label_folder = f'output/labels_3d/{index}'

        # label_folder = "/media/apg/f67e28c6-a968-4bc0-adbe-5c4d7fc75007/ktan24_dataset/yolodataset/val/intersection_4_night_val/rgb_labels"
        # image_folder = "/media/apg/f67e28c6-a968-4bc0-adbe-5c4d7fc75007/ktan24_dataset/yolodataset/val/intersection_4_night_val/images"
        # Path and name of the output video file
        # video_filename = 'rgb_output_video.avi'
        video_filename = f'videos/{index+7*4}.avi'
        # Desired frame rate of the video
        frame_rate = 30

        # Get list of image files
        images = [img for img in os.listdir(image_folder) if img.endswith(".jpg") or img.endswith(".png")]

        # Sort images by filename (assumes filenames are sequentially numbered)
        images.sort()

        # Check if images list is not empty
        if not images:
            raise ValueError("No images found in the specified directory.")

        # Read the first image to get its dimensions
        first_image = cv2.imread(os.path.join(image_folder, images[0]))
        height, width, layers = first_image.shape

        # Define the codec and create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Use 'XVID' codec for .avi files
        video = cv2.VideoWriter(video_filename, fourcc, frame_rate, (width, height))

        # Write images to video
        for image in images:
            img_path = os.path.join(image_folder, image)
            label_name = os.path.splitext(image)[0]+".txt"
            label_path = os.path.join(label_folder, label_name)

            # show_bbox.draw_frame(img_path label_path)
            # frame = cv2.imread(img_path)
            video.write(show_bbox_api.draw_frame_3d(img_path, label_path))
            # video.write(frame)
        # Release the video writer object
        video.release()
        cv2.destroyAllWindows()

        print(f"Video saved as {video_filename}")

if __name__ == '__main__':
    main()
