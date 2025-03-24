import os
import shutil

# filename = 'intersection_4_night_1'
image_folder = "/home/apg/workspace/yolodataset/"+ filename +"/images"
label_folder = "/home/apg/workspace/yolodataset/"+ filename +"/rgb_labels"
destination_folder = "/media/apg/f67e28c6-a968-4bc0-adbe-5c4d7fc75007/ktan24_dataset/yolodataset"
destination_image_folder = destination_folder + "/train/images"
destination_label_folder = destination_folder + "/train/labels"
os.makedirs(destination_image_folder, exist_ok = True)
os.makedirs(destination_label_folder, exist_ok = True)

count = 19772
for image_name in os.listdir(image_folder):
    file_id = image_name.split('.')[0]
    new_id = f'{count:06d}'
    label_name = file_id + ".txt"   

    image_path = os.path.join(image_folder, image_name)
    label_path = os.path.join(label_folder, label_name)

    # print(new_id)
    # print(file_id)
    count +=1
    if count % 500 ==0 :
        print(count)

    new_image_name = new_id + ".png"
    new_label_name = new_id + '.txt'

    destination_image_path = os.path.join(destination_image_folder, new_image_name)
    destination_label_path = os.path.join(destination_label_folder, new_label_name)

    shutil.move(image_path, destination_image_path)
    shutil.move(label_path, destination_label_path)
print(count)
print("FINISH")