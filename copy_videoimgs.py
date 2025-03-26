# coding=utf-8
# vim:set fileencoding=utf-8:

import os.path

base_path = "h264/h264data/0311/datasets"

import os
import shutil

# 定义原始视频文件夹和目标文件夹
# video_folders = ['video01', 'video02']
new_image_folder = '0311_val/images'
new_label_folder = '0311_val/labels'

# 如果目标文件夹不存在，创建它们
os.makedirs(new_image_folder, exist_ok=True)
os.makedirs(new_label_folder, exist_ok=True)

# 遍历每个视频文件夹
for video_folder in os.listdir(base_path):
    images_folder = os.path.join(base_path, video_folder, 'images')
    labels_folder = os.path.join(base_path, video_folder, 'labels')

    # 获取视频文件夹名
    # video_name = os.path.basename(video_folder)

    # 遍历 images 文件夹中的所有 jpg 文件
    for filename in os.listdir(images_folder):
        if filename.endswith('.jpg'):
            # 获取源文件的完整路径
            src_image = os.path.join(images_folder, filename)

            # 构建新文件名并复制文件
            # new_image_name = f"{video_name}_{filename}"
            new_image_name = f"{filename}"
            dst_image = os.path.join(new_image_folder, new_image_name)
            shutil.copy(src_image, dst_image)

    # 遍历 labels 文件夹中的所有 txt 文件
    for filename in os.listdir(labels_folder):
        if filename.endswith('.txt'):
            # 获取源文件的完整路径
            src_label = os.path.join(labels_folder, filename)

            if filename == "classes.txt":
                continue

            # 检查文件是否为空
            if os.path.getsize(src_label) == 0:
                print(f"Skipping empty file: {filename}")
                continue

            # 构建新文件名并复制文件
            # new_label_name = f"{video_name}_{filename}"
            new_label_name = f"{filename}"
            dst_label = os.path.join(new_label_folder, new_label_name)
            shutil.copy(src_label, dst_label)

print("文件复制和重命名完成！")
