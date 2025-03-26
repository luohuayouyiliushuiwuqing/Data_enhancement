import os
import shutil

img_path = "/home/igs/yhj_demo/Data_enhancement/Drone_val/images/val_img"
output_base_path = "/home/igs/yhj_demo/Data_enhancement/Drone_val/images/val_img_split"  # Modify this to your desired output path

count = 0
folder_count = 1
folder_limit = 1000  # Number of images per folder

# Create the base output directory if it doesn't exist
if not os.path.exists(output_base_path):
    os.makedirs(output_base_path)

for filename in os.listdir(img_path):
    # Only process files that are images (optional, depending on your needs)
    if filename.endswith(('.jpg', '.png', '.jpeg')):  # Modify extensions as needed
        # Create a new folder when reaching the limit of 1000 images
        if count % folder_limit == 0:
            folder_name = f"folder_{folder_count}"
            folder_path = os.path.join(output_base_path, folder_name)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            folder_count += 1

        # Move the image to the corresponding folder
        src_image_path = os.path.join(img_path, filename)
        dest_image_path = os.path.join(folder_path, filename)
        shutil.move(src_image_path, dest_image_path)

        count += 1

print(f"Total {count} images moved into {folder_count - 1} folders.")
